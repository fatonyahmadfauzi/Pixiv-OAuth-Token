#!/usr/bin/env python3
"""Local static server with clean-URL rewrite support.

Examples:
  python scripts/run_local_web_server.py
  python scripts/run_local_web_server.py --host 127.0.0.1 --port 4173
"""

from __future__ import annotations

import argparse
import posixpath
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


class CleanURLRequestHandler(SimpleHTTPRequestHandler):
    """Serve static files and map extensionless paths to .html files."""

    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def translate_path(self, path: str) -> str:
        raw_path = urlsplit(path).path
        normalized = posixpath.normpath(unquote(raw_path))
        parts = [p for p in normalized.split("/") if p and p not in {".", ".."}]

        candidate = Path(self.directory or ".")
        for part in parts:
            candidate /= part

        # 1) Serve files as-is when present.
        if candidate.is_file():
            return str(candidate)

        # 2) Resolve extensionless clean routes (e.g. /downloads -> /downloads.html).
        if not raw_path.endswith("/") and Path(candidate.name).suffix == "":
            html_candidate = candidate.with_suffix(".html")
            if html_candidate.is_file():
                return str(html_candidate)

        # 3) Directory index.
        if candidate.is_dir():
            index_candidate = candidate / "index.html"
            if index_candidate.is_file():
                return str(index_candidate)

        # 4) Optional 404.html fallback.
        not_found = Path(self.directory or ".") / "404.html"
        if not_found.is_file():
            return str(not_found)

        return str(candidate)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local static server with clean URL rewrites")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=4173, help="Port to bind (default: 4173)")
    parser.add_argument(
        "--root",
        default="web/public",
        help="Document root directory (default: web/public)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Document root not found: {root}")

    handler = lambda *h_args, **h_kwargs: CleanURLRequestHandler(  # noqa: E731
        *h_args,
        directory=str(root),
        **h_kwargs,
    )

    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving {root} on http://{args.host}:{args.port} (clean URL enabled)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
