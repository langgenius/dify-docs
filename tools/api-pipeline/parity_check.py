import json, os, sys
DOCS = os.environ['DOCS']

def op_shape(op):
    params = sorted(
        (p.get('name'), p.get('in'), bool(p.get('required')), (p.get('schema') or {}).get('type'))
        for p in op.get('parameters', []) or []
    )
    responses = sorted((op.get('responses') or {}).keys())
    body_types = sorted(((op.get('requestBody') or {}).get('content') or {}).keys())
    n_samples = len(op.get('x-codeSamples', []))
    return {'params': params, 'responses': responses, 'body': body_types, 'samples': n_samples}

total = 0
en_file = f'{DOCS}/en/api-reference/openapi_service.json'
if not os.path.exists(en_file):
    print('MISSING FILE: en/api-reference/openapi_service.json'); sys.exit(1)
for en_file in [en_file]:
    name = en_file.split('/')[-1]
    with open(en_file, encoding='utf-8') as _fh:
        en = json.load(_fh)
    for lang in ('zh', 'ja'):
        other_file = en_file.replace('/en/', f'/{lang}/')
        if not os.path.exists(other_file):
            print(f'MISSING FILE: {lang}/{name}'); total += 1; continue
        with open(other_file, encoding='utf-8') as _fh:
            other = json.load(_fh)
        en_ops = {(p, m) for p, ms in en['paths'].items() for m in ms if isinstance(ms[m], dict)}
        ot_ops = {(p, m) for p, ms in other['paths'].items() for m in ms if isinstance(ms[m], dict)}
        for p, m in sorted(en_ops - ot_ops):
            print(f'{lang}/{name}: MISSING op {m.upper()} {p}'); total += 1
        for p, m in sorted(ot_ops - en_ops):
            print(f'{lang}/{name}: EXTRA op {m.upper()} {p}'); total += 1
        for p, m in sorted(en_ops & ot_ops):
            a = op_shape(en['paths'][p][m])
            b = op_shape(other['paths'][p][m])
            for key in a:
                if a[key] != b[key]:
                    print(f'{lang}/{name}: {m.upper()} {p} differs in {key}:')
                    print(f'    en: {a[key]}')
                    print(f'    {lang}: {b[key]}')
                    total += 1
print(f'\nTOTAL PARITY ISSUES: {total}')
sys.exit(1 if total else 0)
