# Tableau de bord Power BI — montage sur maquettes SVG

Reconstruction d'un tableau de bord de 5 pages à partir des seules maquettes
SVG : jeu de données complet, modèle, mesures DAX, thème et guide de montage.

## Contenu

```
fonds/svg/          maquettes SVG d'origine (1280 × 720)
fonds/reference/    maquettes rendues en PNG — calque de repérage
fonds/svg_propres/  fonds nettoyés : structure seule, sans contenu simulé
fonds/png/          les mêmes en PNG 2560 × 1440 → arrière-plans Power BI
donnees/            11 fichiers CSV (modèle en étoile)
theme/              thème Power BI reprenant la palette de la maquette
scripts/            génération des fonds et des données (Python 3, sans dépendance)
docs/               modèle de données · mesures DAX · guide de montage
```

## Par où commencer

1. [`docs/01-modele-de-donnees.md`](docs/01-modele-de-donnees.md) — le schéma et les relations
2. [`docs/02-mesures-dax.md`](docs/02-mesures-dax.md) — les mesures, prêtes à copier
3. [`docs/03-guide-montage.md`](docs/03-guide-montage.md) — le montage, page par page

## Les 5 pages

| Page | Fond | Rôle |
|---|---|---|
| 1 | `P1.png` | Garde et sommaire — navigation |
| 2 | `P2.png` | Capacité et charge — 7 KPI, 3 visuels, matrice mensuelle |
| 3 | `P3.png` | Ressources — 4 KPI, anneau, histogramme empilé, table |
| 4 | `P4.png` | Demandes et portefeuille — 11 KPI, 3 visuels, 2 tables Top N |
| 5 | `P5.png` | Projets de maintenance — même trame que la page 4 |

## Deux points à connaître avant de commencer

**Power BI n'accepte pas le SVG en arrière-plan de page** (PNG, JPG, BMP, GIF
seulement). D'où l'export PNG 2× fourni dans `fonds/png/`.

**La maquette ne peut pas servir de fond telle quelle** : elle contient déjà
des faux graphes, qui resteraient visibles derrière les vrais visuels. Les
fonds de `fonds/png/` ne conservent que la structure — cartes, filets,
panneaux. Tout le reste se reconstruit par-dessus.

## Régénérer

```bash
python3 scripts/01_generer_fonds.py     # fonds/svg_propres/
./scripts/02_exporter_png.sh            # fonds/png/  (nécessite Chromium)
python3 scripts/03_generer_donnees.py   # donnees/
```

Le générateur de données est déterministe (`random.seed(20260908)`) : deux
exécutions produisent des fichiers identiques.

## À propos des données

Les libellés de la maquette sont symboliques. Le scénario retenu — pilotage de
la capacité et du portefeuille d'une DSI — découle du vocabulaire visible
(*Tribu*, *Squad*, *JH*, *Externe/Interne*, *FTE*, *Portfolio*, budget K€).

Les données reproduisent les **ordres de grandeur et les formes** de la
maquette — la coupure d'août, la décroissance par tribu, la répartition
externes/internes — sans chercher à retomber sur les valeurs exactes, qui sont
elles aussi des remplissages.

Date de référence : **08/09/2026**. Réalisé jusqu'au 31/08/2026, planifié
au-delà.
