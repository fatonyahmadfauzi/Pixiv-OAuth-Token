"""
add_debug_coverage.py  — v2
Automatically inserts debug_print() / self.debug() at the start of every
function/method that is currently missing a debug call.

Handles:
  - Multi-line def signatures  (def foo(\n    arg,\n) -> None:)
  - Single-line docstrings & multi-line docstrings
  - Nested functions / lambdas
  - Skips infrastructure helpers

Usage:
    python scripts/add_debug_coverage.py
"""
import re
import ast
import sys
from pathlib import Path

# ── config ───────────────────────────────────────────────────────────────────

SKIP_NAMES = {
    # CLI debug infrastructure (would be recursive / noisy)
    "_dbg_msg", "debug_print", "colorize",
    # GUI
    "__init__", "__str__", "__repr__", "__del__",
    # trivial helpers
    "_nl", "supported_langs_display", "get_lang",
    # lambdas / inner stubs picked up by regex
    "worker", "done", "fail",
}

# ── helpers ───────────────────────────────────────────────────────────────────

def find_def_end(lines: list[str], def_idx: int) -> int:
    """
    Return the 0-based index of the line that ends the def signature
    (the line containing the closing ':' of the def statement).
    Handles multi-line signatures.
    """
    i = def_idx
    depth = 0
    while i < len(lines):
        for ch in lines[i]:
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
        stripped = lines[i].rstrip()
        # The def ends when parens are balanced AND the line ends with ':'
        if depth == 0 and stripped.endswith(':'):
            return i
        i += 1
    return def_idx  # fallback


def find_body_insert_idx(lines: list[str], def_idx: int) -> int:
    """
    Return the 0-based line index where we should insert the debug statement
    (after the def signature and any leading docstring, before the first
    real statement).
    """
    # First, find where the def header ends (may span multiple lines)
    sig_end = find_def_end(lines, def_idx)
    i = sig_end + 1  # first line of the body

    n = len(lines)

    # Skip blank lines
    while i < n and lines[i].strip() == "":
        i += 1

    if i >= n:
        return i

    stripped = lines[i].strip()

    # Check for docstring
    for q in ('"""', "'''"):
        if stripped.startswith(q):
            rest = stripped[len(q):]
            # Single-line docstring: """..."""
            if rest.endswith(q) and len(rest) >= len(q):
                return i + 1  # insert after single-line docstring
            # Multi-line: scan until closing quotes
            i += 1
            while i < n:
                if q in lines[i]:
                    return i + 1  # insert after closing docstring line
                i += 1
            return i

    return i  # no docstring — insert here


def has_debug(lines: list[str], def_idx: int, window: int = 12) -> bool:
    """Return True if any of the next `window` lines after def contains a debug call."""
    for j in range(def_idx + 1, min(def_idx + window, len(lines))):
        l = lines[j]
        if "debug_print(" in l or "self.debug(" in l or "_dbg_msg(" in l:
            return True
    return False


def get_body_indent(lines: list[str], def_idx: int) -> str:
    """Derive the expected body indent from the def line indent + 4 spaces."""
    def_line = lines[def_idx]
    leading = len(def_line) - len(def_line.lstrip())
    return " " * (leading + 4)


# ── patch function ────────────────────────────────────────────────────────────

DEF_RE = re.compile(r'^( *)def (\w+)\s*\(')

def patch_file(path: Path, is_gui: bool) -> int:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    insertions = []  # (insert_before_0based_idx, new_line_str)

    for i, line in enumerate(lines):
        m = DEF_RE.match(line)
        if not m:
            continue
        name = m.group(2)
        if name in SKIP_NAMES:
            continue
        if has_debug(lines, i):
            continue

        insert_at = find_body_insert_idx(lines, i)
        indent = get_body_indent(lines, i)

        is_method = bool(re.search(r"def\s+\w+\s*\(\s*self", line))

        if is_gui and is_method:
            dbg = f'{indent}self.debug(f"[FUNC] {name}() called")\n'
        else:
            dbg = f'{indent}debug_print(f"[FUNC] {name}() called")\n'

        insertions.append((insert_at, dbg))

    # Apply in reverse so indices remain valid
    for insert_at, dbg in sorted(insertions, key=lambda x: x[0], reverse=True):
        lines.insert(insert_at, dbg)

    path.write_text("".join(lines), encoding="utf-8")
    return len(insertions)


# ── main ─────────────────────────────────────────────────────────────────────

root = Path(__file__).parent.parent

cli_path = root / "app" / "pixiv_login.py"
gui_path = root / "app" / "pixiv_login_gui.py"

print(f"Patching CLI: {cli_path.name}")
n_cli = patch_file(cli_path, is_gui=False)
print(f"  → {n_cli} debug_print() calls inserted")

print(f"Patching GUI: {gui_path.name}")
n_gui = patch_file(gui_path, is_gui=True)
print(f"  → {n_gui} self.debug() / debug_print() calls inserted")

print("\nSyntax check...")
ok = True
for p in (cli_path, gui_path):
    try:
        ast.parse(p.read_text(encoding="utf-8"))
        print(f"  ✓ {p.name}")
    except SyntaxError as e:
        print(f"  ✗ {p.name}  →  {e}")
        ok = False

if ok:
    print(f"\n✓ Done. {n_cli + n_gui} debug calls added total.")
else:
    print("\n✗ Syntax error(s) detected — please revert and check.")

sys.exit(0 if ok else 1)
