# CLAUDE.md : atelier salle de bains Morieux

Projet de Samuel (Boulogne-sur-Mer) : aménagement de la salle de bains de l'étage, sous rampant, à partir du permis de construire. Application web d'une seule page, plan 2D coté et maquette 3D synchronisés, versions d'aménagement comparables, achats, budget, murs à construire et réseaux.

- Site publié : https://masuel254.github.io/sdb/ (GitHub Pages, branche `main`, racine)
- Dépôt : `masuel254/sdb`

## À lire avant de modifier

1. `docs/ARCHITECTURE.md` : structure du code, modèle de données, repère des cotes, fonctions clés.
2. `docs/DECISIONS.md` : ce que Samuel a validé ou refusé, version par version. **Ne pas revenir sur une décision listée sans qu'il le demande.**
3. `docs/HISTORIQUE.md` : toutes ses demandes et les réponses, dans l'ordre.

## Règles de travail (demandées par Samuel)

- Répondre en français, ton direct et concis, sans tirets cadratins ni formules toutes faites. Contredire franchement quand une demande est une mauvaise idée, en expliquant pourquoi et en proposant mieux.
- Il travaille surtout **sur iPhone** : tout doit être utilisable au doigt, sans défilement horizontal, avec des cibles d'au moins 44 px.
- Après chaque modification : **construire, tester, pousser** (`main`), il consulte le site directement. Il dit souvent « pousse ».
- Réfléchir en artisan : cotes réalistes, passages, ouvertures de tiroirs, hauteurs sous rampant, normes (NF C 15-100, volumes de douche), faisabilité. Vérifier les conflits avant de livrer.
- Ne jamais inventer une cote existante : les relevés sont dans `docs/ARCHITECTURE.md` (section « La pièce »).

## Boucle de travail

```bash
# 1. modifier la source unique
$EDITOR src/sdb.html            # styles + HTML + script de l'application

# 2. augmenter APP_VERSION et ajouter une entrée en tête de CHANGELOG (dans src/sdb.html)

# 3. vérifier et construire
./tools/check.sh                # syntaxe JS (node)
python3 tools/build.py          # régénère index.html et version.json

# 4. tester
python3 tests/smoke.py          # bureau : erreurs JS + conflits du plan + captures dans tests/out/
python3 tests/smoke.py --mobile # iPhone 390 px

# 5. publier
git add -A && git commit -m "vX.Y.Z : ..." && git push
```

Ne jamais éditer `index.html` à la main : il est généré. `APP_VERSION` (dans `src/sdb.html`) et `version.json` doivent avoir la même version, sinon la mise à jour automatique ne se déclenche pas chez Samuel.

Tests : `pip install playwright` puis `playwright install chromium`. Les tests servent three.js depuis `tests/vendor/` (pas de réseau). Pour un rendu 3D en headless : Chromium avec `--use-gl=swiftshader`.

## Points d'attention techniques

- three.js r128 en UMD depuis cdnjs, aucune autre dépendance, pas de build JS.
- État du plan dans `localStorage` (`sdb-morieux-v8`), interface dans `sdb-ui`, budget dans `sdb-budget`, pad 3D dans `sdb-pad`. Une version non modifiée (`S.edited` faux) se recharge depuis `PRESETS` au démarrage : modifier un preset suffit pour que Samuel voie le changement.
- Les versions v4 et v5 sont **dérivées** de la v3 par code (`PRESETS.sansbalneo4={...PRESETS.sansbalneo3,...}`) : une modification de la v3 se propage. Vérifier les trois après chaque changement de la v3.
- Toute nouvelle construction doit apparaître dans `constructions()` (onglet Murs, cotes d'implantation), `shopping()` (achats, carrelage) et, si elle touche un réseau, `netPoints()`.
- Textures : `img/tex-*.jpg` (une image = 1,20 m de mur ou de sol, sauf marbre 1,80 × 1,20 et béton 1,60 × 1,60 via `SPAN`). Le dépôt est public : la photo du plan de permis reste dans le projet claude.ai, ne pas la committer.
