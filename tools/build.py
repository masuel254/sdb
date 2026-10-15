#!/usr/bin/env python3
"""Construit index.html (page GitHub Pages) et version.json à partir de src/.

src/head.html : début du document (doctype, meta, styles de base)
src/sdb.html  : l'application (styles + HTML + script), source unique à modifier
"""
import json, re, sys, datetime, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "src/sdb.html").read_text(encoding="utf-8")
head = (root / "src/head.html").read_text(encoding="utf-8")
i = src.index("<style>"); j = src.index("</style>") + 8
(root / "index.html").write_text(head + src[:j] + "\n</head>\n<body>\n" + src[j:] + "\n</body>\n</html>\n", encoding="utf-8")
ver = re.search(r'const APP_VERSION="([^"]+)"', src).group(1)
m = re.search(r'const CHANGELOG=\[\["([^"]+)","([^"]+)","((?:[^"\\]|\\.)*)"\]', src)
note = m.group(3).replace("\\'", "'")[:120] if m else ""
(root / "version.json").write_text(json.dumps({"version": ver, "date": datetime.date.today().isoformat(), "notes": note}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"index.html et version.json construits (v{ver})")
