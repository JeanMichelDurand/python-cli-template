"""Turns this template into a new project, once, right after "Use this template":

    python3 rename.py csv2xlsx --description "Convert CSV files into formatted Excel workbooks"

Renames the package folder, and replaces the package name, the repository name and the
one-line description in every text file. It also removes the template's own section from
README.md and deletes this script. It says whether the name is still free on PyPI. Run it on
a clean checkout: `git diff` then shows exactly what it changed.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE, REPO = "myproject", "python-cli-template"
DESCRIPTION = "One line saying what the tool does"
SKIP_DIRS = {".git", ".venv", "build", "dist", "site", "__pycache__", ".pytest_cache", ".ruff_cache"}
TEXT = {".py", ".md", ".toml", ".ini", ".yml", ".yaml", ".json", ".html", ".txt", ""}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("name", help="the package, command and repository name: lowercase, digits, underscores")
    ap.add_argument("--description", help="one line saying what the tool does (pyproject, README, web page)")
    args = ap.parse_args(argv)
    if not re.fullmatch(r"[a-z][a-z0-9]*(_[a-z0-9]+)*", args.name):
        print(f"{args.name!r}: use lowercase letters, digits and single underscores, starting with a letter")
        return 1
    if not (HERE / "src" / PACKAGE).is_dir():
        print(f"src/{PACKAGE} not found: this project was already renamed")
        return 1
    print(_pypi_status(args.name))

    replacements = [(REPO, args.name), (PACKAGE, args.name)]      # the repository name first: it is longer
    if args.description:
        replacements.append((DESCRIPTION, args.description.rstrip(".")))
    changed = 0
    for path in _text_files():
        text = path.read_text(encoding="utf-8")
        new = text
        if path.name == "README.md":
            new = re.sub(r"<!-- template:start -->.*?<!-- template:end -->\n", "", new, flags=re.S)
        for old, value in replacements:
            new = new.replace(old, value)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
    (HERE / "src" / PACKAGE).rename(HERE / "src" / args.name)
    Path(__file__).unlink()
    print(f"Renamed to {args.name}: {changed} files changed, src/{args.name}/, rename.py removed.")
    print("Next: python3 install.py dev, run the tests, commit, then go through SETUP.md.")
    return 0


def _text_files():
    me = Path(__file__).resolve()
    for path in sorted(HERE.rglob("*")):
        rel = path.relative_to(HERE)
        if (path.is_file() and path.resolve() != me and path.suffix in TEXT
                and not SKIP_DIRS.intersection(rel.parts) and not rel.name.endswith(".egg-info")):
            yield path


def _pypi_status(name: str) -> str:
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=10) as r:
            json.load(r)
        return f"Warning: {name} is already taken on PyPI: the pypi job will fail unless you pick another name."
    except urllib.error.HTTPError as e:
        return f"{name} is free on PyPI." if e.code == 404 else f"PyPI check skipped (HTTP {e.code})."
    except (OSError, ValueError):
        return "PyPI check skipped (offline)."


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
