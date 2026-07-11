import ast, glob, json, os, re
from collections import defaultdict

WT = os.environ['WT']; DOCS = os.environ['DOCS']

def norm_flask(p):
    return re.sub(r'<(?:[a-z_]+:)?([a-zA-Z_]+)>', r'{\1}', p)

def blank(p):
    return re.sub(r'\{[^}]+\}', '{}', p)

# --- code inventory ---
code_ops = {}  # (blank_path, method) -> {'path': normalized, 'file': f, 'class': cls}
for f in glob.glob(f'{WT}/api/controllers/service_api/**/*.py', recursive=True):
    tree = ast.parse(open(f, encoding='utf-8').read())
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef): continue
        routes = []
        for dec in node.decorator_list:
            if (isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute)
                    and dec.func.attr == 'route' and dec.args):
                routes.extend(a.value for a in dec.args if isinstance(a, ast.Constant))
        if not routes: continue
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)
                   and n.name in ('get','post','put','patch','delete')]
        for r in routes:
            npath = norm_flask(r)
            for m in methods:
                code_ops[(blank(npath), m)] = {'path': npath, 'file': f.replace(WT+'/',''), 'class': node.name}

# --- spec inventory ---
spec_ops = defaultdict(lambda: {'specs': [], 'paths': set()})
for f in [f'{DOCS}/en/api-reference/openapi_service.json']:
    spec = json.load(open(f, encoding='utf-8'))
    name = f.split('/')[-1].replace('openapi_','').replace('.json','')
    for p, ms in spec['paths'].items():
        for m in ms:
            if m not in ('get','post','put','patch','delete'): continue
            e = spec_ops[(blank(p), m)]
            e['specs'].append(name); e['paths'].add(p)

print(f'code operations: {len(code_ops)}   spec unique operations: {len(spec_ops)}')

print('\n=== A. In code but NOT documented ===')
for k in sorted(code_ops):
    if k not in spec_ops:
        c = code_ops[k]
        print(f"  {k[1].upper():6} {c['path']:60} {c['file']}:{c['class']}")

print('\n=== B. Documented but NOT in code (ghosts) ===')
for k in sorted(spec_ops):
    if k not in code_ops:
        e = spec_ops[k]
        print(f"  {k[1].upper():6} {sorted(e['paths'])[0]:60} in {sorted(set(e['specs']))}")

print('\n=== C. Path param NAME mismatches (code vs spec) ===')
for k in sorted(spec_ops):
    if k in code_ops:
        for sp in spec_ops[k]['paths']:
            cp = code_ops[k]['path']
            if sp != cp:
                print(f"  {k[1].upper():6} spec: {sp:55} code: {cp}   ({sorted(set(spec_ops[k]['specs']))})")
