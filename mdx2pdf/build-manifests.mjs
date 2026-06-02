#!/usr/bin/env node
// Regenerate the Quire manifests from dify-docs/docs.json, for every language.
//
// docs.json is the single source of truth for navigation, so running this keeps each
// manual's page list in sync whenever pages are added, removed, moved, or renamed, and
// whenever a group (section) is renamed or reordered. The build workflow runs it before
// converting, so the published PDFs always match the live navigation.
//
// Output: mdx2pdf/<lang>/<manual>.yaml for each language in books.config.mjs.
// Pure Node, no dependencies. Run from anywhere: node mdx2pdf/build-manifests.mjs
//
// Dropdowns are matched by URL slug (see books.config.mjs), since the display names are
// translated. Section titles come from the (translated) group names; page paths get
// ".mdx"/".md" resolved against disk; the API Reference dropdown's OpenAPI specs become
// `openapi` chapters.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { BOOKS, LANGUAGES } from "./books.config.mjs";

const here = dirname(fileURLToPath(import.meta.url)); // .../mdx2pdf
const repoRoot = resolve(here, ".."); // .../dify-docs
const docs = JSON.parse(readFileSync(join(repoRoot, "docs.json"), "utf8"));
const PREFIX = "../../"; // a manifest at mdx2pdf/<lang>/ is two levels below the repo root
const warnings = [];

// The first page/openapi path under a dropdown, used to identify it by URL slug.
function firstPath(items) {
  for (const it of items) {
    if (typeof it === "string") return it;
    if (it && typeof it === "object") {
      if (it.openapi) return it.openapi;
      const sub = it.pages || it.groups;
      if (sub) {
        const p = firstPath(sub);
        if (p) return p;
      }
    }
  }
  return null;
}

// The slug is the path segment after the language, e.g. "en/use-dify/x" -> "use-dify".
const slugOf = (path) => path.split("/")[1];

function findDropdownBySlug(version, slug) {
  for (const dd of version.dropdowns) {
    const fp = firstPath(dd.pages || dd.groups || []);
    if (fp && slugOf(fp) === slug) return dd;
  }
  return null;
}

function resolveFile(pagePath, exclude) {
  if (exclude.includes(pagePath)) return null;
  for (const ext of [".mdx", ".md"]) {
    if (existsSync(join(repoRoot, pagePath + ext))) return PREFIX + pagePath + ext;
  }
  warnings.push(`page not found on disk: ${pagePath} (.mdx/.md)`);
  return PREFIX + pagePath + ".mdx";
}

function walkItem(item, exclude) {
  if (typeof item === "string") {
    const file = resolveFile(item, exclude);
    return file ? { kind: "page", file } : null;
  }
  if (item && typeof item === "object") {
    if (item.openapi) return { kind: "openapi", file: PREFIX + item.openapi, title: item.group };
    if (item.group) {
      const children = walkItems(item.pages || item.groups || [], exclude);
      return children.length ? { kind: "section", title: item.group, children } : null;
    }
  }
  warnings.push(`skipped unrecognized nav item: ${JSON.stringify(item).slice(0, 80)}`);
  return null;
}

function walkItems(items, exclude) {
  return items.map((it) => walkItem(it, exclude)).filter(Boolean);
}

function emitList(nodes, indent) {
  const lines = [];
  for (const n of nodes) {
    if (n.kind === "page") {
      lines.push(`${indent}- file: "${n.file}"`);
    } else if (n.kind === "openapi") {
      lines.push(`${indent}- openapi: "${n.file}"`);
      lines.push(`${indent}  title: "${n.title}"`);
    } else if (n.kind === "section") {
      lines.push(`${indent}- section: "${n.title}"`);
      lines.push(`${indent}  children:`);
      lines.push(emitList(n.children, indent + "    "));
    }
  }
  return lines.join("\n");
}

for (const lang of LANGUAGES) {
  const l = docs.navigation.languages.find((x) => x.language === lang);
  if (!l) {
    warnings.push(`language "${lang}" not found in docs.json`);
    continue;
  }
  const version = l.versions[0];
  const outDir = join(here, lang);
  mkdirSync(outDir, { recursive: true });
  for (const book of BOOKS) {
    const dd = findDropdownBySlug(version, book.slug);
    if (!dd) {
      warnings.push(`no dropdown for slug "${book.slug}" in ${lang}`);
      continue;
    }
    const nodes = walkItems(dd.pages || dd.groups || [], book.exclude || []);
    const header =
      `# AUTO-GENERATED from docs.json by mdx2pdf/build-manifests.mjs — do not edit by hand.\n` +
      `# Source: the "${dd.dropdown}" dropdown (${lang}). Re-run the generator after docs.json changes.\n\n`;
    writeFileSync(join(outDir, book.manifest), header + emitList(nodes, "") + "\n");
    console.log(`${lang}/${book.manifest}: ${nodes.length} top-level entries from "${dd.dropdown}"`);
  }
}

if (warnings.length) {
  console.warn(`\n${warnings.length} warning(s):`);
  for (const w of warnings) console.warn("  - " + w);
}
