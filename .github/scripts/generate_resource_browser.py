#!/usr/bin/env python3
"""Generate a folder browser for files produced by the Pages build."""

import html
import sys
from pathlib import Path
from urllib.parse import quote


def render_directory(directory: Path, root: Path) -> str:
    items = []
    for path in sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.casefold(), p.name)):
        if path.is_symlink():
            raise ValueError(f"Unexpected symlink in Pages output: {path}")
        name = html.escape(path.name)
        if path.is_dir():
            contents = render_directory(path, root)
            if contents:
                directory_id = html.escape(path.relative_to(root).as_posix(), quote=True)
                items.append(f'<li><details id="{directory_id}"><summary>{name}/</summary><ul>{contents}</ul></details></li>')
        elif path.is_file():
            url = html.escape(quote(path.relative_to(root).as_posix(), safe="/"), quote=True)
            items.append(f'<li><a href="{url}">{name}</a></li>')
    return "\n".join(items)


def generate(root: Path) -> None:
    if not root.is_dir():
        raise ValueError(f"Pages output directory does not exist: {root}")
    output = root / "resource-browser.html"
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite an existing page: {output}")
    contents = render_directory(root, root)
    output.write_text(
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Browse resources by folder</title>'
        '<link rel="stylesheet" href="assets/css/style.css"></head><body>'
        '<header class="page-header"><h1>Browse resources by folder</h1></header>'
        '<main class="main-content"><p><a href="./">Home</a></p>'
        '<p>Files published by the latest site build, organized by folder.</p>'
        f'<ul>{contents}</ul></main>'
        '<script>'
        'function openFolder() {'
        '  if (!location.hash) return;'
        '  var id = new URLSearchParams("path=" + location.hash.slice(1)).get("path");'
        '  var target = document.getElementById(id);'
        '  for (var node = target; node; node = node.parentElement) {'
        '    if (node.tagName === "DETAILS") node.open = true;'
        '  }'
        '  if (target) target.scrollIntoView();'
        '}'
        'window.addEventListener("hashchange", openFolder);'
        'openFolder();'
        '</script></body></html>\n',
        encoding="utf-8",
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: generate_resource_browser.py PAGES_OUTPUT_DIRECTORY")
    generate(Path(sys.argv[1]))
