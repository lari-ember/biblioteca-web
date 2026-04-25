#!/usr/bin/env python3
"""Sync project version from CHANGELOG.md.

Reads the first ``## [X.Y.Z]`` entry in CHANGELOG.md and writes that
version to every file that declares it:

  - ``app/__init__.py``  → ``__version__ = "X.Y.Z"``
  - ``pyproject.toml``   → ``version = "X.Y.Z"``

Usage
-----
Run manually (applies changes):
    python scripts/bump_version.py

Check only – exit 1 if any file is out of sync (useful in CI):
    python scripts/bump_version.py --check

The script is also wired as a local pre-commit hook (see
.pre-commit-config.yaml).  When CHANGELOG.md is staged and the version
files need updating, the hook rewrites them and exits 1 so that git
asks the user to ``git add`` the modified files before committing again.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHANGELOG = ROOT / "CHANGELOG.md"
INIT_PY = ROOT / "app" / "__init__.py"
PYPROJECT = ROOT / "pyproject.toml"

_VERSION_HEADER_RE = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_changelog_version() -> str:
    """Return the first semantic version found in CHANGELOG.md."""
    text = CHANGELOG.read_text(encoding="utf-8")
    match = _VERSION_HEADER_RE.search(text)
    if not match:
        raise ValueError(
            "No version header found in CHANGELOG.md.\n"
            "Expected a line like:  ## [1.2.3] - YYYY-MM-DD"
        )
    return match.group(1)


def _rewrite_if_changed(path: Path, new_text: str, check_only: bool) -> bool:
    """Write *new_text* to *path* if it differs; return True when changed."""
    old_text = path.read_text(encoding="utf-8")
    if new_text == old_text:
        return False
    if not check_only:
        path.write_text(new_text, encoding="utf-8")
    return True


def update_init(version: str, check_only: bool) -> bool:
    """Update ``__version__`` in app/__init__.py."""
    text = INIT_PY.read_text(encoding="utf-8")
    new_text = re.sub(
        r'(__version__\s*=\s*")[^"]+(")',
        rf"\g<1>{version}\g<2>",
        text,
    )
    return _rewrite_if_changed(INIT_PY, new_text, check_only)


def update_pyproject(version: str, check_only: bool) -> bool:
    """Update ``version`` in pyproject.toml.

    Also corrects the accidental ``como version = …`` typo if present.
    """
    text = PYPROJECT.read_text(encoding="utf-8")
    # Handle both the standard form and the legacy "como version = …" typo
    # that existed in pyproject.toml before this script was introduced.
    new_text = re.sub(
        r"^(?:como\s+)?version\s*=\s*\"[^\"]+\"",
        f'version = "{version}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    return _rewrite_if_changed(PYPROJECT, new_text, check_only)


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

def main() -> int:
    args = sys.argv[1:]
    # Strip staged-file arguments passed by pre-commit (we don't need them).
    check_only = "--check" in args

    try:
        version = read_changelog_version()
    except (FileNotFoundError, ValueError) as exc:
        print(f"[bump_version] ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"[bump_version] version from CHANGELOG.md: {version}")

    action_word = "Would update" if check_only else "Updated"
    changed = False

    if update_init(version, check_only):
        changed = True
        print(f"[bump_version] {action_word} app/__init__.py → {version}")

    if update_pyproject(version, check_only):
        changed = True
        print(f"[bump_version] {action_word} pyproject.toml → {version}")

    if not changed:
        print(f"[bump_version] All files already at {version} — nothing to do.")
        return 0

    if check_only:
        print(
            "[bump_version] Version mismatch detected. "
            "Run  python scripts/bump_version.py  to fix.",
            file=sys.stderr,
        )
        return 1

    # Files were modified by this run.  Signal pre-commit to re-stage them.
    print(
        "[bump_version] Version files updated. "
        "Stage the changes and commit again."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
