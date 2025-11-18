# Automatic Document Translation

Multi-language document auto-translation system based on GitHub Actions and Dify AI, supporting English, Chinese, and Japanese trilingual translation.

> **Other Languages**: [中文](README.md) | [日本語](README_JA.md)

## How It Works

1. **Trigger Condition**: Automatically runs when pushing to non-main branches
2. **Smart Detection**: Automatically identifies modified `.md/.mdx` files and determines source language
3. **Translation Logic**:
    - ✅ Translates new documents to other languages
    - ❌ Skips existing translation files (avoids overwriting manual edits)
4. **Auto Commit**: Translation results are automatically pushed to the current branch

## System Features

- 🌐 **Multi-language Support**: Configuration-based language mapping, theoretically supports any language extension
- 📚 **Terminology Consistency**: Built-in professional terminology database, LLM intelligently follows terminology to ensure unified technical vocabulary translation
- 🔄 **Concurrent Processing**: Smart concurrency control, translates multiple target languages simultaneously
- 🛡️ **Fault Tolerance**: 3-retry mechanism with exponential backoff strategy
- ⚡ **Incremental Translation**: Only processes changed files, avoids redundant work
- 🧠 **High-Performance Models**: Uses high-performance LLM models to ensure translation quality

## Usage

### For Document Writers

1. Write/modify documents in any language directory
2. Push to branch (non-main)
3. Wait 0.5-1 minute for automatic translation completion
4. **View Translation Results**:
    - Create Pull Request for local viewing and subsequent editing
    - Or view Actions push commit details on GitHub to directly review translation quality

### Supported Language Directories

- **General Documentation**: `en/` ↔ `zh-hans/` ↔ `ja-jp/`
- **Plugin Development Documentation**: `plugin-dev-en/` ↔ `plugin-dev-zh/` ↔ `plugin-dev-ja/`

Note: System architecture supports extending more languages, just modify configuration files

## Important Notes

- System only translates new documents, won't overwrite existing translations
- To update existing translations, manually delete target files then retrigger
- Terminology translation follows professional vocabulary in `termbase_i18n.md`, LLM has intelligent terminology recognition capabilities
- Translation quality depends on configured high-performance models, recommend using high-performance base models in Dify Studio

### System Configuration

#### Terminology Database

Edit `tools/translate/termbase_i18n.md` to update professional terminology translation reference table.

#### Translation Model

Visit Dify Studio to adjust translation prompts or change base models.

---

## 🔧 Development and Deployment Configuration

### Local Development Environment

#### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r tools/translate/requirements.txt
```

#### 3. Configure API Key

Create `.env` file in `tools/translate/` directory:

```bash
DIFY_API_KEY=your_dify_api_key_here
```

#### 4. Run Translation

```bash
# Interactive mode (recommended for beginners)
python tools/translate/main.py

# Command line mode (specify file)
python tools/translate/main.py path/to/file.mdx [DIFY_API_KEY]
```

> **Tip**: Right-click in IDE and select "Copy Relative Path" to use as parameter

### Deploy to Other Repositories

1. **Copy Files**:
    - `.github/workflows/translate.yml`
    - `tools/translate/` entire directory

2. **Configure GitHub Secrets**:
    - Repository Settings → Secrets and variables → Actions
    - Add `DIFY_API_KEY` secret

3. **Test**: Modify documents in branch to verify automatic translation functionality

### Technical Details

- Concurrent translation limited to 2 tasks to avoid excessive API pressure
- Supports `.md` and `.mdx` file formats
- Based on Dify API workflow mode

## TODO

- [ ] Support updating existing translations
