#!/usr/bin/env bash
# Build the Dify manual PDFs with Quire.
#
# Builds one language at a time. Positional args: arg 1 is a manual name (or "all"),
# arg 2 is the language (default en). As a shortcut, a lone language code in the first
# slot (e.g. `build.sh zh`) builds all manuals in that language. A manual name on its
# own still builds English only.
#
# Args:  build.sh [manual|all|lang] [lang]   manual: a name below or "all" (default all)
#                                             lang:   en | zh | ja (default en)
# Usage (run from anywhere):
#   ./mdx2pdf/build.sh                      # all manuals, English
#   ./mdx2pdf/build.sh zh                   # all manuals, Chinese (lone-language shortcut)
#   ./mdx2pdf/build.sh self-host-guide      # one manual, English only
#   ./mdx2pdf/build.sh self-host-guide zh   # one manual, Chinese
#   ./mdx2pdf/build.sh all ja               # all manuals, Japanese
#
# Output: ~/Desktop/dify-pdfs/<lang>/Dify_<manual>_<version>_<lang>_<YYYYMMDD-HHmm>.pdf
# (override the root with MDX2PDF_OUT; the <version> segment is dropped when there is none).
# The cover version comes from MDX2PDF_VERSION if it is set, otherwise it is derived from
# the current git branch: a release/* branch yields its release number, main yields nothing,
# and any other branch uses its name. Set MDX2PDF_VERSION="" to force no version, or to a
# value (e.g. MDX2PDF_VERSION=1.9.0) to override the branch.
# Needs `quire` on PATH (`npm install -g @riskeyl/quire`), or set QUIRE to the command,
# e.g. QUIRE="node /path/to/quire/dist/cli.js" ./mdx2pdf/build.sh
#
# Note: titles below are English. For zh/ja covers, translate them or edit title_for.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(dirname "$script_dir")"
cd "$repo_root"

read -ra QUIRE_CMD <<< "${QUIRE:-quire}"
config="mdx2pdf/quire.config.yaml"
manuals=(use-dify-manual self-host-guide plugin-developer-handbook api-reference)

# Where finished PDFs land. Defaults to a folder on the Desktop so they're easy to find
# and hand to a customer; set MDX2PDF_OUT to put them elsewhere (CI uses a repo-local dir).
out_root="${MDX2PDF_OUT:-$HOME/Desktop/dify-pdfs}"

# Version label printed on every cover. An explicit MDX2PDF_VERSION wins (even when empty,
# which prints no version — that is how main builds and CI suppress it). Otherwise derive it
# from the current git branch: release/* -> the release number; main/master or a detached
# HEAD -> none; any other branch -> its name. CI sets MDX2PDF_VERSION explicitly, so this git
# fallback only fires for local/manual builds.
if [ -n "${MDX2PDF_VERSION+x}" ]; then
  version_label="$MDX2PDF_VERSION"
else
  branch="$(git -C "$repo_root" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
  case "$branch" in
    release/*)           version_label="${branch#release/}" ;;
    main|master|HEAD|"") version_label="" ;;
    *)                   version_label="$branch" ;;
  esac
fi

# Cover title per manual and language. The zh/ja wording follows the docs.json group
# names; adjust it here if you prefer different titles.
title_for() {
  case "$2/$1" in
    en/use-dify-manual)           echo "Dify User Guide" ;;
    en/self-host-guide)           echo "Dify Self-Host Deployment Guide" ;;
    en/plugin-developer-handbook) echo "Dify Plugin Developer Handbook" ;;
    en/api-reference)             echo "Dify API Reference" ;;
    zh/use-dify-manual)           echo "Dify 用户指南" ;;
    zh/self-host-guide)           echo "Dify 自托管部署指南" ;;
    zh/plugin-developer-handbook) echo "Dify 插件开发手册" ;;
    zh/api-reference)             echo "Dify API 文档" ;;
    ja/use-dify-manual)           echo "Dify ユーザーガイド" ;;
    ja/self-host-guide)           echo "Dify セルフホスティングガイド" ;;
    ja/plugin-developer-handbook) echo "Dify プラグイン開発ハンドブック" ;;
    ja/api-reference)             echo "Dify API リファレンス" ;;
    *) echo "No title for manual '$1' in language '$2'" >&2; return 1 ;;
  esac
}

build_one() {
  local manual="$1" lang="$2" manifest title
  manifest="mdx2pdf/$lang/$manual.yaml"
  if [ ! -f "$manifest" ]; then
    echo "Missing manifest: $manifest (no such manual or language; check books.config.mjs and docs.json)." >&2
    return 1
  fi
  title="$(title_for "$manual" "$lang")"
  # Per-language theme: en uses the base; zh/ja add their CJK font (MiSans / Noto Sans JP).
  local theme="mdx2pdf/dify-brand.yaml"
  [ "$lang" != "en" ] && theme="mdx2pdf/dify-brand-$lang.yaml"
  local out_dir="$out_root/$lang"
  mkdir -p "$out_dir"
  # Standardized output base: product, manual, [version], language, export time (to the
  # minute). The version segment is dropped when empty; a branch-derived label's slashes
  # become hyphens so the name stays filesystem-safe. `date` uses the machine's local time.
  local ver_seg=""
  [ -n "$version_label" ] && ver_seg="${version_label//\//-}_"
  local stamp out_base
  stamp="$(date +%Y%m%d-%H%M)"
  out_base="Dify_${manual}_${ver_seg}${lang}_${stamp}"
  echo "==> $manual ($lang) -> $out_dir/$out_base.pdf"
  local args=(convert -c "$config" --theme "$theme" --manifest "$manifest" --title "$title")
  [ -n "$version_label" ] && args+=(--doc-version "$version_label")
  args+=(-o "$out_dir/$out_base")
  "${QUIRE_CMD[@]}" "${args[@]}"
}

target="${1:-all}"
lang="${2:-en}"

# Shortcut: a lone language code in the first slot (e.g. `build.sh zh`) means "all
# manuals in that language". Language codes are never manual names, so there is no
# ambiguity; an explicit second argument keeps the positional manual+lang form.
if [ -z "${2:-}" ]; then
  case "$target" in
    en|zh|ja) lang="$target"; target="all" ;;
  esac
fi

# Keep the manifests in sync with docs.json on every build (same as CI), so a docs.json
# change is picked up automatically with no separate step. docs.json is the single source
# of truth. Clear the generated manifests first, then rebuild them: on a branch whose
# docs.json lacks an expected dropdown (e.g. a backport to an older release), that manual
# then fails with a clear "Missing manifest" error instead of silently building from a
# stale manifest left behind by the backport. The brand themes / config at mdx2pdf/*.yaml
# are untouched (the glob only matches the per-language manifest subdirs).
echo "==> Regenerating manifests from docs.json"
rm -f mdx2pdf/*/*.yaml
node mdx2pdf/build-manifests.mjs

if [ "$target" = "all" ]; then
  for m in "${manuals[@]}"; do build_one "$m" "$lang"; done
else
  build_one "$target" "$lang"
fi
