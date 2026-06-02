# Building the Dify documentation PDFs

Internal tooling that turns the Dify docs into branded PDF manuals with [Quire](https://github.com/RiskeyL/quire). These files are not published pages.

## Setup (once)

- Install Quire: `npm install -g @riskeyl/quire`
- Install the fonts the manuals are built with (all free): 

    - **Inter** for Latin text
    - **MiSans** for Chinese
    - **Noto Sans JP** for Japanese
    
    These are the same fonts the published PDFs use. If one is missing, the text falls back automatically (PingFang SC / Noto Sans SC for Chinese, Hiragino Sans / Yu Gothic for Japanese), so a build never fails for want of a font.

## Build

From the repo root:

```bash
./mdx2pdf/build.sh                    # all manuals, English
./mdx2pdf/build.sh zh                 # all manuals in Chinese (or ja for Japanese)
./mdx2pdf/build.sh self-host-guide    # one manual, English
./mdx2pdf/build.sh self-host-guide zh # one manual, Chinese (or ja for Japanese)

```

Manuals: `use-dify-manual`, `self-host-guide`, `plugin-developer-handbook`, `api-reference`.

**To export a specific release**, check out its branch first; the release number is then printed on the cover. Building from `main` gives you the latest.

```bash
git checkout release/v1.14.0   # then run build.sh; the cover reads v1.14.0
```

Each build first rebuilds the manuals' page lists from `docs.json`, so they always match the current navigation.

PDFs are written to `~/Desktop/dify-pdfs/<lang>/`; set `MDX2PDF_OUT` to use a different location.

If `quire` is not on your PATH, point the script at a build with `QUIRE="node /path/to/quire/dist/cli.js" ./mdx2pdf/build.sh …`.

## Export a chosen set of pages

To build a PDF of pages you pick (rather than a whole manual):

1. **List the pages** in a YAML file at the repo root, say `my-guide.yaml`. Each `file:` is a doc path under `en/` (or `zh/`/`ja/`). Wrap pages in `section:` blocks to make chapters. 

    To start from an existing layout, copy one of `mdx2pdf/en/*.yaml` (or `zh/`/`ja/`).

   ```yaml
   # my-guide.yaml
   - section: "My Selection"
     children:
       - file: "en/self-host/quick-start/docker-compose.mdx"
       - file: "en/self-host/quick-start/faqs.mdx"
   ```

2. **Build it** from the repo root. `-c mdx2pdf/quire.config.yaml` pulls in the shared build settings (brand theme, site base URL, PDF output), so the command stays short:

   ```bash
   quire convert -c mdx2pdf/quire.config.yaml --manifest my-guide.yaml \
     --title "My Guide" -o ~/Desktop/dify-pdfs/en/my-guide
   ```

That writes `~/Desktop/dify-pdfs/en/my-guide.pdf`. The shared config already sets the English theme, so English pages need nothing more; for Chinese or Japanese, add `--theme mdx2pdf/dify-brand-zh.yaml` (or `dify-brand-ja.yaml`) to switch to the CJK fonts. 

## What's here

- `build.sh` — the build wrapper; also holds the per-language cover titles.
- `build-manifests.mjs` — regenerates the manifests from `docs.json`; runs automatically at the start of every `build.sh` build and in CI (the dropdown-to-manual mapping is in `books.config.mjs`).
- `dify-brand.yaml` — the theme (colors, fonts, logo); `dify-brand-zh.yaml` / `dify-brand-ja.yaml` add the Chinese / Japanese fonts. `quire.config.yaml` — shared build options.
- `en/`, `zh/`, `ja/` — the generated manifests.

CI (`.github/workflows/build-pdfs.yml`) builds and publishes all three language sets (en, zh, ja) automatically on every docs change.
