"""Isolated git fixtures. Never touches the user's product/docs repositories."""

import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import collect_impact as impact


class ImpactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.product = self.root / 'product'
        self.docs = self.root / 'docs'
        for repo in (self.product, self.docs):
            repo.mkdir()
            self.git(repo, 'init', '-q')
            self.git(repo, 'config', 'user.name', 'Fixture')
            self.git(repo, 'config', 'user.email', 'fixture@example.invalid')
        self.locale('en-US', {'rename': 'Old name', 'removed': 'Remove me',
                              'items_one': '{{count}} item', 'same': 'Same', 'nested': {'title': 'Before'}})
        self.locale('zh-Hans', {'rename': '旧名称', 'removed': '移除', 'items_one': '{{count}} 项'})
        self.write(self.product, 'web/app/shared.tsx', """import { useTranslation } from 'react-i18next'
const { t } = useTranslation('appDebug')
t($ => $['rename'])
t('appDebug:removed')
t($ => $['items'], { count: 2 })
t($ => $.nested.title)
t(prefix + state)
""")
        self.write(self.product, 'web/app/page.tsx', "import Shared from '@/app/shared'\n")
        self.write(self.product, 'web/app/another.tsx', "import Shared from './shared'\n")
        self.write(self.product, 'web/app/__tests__/shared.spec.tsx', "expect(t('rename')).toBe('Old name')\n")
        self.base = self.commit(self.product)
        self.locale('en-US', {'rename': 'New name', 'added': 'Added copy',
                              'items_one': '{{total}} <strong>item</strong>', 'same': 'Same', 'nested': {'title': 'After'}})
        self.locale('zh-Hans', {'rename': '旧名称', 'items_one': '{{total}} 项', 'added': '新增'})
        self.head = self.commit(self.product)
        self.write(self.docs, 'en/cloud/guide.mdx', '# Guide\nClick **Old name**.\n![Panel](/images/panel.png)\n<video src="/demo.gif" />\n')
        self.write(self.docs, 'zh/cloud/guide.mdx', '# 指南\n点击 **旧名称**。\n')
        self.write(self.docs, 'ja/cloud/guide.mdx', '# Guide\n未翻訳\n')
        self.write(self.docs, 'en/unrelated.mdx', 'Old namesake must not match.\n')
        self.commit(self.docs)

    def git(self, repo, *args):
        return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.PIPE).decode().strip()

    def write(self, repo, path, text):
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def locale(self, locale, values):
        self.write(self.product, f'web/i18n/locales/{locale}/app-debug.json', json.dumps(values, ensure_ascii=False))

    def commit(self, repo):
        self.git(repo, 'add', '.')
        self.git(repo, 'commit', '-qm', 'fixture')
        return self.git(repo, 'rev-parse', 'HEAD')

    def report(self, **kwargs):
        return impact.collect(self.product, self.docs, self.base, self.head, **kwargs)

    def keyed(self, **kwargs):
        return {c['key']: c for c in self.report(**kwargs)['changes']}

    def test_added_modified_removed_and_nested(self):
        changes = self.keyed()
        self.assertEqual(set(changes), {'added', 'removed', 'rename', 'items_one', 'nested.title'})
        self.assertEqual(changes['added']['status'], 'added')
        self.assertEqual(changes['removed']['status'], 'removed')
        self.assertEqual(changes['nested.title']['after'], 'After')
        self.assertEqual(changes['rename']['status'], 'modified')

    def test_selectors_plural_base_and_imports(self):
        changes = self.keyed()
        rename = changes['rename']['code_after']
        source = [h for h in rename['references']['items'] if h['kind'] == 'source_candidate']
        self.assertEqual(len(source), 1)
        self.assertTrue(source[0]['namespace_hint'])
        self.assertEqual(source[0]['line'], 3)
        self.assertEqual(rename['references']['total'], 2)
        self.assertEqual({d['direct_importer'] for d in rename['direct_importers']['items']},
                         {'web/app/page.tsx', 'web/app/another.tsx'})
        for key in ('items_one', 'nested.title', 'removed'):
            self.assertEqual(changes[key]['code_after']['references']['total'], 1)
        self.assertEqual(changes['added']['code_after']['references']['total'], 0)

    def test_contract_and_translation_status(self):
        changes = self.keyed()
        self.assertEqual(changes['items_one']['before_contract']['variables'], ['count'])
        self.assertEqual(changes['items_one']['after_contract']['variables'], ['total'])
        self.assertEqual(changes['items_one']['after_contract']['tags'], ['</strong>', '<strong>'])
        self.assertEqual(changes['rename']['translations'][0]['status'], 'unchanged')
        self.assertEqual(changes['removed']['translations'][0]['status'], 'missing_at_head')

    def test_docs_old_localized_text_and_media(self):
        docs = self.keyed()['rename']['documentation']['pages']
        self.assertEqual(docs['total'], 2)
        english = next(p for p in docs['items'] if p['path'].startswith('en/'))
        self.assertEqual(english['media_to_inspect'], ['/demo.gif', '/images/panel.png'])
        self.assertEqual(english['occurrences']['items'][0]['line'], 2)
        self.assertEqual(set(english['language_sibling_candidates']), {'zh/cloud/guide.mdx', 'ja/cloud/guide.mdx'})

    def test_limits_explicitly_mark_omissions(self):
        change = self.keyed(limit=1)['rename']
        self.assertEqual(change['code_after']['references']['omitted'], 1)
        self.assertEqual(change['code_after']['direct_importers']['omitted'], 1)
        self.assertEqual(change['documentation']['pages']['omitted'], 1)

    def test_key_filter_and_invalid_filter(self):
        self.assertEqual(list(self.keyed(only_keys=['app-debug:rename'])), ['rename'])
        with self.assertRaisesRegex(ValueError, 'no English change'):
            self.report(only_keys=['app-debug:same'])

    def test_dirty_working_tree_not_read_or_modified(self):
        self.write(self.product, 'web/app/shared.tsx', 'uncommitted changes')
        self.write(self.docs, 'en/cloud/guide.mdx', 'uncommitted document')
        before = [self.git(p, 'status', '--porcelain') for p in (self.product, self.docs)]
        report = self.report()
        self.assertTrue(report['product_head']['working_tree_changes_excluded'])
        self.assertTrue(report['docs']['working_tree_changes_excluded'])
        self.assertTrue(next(c for c in report['changes'] if c['key'] == 'rename')['documentation']['pages']['total'])
        self.assertEqual(before, [self.git(p, 'status', '--porcelain') for p in (self.product, self.docs)])
        self.assertEqual((self.docs / 'en/cloud/guide.mdx').read_text(), 'uncommitted document')

    def test_no_changes(self):
        report = impact.collect(self.product, self.docs, self.head, self.head)
        self.assertEqual(report['changes'], [])
        self.assertIn('英文变更：0 条', impact.markdown(report))

    def test_wrong_docs_layout_is_error(self):
        self.git(self.docs, 'rm', '-r', 'en', 'zh', 'ja')
        self.write(self.docs, 'README.md', 'Unsupported documentation layout')
        self.commit(self.docs)
        with self.assertRaisesRegex(ValueError, 'No supported documentation'):
            self.report()

    def test_invalid_ref(self):
        with self.assertRaises(ValueError):
            impact.collect(self.product, self.docs, '--evil', self.head)

    def test_malformed_json_is_error(self):
        self.write(self.product, 'web/i18n/locales/en-US/app-debug.json', '{broken')
        self.head = self.commit(self.product)
        with self.assertRaisesRegex(ValueError, 'Cannot parse'):
            self.report()

    def test_duplicate_json_and_ambiguous_flattening(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON'):
            json.loads('{"a":"x","a":"y"}', object_pairs_hook=impact.unique_object)
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            impact.flatten({'a.b': 'x', 'a': {'b': 'y'}}, 'fixture')

    def test_array_locale_values_and_short_doc_key(self):
        self.assertEqual(impact.flatten({'features': ['First', 'Second']}, 'fixture'),
                         {'features.0': 'First', 'features.1': 'Second'})
        self.assertNotIn('rename', self.keyed()['rename']['documentation']['search_terms'])

    def test_unsupported_ts_source_is_error(self):
        self.write(self.product, 'web/i18n/en-US/legacy.ts', 'export default {}')
        self.head = self.commit(self.product)
        with self.assertRaisesRegex(ValueError, 'Only JSON'):
            self.report()

    def test_paths_with_spaces_and_output_protection(self):
        output = self.root / 'reports with spaces'
        args = ['--product-repo', str(self.product), '--docs-repo', str(self.docs),
                '--base', self.base, '--head', self.head, '--output-dir', str(output)]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(impact.main(args), 0)
            self.assertEqual(impact.main(args), 2)
            self.assertEqual(impact.main(args[:-1] + [str(self.product / 'report')]), 2)
            self.assertEqual(impact.main(args[:-1] + [str(self.root / 'bad')] + ['--limit', '0']), 2)
        self.assertEqual(json.loads((output / 'report.json').read_text())['schema_version'], 1)
        self.assertIn('后续判断', (output / 'report.md').read_text())

    def test_lookup_unchanged_key_without_diff(self):
        report = impact.lookup(self.product, self.docs, self.base, only_keys=['app-debug:rename'])
        self.assertEqual(report['resolution'], 'resolved')
        self.assertEqual(report['product_head']['commit'], self.base)
        target = report['changes'][0]
        self.assertEqual(target['before'], 'Old name')
        self.assertEqual(target['documentation']['pages']['total'], 2)
        self.assertEqual(target['code_after']['references']['total'], 2)
        rendered = impact.markdown(report)
        self.assertIn('当前英文', rendered)
        self.assertNotIn('新文：', rendered)
        self.assertNotIn('修改后代码', rendered)

    def test_lookup_text_in_non_english_locale(self):
        report = impact.lookup(self.product, self.docs, self.head, text='旧名称', locale='zh-Hans')
        self.assertEqual(report['changes'][0]['key'], 'rename')
        self.assertEqual(report['changes'][0]['before'], 'New name')
        self.assertEqual(report['changes'][0]['matched_value'], '旧名称')

    def test_lookup_duplicate_text_requires_selection(self):
        self.locale('en-US', {'first': 'Same label', 'second': 'Same label'})
        ref = self.commit(self.product)
        report = impact.lookup(self.product, self.docs, ref, text='Same label')
        self.assertEqual(report['resolution'], 'needs_selection')
        self.assertEqual(len(report['candidates']), 2)
        self.assertEqual(report['changes'], [])
        self.assertIn('--key', impact.markdown(report))
        selected = impact.lookup(self.product, self.docs, ref, only_keys=['app-debug:second'])
        self.assertEqual(selected['changes'][0]['key'], 'second')

    def test_lookup_missing_or_partial_text_and_invalid_key(self):
        for value in ['Not a known string', 'New']:
            report = impact.lookup(self.product, self.docs, self.head, text=value)
            self.assertEqual(report['resolution'], 'not_found')
            self.assertEqual(report['changes'], [])
        with self.assertRaisesRegex(ValueError, 'Keys not found'):
            impact.lookup(self.product, self.docs, self.head, only_keys=['app-debug:removed'])
        with self.assertRaisesRegex(ValueError, 'Locale not present'):
            impact.lookup(self.product, self.docs, self.head, text='New name', locale='xx-XX')

    def test_lookup_dirty_tree_untouched_and_omissions(self):
        self.write(self.product, 'web/app/shared.tsx', 'uncommitted')
        before = self.git(self.product, 'status', '--porcelain')
        report = impact.lookup(self.product, self.docs, self.head, only_keys=['app-debug:rename'], limit=1)
        self.assertTrue(report['product_head']['working_tree_changes_excluded'])
        self.assertEqual(report['changes'][0]['code_after']['references']['omitted'], 1)
        self.assertEqual(self.git(self.product, 'status', '--porcelain'), before)

    def test_lookup_cli_result_codes_and_validation(self):
        self.locale('en-US', {'first': 'Same label', 'second': 'Same label'})
        self.commit(self.product)
        common = ['--mode', 'lookup', '--product-repo', str(self.product), '--docs-repo', str(self.docs)]
        cases = [(['--key', 'app-debug:first'], 0),
                 (['--text', 'Same label'], 3), (['--text', 'Missing'], 4),
                 (['--text', 'Same label', '--key', 'app-debug:first'], 2),
                 (['--text', ''], 2), ([], 2),
                 (['--base', self.base, '--key', 'app-debug:first'], 2)]
        for i, (options, code) in enumerate(cases):
            out = self.root / f'lookup-{i}'
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(impact.main(common + options + ['--output-dir', str(out)]), code)
            self.assertEqual(out.exists(), code in (0, 3, 4))

    def add_text_candidates(self):
        self.write(self.product, 'web/i18n/locales/en-US/help.json', json.dumps({
            'instruction': 'Click Old name to continue.',
            'newInstruction': 'Choose New name.',
            'unrelated': 'Old namesake',
            'sameText': 'Old name',
            'differentLanguage': '点击旧名称按钮。',
        }))
        self.write(self.product, 'web/i18n/locales/zh-Hans/help.json', json.dumps({
            'instruction': '点击旧名称按钮。', 'differentLanguage': 'Click Old name.',
        }))
        self.write(self.product, 'e2e/rename.spec.ts',
                   "page.getByRole('button', { name: 'Old name' }).click()\n"
                   "expect(page.getByText('New name')).toBeVisible()\n"
                   "expect(page.getByText('Old namesake')).toBeVisible()\n")
        self.write(self.product, 'web/app/__snapshots__/panel.snap', 'button: Old name\n')
        self.write(self.product, 'tests/rename.ts', "getByText('旧名称')\n")
        self.write(self.product, 'web/app/not-a-test.ts', "const text = 'Old name'\n")
        self.write(self.product, 'scripts/out-of-scope.spec.ts', "getByText('Old name')\n")
        self.write(self.product, 'web/node_modules/tests/ignored.ts', "getByText('Old name')\n")
        self.head = self.commit(self.product)

    def test_related_copy_old_new_locales_and_self_exclusion(self):
        self.add_text_candidates()
        result = self.keyed(only_keys=['app-debug:rename'])['rename']['text_impact']
        related = result['related_copy_after']['items']
        self.assertEqual({(h['locale'], h['key']) for h in related}, {
            ('en-US', 'instruction'), ('en-US', 'newInstruction'),
            ('en-US', 'sameText'), ('zh-Hans', 'instruction'),
        })
        self.assertEqual(result['related_copy_before']['total'], 0)
        self.assertTrue(all(h['namespace'] == 'help' for h in related))
        self.assertEqual({t['text'] for t in result['search_terms']}, {'Old name', 'New name', '旧名称'})

    def test_test_text_search_without_key_and_with_snapshots(self):
        self.add_text_candidates()
        evidence = self.keyed(only_keys=['app-debug:rename'])['rename']['text_impact']
        hits = evidence['test_text_after']['items']
        self.assertEqual({h['path'] for h in hits}, {
            'e2e/rename.spec.ts', 'web/app/__snapshots__/panel.snap',
            'web/app/__tests__/shared.spec.tsx', 'tests/rename.ts',
        })
        self.assertEqual([h['line'] for h in hits if h['path'] == 'e2e/rename.spec.ts'], [1, 2])
        self.assertEqual(evidence['test_text_before']['total'], 1)
        self.assertIn("getByRole('button'", hits[0]['context'])

    def test_lookup_searches_current_text_not_historical_names(self):
        self.add_text_candidates()
        report = impact.lookup(self.product, self.docs, self.head, only_keys=['app-debug:rename'])
        evidence = report['changes'][0]['text_impact']
        self.assertEqual({t['text'] for t in evidence['search_terms']}, {'New name', '旧名称'})
        self.assertEqual({h['key'] for h in evidence['related_copy_after']['items']},
                         {'newInstruction', 'instruction'})
        self.assertEqual(evidence['test_text_after']['total'], 2)
        rendered = impact.markdown(report)
        self.assertIn('e2e/rename.spec.ts:2', rendered)
        self.assertIn('当前关联文案', rendered)
        self.assertNotIn('修改前关联文案', rendered)

    def test_text_candidate_limits_and_empty_results(self):
        self.add_text_candidates()
        change = self.keyed(only_keys=['app-debug:rename'], limit=1)['rename']
        self.assertEqual(change['text_impact']['related_copy_after']['omitted'], 3)
        self.assertEqual(change['text_impact']['test_text_after']['omitted'], 4)
        self.assertEqual(impact.test_text_matches({}, [], 1), {'total': 0, 'omitted': 0, 'items': []})

    def test_text_candidates_use_immutable_snapshots(self):
        self.add_text_candidates()
        self.write(self.product, 'e2e/rename.spec.ts', 'uncommitted test\n')
        self.write(self.product, 'web/i18n/locales/en-US/help.json', '{"instruction": "uncommitted"}')
        before = self.git(self.product, 'status', '--porcelain')
        result = self.keyed(only_keys=['app-debug:rename'])['rename']['text_impact']
        self.assertEqual(result['related_copy_after']['total'], 4)
        self.assertEqual(result['test_text_after']['total'], 5)
        self.assertEqual(before, self.git(self.product, 'status', '--porcelain'))

    def test_text_matching_literals_case_and_boundaries(self):
        terms = [{'locale': 'en-US', 'text': 'Save'}, {'locale': 'en-US', 'text': 'Run (test)?'}]
        hits = impact.test_text_matches({'web/a.spec.ts':
            'Saved\nAutosave\nsave\nRun (test)?\nRun test\n'}, terms, 50)
        self.assertEqual([h['line'] for h in hits['items']], [3, 4])

    def test_candidate_ranking_keeps_english_and_literal_tests_visible(self):
        terms = [{'locale': 'en-US', 'text': 'Save'}, {'locale': 'ar-TN', 'text': 'حفظ'}]
        catalog = {
            ('ar-TN', 'help'): {'path': 'ar.json', 'values': {'hint': 'حفظ'}},
            ('en-US', 'help'): {'path': 'en.json', 'values': {'hint': 'Click Save.'}},
        }
        related = impact.related_copy({'namespace': 'common', 'key': 'save'}, catalog, terms, 1)
        self.assertEqual(related['items'][0]['locale'], 'en-US')
        self.assertEqual(related['omitted'], 1)
        tests = impact.test_text_matches({'web/a.spec.ts':
            "getByText('common.operation.save')\ngetByRole('button', { name: 'Save' })\n"}, terms, 1)
        self.assertEqual(tests['items'][0]['line'], 2)
        self.assertEqual(tests['items'][0]['match_basis'], 'exact_literal')
        self.assertEqual(tests['omitted'], 1)

    def test_added_removed_strings_have_text_candidates(self):
        self.write(self.product, 'tests/copy.test.ts', "expect('Remove me')\nexpect('Added copy')\n")
        self.head = self.commit(self.product)
        changes = self.keyed()
        for key in ('removed', 'added'):
            self.assertEqual(changes[key]['text_impact']['test_text_after']['total'], 1)
        rendered = impact.markdown(self.report())
        self.assertIn('修改前关联文案', rendered)
        self.assertIn('修改后测试文字匹配', rendered)

    def test_diff_cli_writes_new_evidence(self):
        self.add_text_candidates()
        output = self.root / 'text-evidence-report'
        with contextlib.redirect_stdout(io.StringIO()):
            status = impact.main(['--product-repo', str(self.product), '--docs-repo', str(self.docs),
                                  '--base', self.base, '--head', self.head, '--key', 'app-debug:rename',
                                  '--output-dir', str(output)])
        self.assertEqual(status, 0)
        report = json.loads((output / 'report.json').read_text())
        self.assertEqual(report['changes'][0]['text_impact']['test_text_after']['total'], 5)
        self.assertIn('e2e/rename.spec.ts:1', (output / 'report.md').read_text())


if __name__ == '__main__':
    unittest.main()
