#!/usr/bin/env bash
# Vérifie la syntaxe du script de l'application (node requis).
set -e
cd "$(dirname "$0")/.."
python3 -c "import re;s=open('src/sdb.html',encoding='utf-8').read();js=re.findall(r'<script>(.*?)</script>',s,re.S)[-1];open('/tmp/sdb_check.js','w',encoding='utf-8').write(js)"
node --check /tmp/sdb_check.js && echo "Syntaxe JS OK"
grep -o 'const APP_VERSION="[^"]*"' src/sdb.html
