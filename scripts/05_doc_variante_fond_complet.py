# -*- coding: utf-8 -*-
"""
Genere docs/04-variante-fond-complet.md a partir des zones calculees par
04_zones_de_masquage.py, en retrouvant le repere (KPI_01, VISUEL_03, ...) de
chaque carte dans le SVG.
"""
import csv
import pathlib
import re

TITRES = {
    "P2": "Page 2 · Capacité et charge",
    "P3": "Page 3 · Ressources",
    "P4": "Page 4 · Demandes et portefeuille",
    "P5": "Page 5 · Projets de maintenance",
}


def num(tag, nom):
    m = re.search(rf'{nom}="([-\d.]+)"', tag)
    return float(m.group(1)) if m else None


def reperes(page):
    """Associe a chaque carte le libelle imprime en haut a gauche."""
    svg = re.sub(r"<metadata>.*?</metadata>", "",
                 pathlib.Path(f"fonds/svg/{page}.svg").read_text(encoding="utf-8"),
                 flags=re.S)
    trouves = []
    for m in re.finditer(r"<text\b[^>]*>", svg):
        t = m.group(0)
        if 'text-anchor="start"' not in t:
            continue
        txt = svg[svg.index(">", m.start()) + 1:svg.index("</text>", m.start())]
        if re.fullmatch(r"(KPI|VISUEL)_\d+", txt):
            trouves.append((num(t, "x"), num(t, "y"), txt))
    return trouves


def repere_de(page, x, y, w, h):
    noms = [txt for (tx, ty, txt) in reperes(page)
            if x <= tx <= x + w and y <= ty <= y + h]
    return " / ".join(noms) if noms else "—"


lignes = list(csv.DictReader(open("donnees/zones_masquage.csv", encoding="utf-8-sig"),
                            delimiter=";"))

SLICERS = {
    "P2": [("FILTRE_01", 87), ("FILTRE_02", 156), ("FILTRE_03", 202),
           ("FILTRE_04", 271), ("FILTRE_05", 317), ("FILTRE_06", 386),
           ("FILTRE_07", 432)],
    "P3": [("FILTRE_02", 87), ("FILTRE_04", 133), ("FILTRE_05", 179),
           ("FILTRE_06", 248), ("FILTRE_07", 294)],
    "P4": [("FILTRE_08", 87), ("FILTRE_09", 133), ("Portfolio", 179),
           ("SECTION_05", 225), ("FILTRE_07", 294), ("FILTRE_10", 340),
           ("FILTRE_11", 409), ("FILTRE_12", 455), ("FILTRE_13", 501)],
    "P5": [("FILTRE_01", 87), ("FILTRE_08", 156), ("FILTRE_09", 202),
           ("FILTRE_06", 271), ("FILTRE_07", 317), ("FILTRE_10", 363)],
}

sortie = ["""# 4 · Variante « maquette complète en arrière-plan »

Cette variante répond à la consigne : **la maquette envoyée reste l'image de
fond, telle quelle**. Les visuels se posent par-dessus.

## Ce que cette approche donne gratuitement

Tout le décor de la maquette est déjà juste, et ne se reconstruit pas :

| Élément | Statut |
|---|---|
| Barre latérale, avec la pastille active déjà bonne page par page | conservé |
| Bandeau de titre `TITRE_0n` / `SOUS_TITRE_0n` | conservé |
| Libellés `KPI_01` → `KPI_30` | conservés |
| Pastilles rondes et leurs icônes | conservées |
| Titres `VISUEL_01` → `VISUEL_13` | conservés |
| Picto ⓘ d'info-bulle | conservé |
| Panneau de filtres : titres de sections, libellés `FILTRE_0n`, filets | conservés |

Sur les 5 pages, cela représente environ **120 objets que vous n'avez pas à
créer**. C'est le gain réel de la consigne.

## La règle, en une phrase

> Tout ce qui reste **doit être recouvert intégralement** par un objet opaque,
> sinon le faux chiffre transparaît derrière le vrai.

## La méthode, en 3 gestes par zone

1. **Insérer → Formes → Rectangle**, posé aux coordonnées du masque ci-dessous.
   Remplissage **blanc uni, transparence 0 %**, **aucune bordure**, **aucune
   ombre**.
2. Clic droit → **Ordre de plan → Mettre à l'arrière-plan**.
3. Poser le vrai visuel par-dessus, **fond transparent** et **titre désactivé**
   (le titre est déjà dans l'image).

> **Pourquoi un rectangle plutôt qu'un visuel opaque ?** Un visuel opaque
> masquerait aussi, mais Power BI redimensionne son fond avec ses marges
> internes&nbsp;: le recouvrement n'est jamais exact au pixel. Le rectangle,
> lui, ne bouge pas. Et il se déplace indépendamment quand vous ajustez le
> visuel.

## Les 4 points de vigilance propres à cette variante

**1 · Le rectangle doit être blanc pur, pas « blanc du thème ».**
Les cartes de la maquette sont en `#FFFFFF`. Si votre rectangle prend une
nuance du thème, un liseré gris apparaîtra au raccord.

**2 · Les listes déroulantes du panneau sont dessinées.**
Chaque segment réel doit se poser **exactement** sur le rectangle dessiné,
sinon on verra deux listes superposées. Coordonnées dans le tableau des
segments, plus bas : toutes en `x = 1081`, `largeur = 172`, `hauteur = 21`.

**3 · Les tableaux dessinés ont un nombre de lignes figé.**
Si votre table réelle affiche moins de lignes que la maquette, les lignes
dessinées réapparaissent en bas. Le masque couvre toute la hauteur de la carte :
ne le rognez pas pour « gagner de la place ».

**4 · La barre latérale ne se masque pas.**
Posez simplement 6 **boutons transparents** sur les entrées dessinées, avec
`Action = Navigation de page`. L'état actif est déjà peint dans chaque image.

---
"""]

for page in ("P2", "P3", "P4", "P5"):
    sortie.append(f"\n## {TITRES[page]}\n")
    sortie.append("### Zones à masquer\n")
    sortie.append("| Repère | Carte (x, y, l × h) | **Masque (x, y, l × h)** |")
    sortie.append("|---|---|---|")
    for r in lignes:
        if r["Page"] != page:
            continue
        x, y = float(r["Carte_X"]), float(r["Carte_Y"])
        w, h = float(r["Carte_L"]), float(r["Carte_H"])
        rep = repere_de(page, x, y, w, h)
        carte = f'{r["Carte_X"]}, {r["Carte_Y"]} · {r["Carte_L"]} × {r["Carte_H"]}'
        masq = f'**{r["Masque_X"]}, {r["Masque_Y"]} · {r["Masque_L"]} × {r["Masque_H"]}**'
        sortie.append(f"| {rep} | {carte} | {masq} |")
    sortie.append("")
    sortie.append("### Segments à poser sur les listes dessinées\n")
    sortie.append("| Libellé imprimé | X | Y | Largeur | Hauteur |")
    sortie.append("|---|---:|---:|---:|---:|")
    for nom, y in SLICERS[page]:
        sortie.append(f"| {nom} | 1081 | {y} | 172 | 21 |")
    sortie.append("")

sortie.append("""
---

## Contrôler le résultat

`fonds/apercu_masques/` contient les 4 maquettes avec les zones de masquage
surlignées en rouge. Gardez l'aperçu de la page ouvert à côté de Power BI :
tout ce qui est rouge doit finir recouvert, tout ce qui ne l'est pas doit
rester visible.

Le test qui tranche : **mettez tous les segments sur une valeur qui ne renvoie
rien**. Si un chiffre de la maquette apparaît, c'est qu'un masque manque ou
qu'il est trop petit.

## Pour la version de comparaison

Les fonds nettoyés restent dans `fonds/png/`. Pour produire la seconde version,
il n'y a rien à remonter : **Fichier → Enregistrer sous**, puis sur chaque page,
remplacez l'image d'arrière-plan et supprimez les rectangles de masquage
(sélection par le volet Sélection → tous les objets nommés `Rectangle`).
Les visuels, eux, ne bougent pas.

Comptez une quinzaine de minutes pour la bascule, une fois la première version
terminée.
""")

pathlib.Path("docs/04-variante-fond-complet.md").write_text(
    "\n".join(sortie), encoding="utf-8")
print("docs/04-variante-fond-complet.md ecrit")
