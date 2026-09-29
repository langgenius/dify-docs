"""Regression tests for CJK spacing around literal bold UI labels."""

import runpy
import unittest
from pathlib import Path


CHECKER = runpy.run_path(str(Path(__file__).with_name('check-format-cjk.py')))
check_latin_spacing = CHECKER['check_cjk_latin_spacing']
check_bold_spacing = CHECKER['check_cjk_bold_spacing']


class CjkLatinSpacingTests(unittest.TestCase):
    def test_literal_ui_labels_preserve_product_spacing(self):
        for label in ('Skillを表示', 'Agentsを管理', '管理MCP', 'API拡張設定を管理'):
            with self.subTest(label=label):
                self.assertEqual(check_latin_spacing([f'**{label}**']), [])

    def test_prose_before_between_and_after_labels_still_checked(self):
        lines = [
            '使用API，点击 **管理MCP**。',
            '**Skillを表示** とAPI設定と **Agentsを管理**。',
            '**Skillを表示** を選び、APIを設定します。',
        ]
        violations = check_latin_spacing(lines)
        self.assertEqual([(v.line, v.rule) for v in violations], [
            (1, 'CJK-latin-spacing'),
            (2, 'CJK-latin-spacing'),
            (3, 'CJK-latin-spacing'),
        ])

    def test_multiple_labels_with_correct_prose_spacing(self):
        self.assertEqual(check_latin_spacing([
            '**Skillを表示** と **Agentsを管理** を選択します。',
            '点击 **管理MCP** 并使用 API。',
            '[**Skillを表示**](/ja/page) を選びます。',
        ]), [])

    def test_unclosed_bold_does_not_exempt_prose(self):
        for line in ('**Skillを表示', '**Skillを表示*', '*Skillを表示**'):
            with self.subTest(line=line):
                self.assertEqual(len(check_latin_spacing([line])), 1)
        self.assertEqual([v.line for v in check_latin_spacing([
            '**Skillを表示', 'APIを設定**',
        ])], [1, 2])

    def test_odd_bold_markers_do_not_hide_prose(self):
        lines = [
            '- **Dify Marketplaceは現在、**無料**です。',
            '**説明** 使用API**',
            '**説明** **APIを設定** **',
        ]
        self.assertEqual([v.line for v in check_latin_spacing(lines)], [1, 2, 3])

    def test_bold_markers_in_code_and_urls_do_not_affect_balance(self):
        self.assertEqual(check_latin_spacing([
            '`**` と **Skillを表示** を選択します。',
            '[**Skillを表示**](https://example.com/**) を選択します。',
        ]), [])

    def test_masking_does_not_join_surrounding_prose(self):
        self.assertEqual(check_latin_spacing(['日本語**Skillを表示**API']), [])

    def test_outer_bold_spacing_still_checked(self):
        line = '点击**管理MCP**按钮'
        self.assertEqual(check_latin_spacing([line]), [])
        self.assertEqual([v.rule for v in check_bold_spacing([line])], [
            'CJK-bold-no-space',
        ])

    def test_other_checks_still_inspect_bold_interiors(self):
        violations = CHECKER['check_cjk_halfwidth_punct'](['**管理MCP:設定**'])
        self.assertEqual([v.rule for v in violations], ['CJK-halfwidth-punct'])

    def test_code_urls_and_nonbold_link_text_keep_existing_behavior(self):
        self.assertEqual(check_latin_spacing([
            '`Skillを表示` と https://example.com/管理MCP',
            '```text',
            'APIを設定 **管理MCP**',
            '```',
            '~~~text',
            '使用API',
            '~~~',
        ]), [])
        violations = check_latin_spacing([
            '[APIを設定](/ja/page)',
            '使用API 和 3种模型',
            '「ライセンスID」を入力します。',
        ])
        self.assertEqual([v.line for v in violations], [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
