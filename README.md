<!-- template:start -->
# python-cli-template

A starting point for a small Python command-line tool, with the release machinery already
working: tests on three systems, standalone executables, PyPI, an optional browser version and
Windows code signing. Extracted from [mermaid2pptx](https://github.com/JeanMichelDurand/mermaid2pptx).

**Start a project from it:**

1. On GitHub, **Use this template** → **Create a new repository**, named like the package
   (lowercase letters, digits and underscores, e.g. `csv2xlsx`). Clone it.
2. `python3 rename.py csv2xlsx --description "Convert CSV files into formatted Excel workbooks"`
   renames the package, the command, the URLs and the workflows, removes this section and
   deletes itself. It also tells you whether the name is still free on PyPI.
3. `python3 install.py dev && .venv/bin/python -m pytest`, commit, push.
4. Go through [SETUP.md](SETUP.md) once: the GitHub and PyPI settings no file can carry.
5. Replace `core.py` (the example counts lines and words) with the real work.

What you get:

| Piece | Where |
|---|---|
| `src/` layout package, version in one place (`__version__`) | `src/myproject/`, `pyproject.toml` |
| Tests on Linux, Windows, macOS × Python 3.10 and 3.13, ruff, one required check `ci-ok` | `.github/workflows/ci.yml` |
| Tag → version check, tests, one-file executables smoke-tested, GitHub release, PyPI | `.github/workflows/release.yml` |
| Browser version (Pyodide runs the package's own wheel), deployed on each tag | `web/index.html`, `.github/workflows/pages.yml` |
| Windows signing through SignPath, off until its secret exists | `release.yml`, `CODE_SIGNING.md` |
| Protected `main` (pull request + `ci-ok`, squash only) | `.github/rulesets/main.json` |
| Issue forms, PR checklist, code owners, monthly Dependabot | `.github/` |
| No file over 500 lines, enforced by a test | `tests/test_code_size.py` |
| A venv and a launcher without knowing pip, for users who get a zip | `install.py` |

Everything below this section is the new project's README, ready to fill in.

<!-- template:end -->
# myproject

One line saying what the tool does.

```sh
myproject notes.txt report.md
cat notes.txt | myproject -
```

```text
notes.txt: 2 lines, 9 words
```

## Install

Pick one:

- **No install at all:** the [browser version](https://jeanmicheldurand.github.io/python-cli-template/)
  runs in the page; your files never leave your computer.
- **A single executable**, no Python needed: download it from the
  [latest release](https://github.com/JeanMichelDurand/python-cli-template/releases/latest)
  (Windows, Linux, macOS).
- **With Python 3.10 or later:** `pipx install myproject` (or `uv tool install myproject`).
- **From a copy of this folder:** `python3 install.py` (Windows: `py install.py`), then `./myproject`
  (Windows: `myproject.bat`).

## Usage

```text
myproject FILE [FILE ...]
```

| Option | Meaning |
|---|---|
| `FILE` | text files to read, or `-` for standard input |
| `--version` | print the version |

Exit code 0 when every file worked, 1 otherwise; errors go to standard error, one line per file.

## Development

```sh
python3 install.py dev          # Windows: py install.py dev
.venv/bin/python -m pytest      # Windows: .venv\Scripts\python.exe -m pytest
.venv/bin/ruff check .
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the conventions and the code map.

## Releasing

1. Record the changes under a new version heading in [CHANGELOG.md](CHANGELOG.md).
2. Bump `__version__` in `src/myproject/__init__.py`, open a pull request and merge it into `main`.
3. Tag the merged commit, not your branch:
   `git switch main && git pull && git tag v1.2.3 && git push origin v1.2.3`.

The `release` workflow stops at once if the tag and `__version__` differ; otherwise it runs the
tests, builds and smoke-tests one executable per system, attaches them to a GitHub release and
publishes the package to PyPI. The `pages` workflow deploys the browser version from the same tag.

## Licence

[MIT](LICENSE), provided as is, without warranty.
