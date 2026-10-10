# Salle de bains de l'étage, maison Morieux

Atelier d'aménagement en ligne : plan 2D coté à l'échelle 1/50, éditable à la souris ou au doigt, et maquette 3D qui suit chaque modification. Chaque piste d'optimisation est enregistrée comme une version que l'on peut rappeler d'un clic, comparer et partager.

## Versions

| Version | Idée | Points clés |
|---|---|---|
| **Actuel** | État relevé le 10/10/2026 | Baignoire 170 × 75 dans son socle au pignon, douche maçonnée 147 × 108, double vasque 120 × 60, radiateur sous le Velux, porte battante |
| **Balnéo** | Ambiance pierre claire, chêne, noir mat | Baignoire balnéo duo 185 × 90 sous le Velux avec tablier, douche à l'italienne à verrière et niche, vasque simple, porte à galandage dans un doublage pleine longueur |

Le détail de chaque version (ce qui change et pourquoi, palette de matériaux) s'affiche sur la page sous le plan.

## La pièce

- Surface utile 11,01 m² (8,58 m² sous 1,80 m de hauteur et plus), d'après le permis TECCI d'avril 2005.
- 3,49 × 3,00 m, plus une niche de 0,60 × 0,97 m côté porte.
- Mur nain 93 cm, 1,80 m atteint à 72 cm du mur nain, plafond 2,45 m.
- Velux dans une niche de 107 × 110, à 95 cm du mur du rangement.

### Repère des cotes

- **X** se mesure depuis le mur nain (0) vers la chambre 2 (3,49).
- **Y** se mesure depuis le mur du rangement (0) vers le pignon (3,00).
- La rotation d'un élément indique le mur contre lequel se trouve son dos.

## Utiliser la page

- Cliquer un élément pour le sélectionner, le glisser pour le déplacer (pas de 5 cm).
- Ajustement fin au clavier : flèches = 1 cm, Maj + flèches = 10 cm, R = tourner, Suppr = supprimer.
- Les dimensions exactes se saisissent dans le panneau « Élément sélectionné ».
- Le panneau « Contrôles » signale les chevauchements, les passages trop étroits (moins de 60 cm), les hauteurs insuffisantes sous le rampant et les contraintes de porte.
- « Copier ma configuration » produit un texte à coller dans la conversation avec Claude pour une analyse ou une nouvelle variante.

Les modifications sont gardées dans le navigateur de chaque visiteur. Elles ne modifient pas le site : pour figer une proposition, il faut l'ajouter comme nouvelle version.

## Photos des matériaux

Chaque matériau de la palette cherche une photo dans `img/` au nom affiché sous sa pastille, par exemple `img/balneo-sol.jpg`. Si la photo n'existe pas, un aperçu peint de la matière s'affiche à la place. La liste des noms attendus est dans `img/LISEZMOI.md`.

Le dépôt étant public, utilisez vos propres photos ou des images libres de droits plutôt que des visuels de fabricants.

## Publier avec GitHub Pages

1. Déposer `index.html`, `README.md` et le dossier `img/` à la racine du dépôt.
2. Dans le dépôt : Settings, puis Pages, source « Deploy from a branch », branche `main`, dossier `/ (root)`.
3. La page est servie à l'adresse `https://<utilisateur>.github.io/<dépôt>/` après une à deux minutes.

La page charge three.js et les polices Google en ligne : une connexion internet est nécessaire.

## Points à valider avant travaux

- Largeur totale de la pièce à hauteur du socle actuel : la somme socle + douche donne 3,51 m contre 3,49 m au permis.
- Possibilité de décaisser le plancher pour une douche de plain-pied à l'étage, sinon receveur extra-plat.
- Trappe d'accès au moteur de la balnéo et circuit électrique dédié avec différentiel 30 mA.
- Prises et interrupteurs à plus de 60 cm des bords de baignoire et de douche (NF C 15-100).
