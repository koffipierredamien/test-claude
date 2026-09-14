# Tableau de bord Power BI — montage sur maquettes SVG

Reconstruction d'un tableau de bord de 5 pages à partir des seules maquettes
SVG : jeu de données complet, modèle, mesures DAX, thème et guide de montage.

## Contenu

```
fonds/svg/               maquettes SVG d'origine (1280 × 720)
fonds/reference/         maquettes rendues en PNG — fond de la VARIANTE A
fonds/svg_propres/       fonds nettoyés : structure seule, sans contenu simulé
fonds/png/               les mêmes en PNG 2560 × 1440 — fond de la VARIANTE B
fonds/apercu_masques/    zones à masquer, surlignées (variante A)
donnees/            11 fichiers CSV (modèle en étoile)
theme/              thème Power BI reprenant la palette de la maquette
scripts/            génération des fonds et des données (Python 3, sans dépendance)
docs/               modèle de données · mesures DAX · guide de montage
```

## Par où commencer

1. [`docs/01-modele-de-donnees.md`](docs/01-modele-de-donnees.md) — le schéma et les relations
2. [`docs/02-mesures-dax.md`](docs/02-mesures-dax.md) — les mesures, prêtes à copier
3. [`docs/03-guide-montage.md`](docs/03-guide-montage.md) — le montage, page par page
4. [`docs/04-variante-fond-complet.md`](docs/04-variante-fond-complet.md) — les zones de masquage

## Deux variantes d'arrière-plan

| | Variante A — maquette complète | Variante B — fond nettoyé |
|---|---|---|
| Image de fond | `fonds/reference/` | `fonds/png/` |
| Décor (barre latérale, libellés, icônes, titres) | déjà peint, ~120 objets en moins | à reconstruire |
| Chaque zone dynamique | doit être **masquée** par un rectangle blanc | rien à masquer |
| Visuels | fond transparent, titre désactivé | fond transparent |
| Objets par page | ~30 visuels + ~12 rectangles | ~45 visuels |

Les deux partagent **exactement le même modèle, les mêmes mesures et les mêmes
visuels**. Passer de l'une à l'autre revient à changer l'image de fond et à
ajouter ou retirer les rectangles de masquage.

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
python3 scripts/01_generer_fonds.py              # fonds/svg_propres/
./scripts/02_exporter_png.sh                     # fonds/png/  (nécessite Chromium)
python3 scripts/03_generer_donnees.py            # donnees/
python3 scripts/04_zones_de_masquage.py          # zones de masquage + aperçus
python3 scripts/05_doc_variante_fond_complet.py  # docs/04-...md
./scripts/02_exporter_png.sh fonds/apercu_masques fonds/apercu_masques_png
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
