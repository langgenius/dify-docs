// Which docs.json dropdown each downloadable manual is built from, and for which
// languages. Dropdowns are matched by URL slug (the path segment after the language,
// e.g. "use-dify"), NOT by the dropdown's display name, because the names are
// translated per language ("Use Dify" / "使用 Dify" / "Dify を使う"). Add a page path
// to `exclude` to keep it out of a manual (e.g. a page that makes no sense in print).

export const LANGUAGES = ["en", "zh", "ja"];

export const BOOKS = [
  { manifest: "use-dify-manual.yaml",           slug: "use-dify",       exclude: [] },
  { manifest: "self-host-guide.yaml",           slug: "self-host",      exclude: [] },
  { manifest: "plugin-developer-handbook.yaml", slug: "develop-plugin", exclude: [] },
  { manifest: "api-reference.yaml",             slug: "api-reference",  exclude: [] },
];
