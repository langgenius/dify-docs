# tools

This directory contains Python scripts designed to automate various maintenance and generation tasks for the Dify documentation, such as content synchronization and navigation file updates.

## How to use

### Auto apply when PR

Tools will work and apply changes by git push when the PR is made from a branch under the same repo by GitHub Actions.

When the PR is from a forked repo, it will not work since GitHub Actions will not have permission to push back to the forked repo.

### Manually apply

Run the `tools/main_docs_bundle.py` script.

**Prerequisites**: Ensure you have the necessary Python environment and dependencies installed (e.g., `python3.x`, `pip install -r requirements.txt` if applicable).

## Features

### General

- Remove all "Edit this page" and "Report an issue" cards.
- Then reapply them to all mdx docs under folder `plugin-dev-**`, en, ja-jp, zh-hans.
    - Also apply standard markdown ending syntax - leave a blank line before the last line.

### Plugin Dev docs

- Rename plugin-dev-** docs based on its frontmatter.
    - Automatically sync references at other docs when renaming happens. (Optional - consider specifying how this is triggered, e.g., via a script flag like `--sync-refs`)
- Apply plugin-dev-** docs to docs.json (Auto Mintlify deployment).
    - Remove non-existing docs.
    - Leave docs that already exist.
        - Optionally rebuild all plugin-dev-** docs - would be useful when changing order or nested structure. (Consider specifying how this is triggered, e.g., via a script flag like `--rebuild-all`)

## Additional notes

Plugin Dev docs manually modified:

- The "Contributing" documentation is manually positioned at the end of its relevant navigation group (e.g., in `docs.json` or sidebar configuration).
- The order of a few documents requires manual adjustment as the automated process defaults to alphabetical sorting.
