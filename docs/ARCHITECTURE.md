# Architecture

## Fichiers

| Chemin | Rôle |
|---|---|
| `src/sdb.html` | **Source unique de l'application** : `<style>`, HTML des panneaux, puis un seul `<script>`. C'est aussi le corps publié comme artefact claude.ai. |
| `src/head.html` | Début du document de la page GitHub (doctype, meta viewport, styles de base). |
| `tools/build.py` | Assemble `index.html` = head + source, et écrit `version.json` depuis `APP_VERSION` et la première entrée de `CHANGELOG`. |
| `tools/check.sh` | Extrait le script et vérifie sa syntaxe avec `node --check`. |
| `tests/smoke.py` | Playwright : toutes les versions × tous les onglets, erreurs JS, conflits, captures. |
| `tests/vendor/three.min.js` | three.js r128 local pour les tests hors ligne. |
| `index.html` | Page publiée (générée, ne pas éditer). |
| `version.json` | Lu par la page au chargement pour proposer la mise à jour. |
| `img/` | Palettes (`mat-*`, `act-*`) et textures 3D (`tex-*`). |
| `docs/` | Cette documentation, les décisions et l'historique. |

Dépendances : three.js r128 (cdnjs, UMD, global `THREE`), polices Google. Rien d'autre.

## La pièce (relevé et permis TECCI d'avril 2005)

- Rectangle 3,49 × 3,00 m, plus une niche d'entrée de 0,60 × 0,97 m côté porte (de x 3,49 à 4,09, y 0 à 0,97).
- Mur nain 93 cm (`S.H0`), 1,80 m atteint à 72 cm du mur nain (`S.L`), plafond plat 2,45 m (`S.P`). Pente = (1,80 − 0,93) / 0,72 ; plafond plat à partir de x ≈ 1,26.
- Velux dans une niche de 107 × 110, de y 0,95 à 2,02 (`VEL`), longueur 1,10 le long de la pente.
- Porte PS 73 : ouverture x 3,27 à 4,00 sur le mur du rangement (`DOOR.o1`, `DOOR.o2`), battante, noire des deux côtés, s'ouvre dans la niche (charnières côté x 4,00). Version galandage : poche de x 2,52 à 3,27 (`DOOR.pk1`) dans un doublage de 10 cm.
- Existant (version Actuel) : baignoire 170 × 75 dans un socle (23 / 11 / 10 / 10), douche maçonnée 147 × 108 entrée 55, double vasque 120 × 60 à 165 du mur nain, miroir 120 × 110, radiateur à eau 70 × 60 × 10 (15 avec supports) sous le Velux, sèche-serviettes électrique 45 × 90.
- Radiateur : sur la chaudière. Sèche-serviettes : **électrique**.

## Repère

- **x** depuis le mur nain (0) vers la chambre 2 (3,49) ; **y** depuis le mur du rangement (0) vers le pignon (3,00). En 3D : X = x, Z = y, Y = hauteur.
- Rotation `r` d'un élément = mur contre lequel est son dos : 0 rangement, 1 chambre 2, 2 pignon, 3 mur nain. `w` est la longueur le long du mur, `d` la profondeur. `fw()`, `fd()` donnent l'emprise en plan ; `loc2plan(it,lx,lz)` convertit une position locale (le long du mur, depuis le mur) en plan.
- Carrelage : `TW()` épaisseur murale (10 mm), `TF()` sol (15 mm). `ceilAt(x)` hauteur sous plafond depuis le sol fini, `rawTop(x)` brut.

## Modèle de données

```js
S = { preset, edited, name, door:"battante"|"galandage"|"applique", style:"beige"|..., skin?:"marbre",
      tile, tw, tf, H0, L, P, items:[ {id, t, lbl?, x, y, r, w, d, ...paramètres propres au type} ] }
```

- `CAT` : catalogue des types (nom, dimensions par défaut). `REQ` : hauteurs minimales sous rampant.
- `PRESETS` : les versions (`actuel`, `balneo`, `sansbalneo`, `sansbalneo2`, `sansbalneo3`, puis `sansbalneo4` et `sansbalneo5` dérivés en code). Chaque preset : `name`, `intro`, `changes[]` (descriptif HTML de l'onglet Matériaux), `mats[]` (palette : image, titre, texte, peinture de secours), `items[]`.
- Types notables :
  - `showerSlope` (douche sous rampant, v3 à v5) : `tab` largeur du muret du mur nain (tablette), `bx1..bx2 / bz1..bz2` banc, `benchBack` banc au fond, `standX` début de la zone debout, `encX/mixX/headX/nicheX` robinetterie et niche le long du faux mur, `walk` entrée sans porte avec muret vitré, `post` poteau de verrière (12 cm, h 2,00), `side`, `door`.
  - `showerNiche` (Balnéo, v1, v2) : douche avec faux mur et muret, `open`, `hand` (douchette banquette).
  - `wallNiche` cloison à niches, `wallPiece` faux mur, `low` banc ou meuble bas (`tiled` maçonné, `hh` hauteur, `drw` tiroirs), `vanity1/2` (`vessel`, `oval`, `col`, `col:"w2"` = texture bois), `towel` (`ladder`, `elec`, `black`), `radiator` (`reuse`).

## Organisation du script (dans l'ordre du fichier)

| Section | Fonctions principales |
|---|---|
| Données | `CAT`, `REQ`, `APP_VERSION`, `CHANGELOG`, `TILES()`, `MAT_B`, `PRESETS`, `VEL`, `DOOR`, `DBL()` |
| État | `load()`, `persist()`, `save()` ; migration des versions non modifiées au démarrage |
| Géométrie | `showerFront`, `details`, `loc2plan`, `trayRect` (bac réel), `interiorRect`, `slope`, `ceilAt`, `veluxX` |
| Contrôles | `drawerZone` (ouverture des tiroirs), `rect`, `inter`, `checks()` (chevauchements, passages < 60 / < 70 cm, carrelage, hauteurs, porte, poche, tiroirs) |
| Plan 2D (SVG, 100 px = 1 m) | `drawStatic`, `sym` (dessin par type), `drawItems` (dont cotes Espace, Implantation, Éléments, Mesurer), zoom et déplacement (`VB`, `applyVB`, `zoomAt`), mode `EDIT` |
| 3D | `buildShell` (murs, sol, pente, porte), `applySkin` (textures v5), `buildFix` (éléments, étiquettes, mesures, réseaux), `HIDE`/`OCC`/`FOLLOW` (murs masqués face caméra), caméra orbitale `cam`/`T`, `pan3`, `walk3`, `turn3`, pad, `VIEWS` |
| Descriptif | `painter`, `drawDesc` (onglet Matériaux) |
| Espace | `measures()` (distances libres, diagonales, Velux), `circulation()` (m² libres), `heightLines` ; sélection d'une mesure `MSEL` |
| Achats | `shopping()` : surfaces de carrelage (intégrale du profil sous pente), fournitures, équipements ; `drawBuy` |
| Réseaux | `netPoints()` (EF, EC, EV, EL, CH, VM avec position, hauteur, normale du mur), `drawNet3D`, `netVis` (masque les points vus de dos, filtre `NETF`), `drawRes` (tableau et règles) |
| Murs | `constructions()` (ouvrages : cotes brutes L, l, H, épaisseur, rectangle d'implantation), `implant()`, `drawMurs` |
| Budget | `PRICE` (prix estimés 2026), `budLines`, `moEst` (heures poste par poste), `bSheet` (saisie au toucher), `drawBud` ; stockage `sdb-budget` |
| Onglets | `setTab` (2D, 3D, 2D+3D, Matériaux, Éléments, Murs, Réseaux, Achats, Budget, Réglages) |
| Mise à jour | `checkUpdate` lit `version.json`, recharge une fois si une version plus récente est publiée |
| Textures | `loadTextures` remplace les textures dessinées par les images `img/tex-*.jpg` |

`refresh(light, shell)` est le point d'entrée après toute modification : contrôles, plan, panneaux, puis 3D (`buildShell` si `shell`, `buildFix` toujours).

## Ajouter une version

1. Dans `PRESETS`, nouvelle clé (copier un preset ou dériver : `PRESETS.x={...PRESETS.sansbalneo4,name:"…",items:PRESETS.sansbalneo4.items.map(...)}` placé avant `const VEL`).
2. `intro`, `changes`, `mats` cohérents avec les éléments.
3. Vérifier : onglet Contrôles sans conflit, Murs, Achats, Budget, Réseaux.
4. Ajouter la ligne dans le tableau des versions du `README.md`.
