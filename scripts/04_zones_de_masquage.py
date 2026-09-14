# -*- coding: utf-8 -*-
"""
Calcule, pour chaque carte de chaque maquette, la ZONE DE MASQUAGE : la partie
de la carte occupee par du contenu simule, qu'un visuel opaque devra recouvrir
integralement si l'on garde la maquette complete en arriere-plan.

Ce qui reste visible (et donc ne se reconstruit pas) :
  - le libelle en haut a gauche de la carte (KPI_01, VISUEL_03, ...)
  - la pastille ronde a icone
  - le petit (i) d'info-bulle

Sortie : donnees/zones_masquage.csv + fonds/apercu_masques/*.svg
"""
import csv
import pathlib
import re

SRC = pathlib.Path("fonds/svg")
APERCU = pathlib.Path("fonds/apercu_masques")
APERCU.mkdir(parents=True, exist_ok=True)

# Cartes a ne pas masquer : leur contenu dessine EST le design definitif.
A_CONSERVER = {
    ("P2", 0, 0), ("P3", 0, 0), ("P4", 0, 0), ("P5", 0, 0),      # barre laterale
    ("P2", 1072, 11), ("P3", 1072, 11), ("P4", 1072, 11), ("P5", 1072, 11),  # panneau
    ("P2", 168, 11), ("P3", 168, 11), ("P4", 168, 11), ("P5", 168, 11),      # bandeau titre
}


def nettoyer(svg):
    return re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)


def nombre(tag, nom):
    m = re.search(rf'{nom}="([-\d.]+)"', tag)
    return float(m.group(1)) if m else None


def cartes(svg):
    trouvees = []
    for m in re.finditer(r'<rect\b[^>]*/>', svg):
        t = m.group(0)
        remplissage = re.search(r'fill="([^"]+)"', t)
        remplissage = remplissage.group(1).lower() if remplissage else ""
        x, y = nombre(t, "x"), nombre(t, "y")
        w, h = nombre(t, "width"), nombre(t, "height")
        if None in (x, y, w, h):
            continue
        if remplissage in ("white", "#fff", "#ffffff") and w > 60 and h > 30:
            trouvees.append((x, y, w, h))
    return trouvees


def zone_masquage(svg, x, y, w, h):
    """Interieur de la carte, prive de la ligne de titre et de la colonne de droite
    ou se trouvent pastille et (i)."""
    droite, bas = x + w, y + h
    bas_titre = y                 # bas de la ligne de libelle a conserver
    bord_droit = droite - 1       # bord gauche du premier objet conserve a droite

    for m in re.finditer(r"<text\b[^>]*>", svg):
        t = m.group(0)
        tx, ty, fs = nombre(t, "x"), nombre(t, "y"), nombre(t, "font-size")
        if tx is None or not (x <= tx <= droite and y <= ty <= bas):
            continue
        debut = 'text-anchor="start"' in t
        # Le libelle de carte : ancre a gauche, dans les 30 premiers pixels.
        # 30 et non 24 : les titres VISUEL_xx sont poses plus bas que les
        # libelles KPI_xx, et doivent rester visibles eux aussi.
        if debut and ty - y <= 30:
            bas_titre = max(bas_titre, ty + (fs or 9) * 0.45 + 4)

    for m in re.finditer(r"<circle\b[^>]*/>", svg):
        t = m.group(0)
        cx, cy, r = nombre(t, "cx"), nombre(t, "cy"), nombre(t, "r")
        if cx is None or not (x <= cx <= droite and y <= cy <= bas):
            continue
        # Pastille (r >= 10) et picto d'info-bulle (r = 4,5) loges dans la
        # colonne de droite. Le seuil est calcule depuis le bord droit, et non
        # en proportion de la largeur : sur les cartes larges, le (i) pose a
        # cote du titre retrecissait le masque de moitie.
        if (r >= 10 or abs(r - 4.5) < 0.01) and cx > droite - 42:
            bord_droit = min(bord_droit, cx - r - 2)

    # Cartes-compteurs de 48 px : pastille et libelle a gauche, valeur calee a
    # droite. Seule la valeur se reconstruit, le reste est deja bon.
    if h <= 50:
        return x + 78, y + 1, round(w - 80), round(h - 2)

    mx = x + 1
    my = max(y + 1, round(bas_titre) + 1)
    return mx, my, round(bord_droit - mx), round(bas - 1 - my)


lignes = []
for chemin in sorted(SRC.glob("P*.svg")):
    page = chemin.stem
    if page == "P1":
        continue  # page de garde : aucun contenu simule a masquer
    svg = nettoyer(chemin.read_text(encoding="utf-8"))
    masques = []
    for (x, y, w, h) in sorted(cartes(svg), key=lambda c: (round(c[1] / 5), c[0])):
        if (page, int(x), int(y)) in A_CONSERVER:
            continue
        mx, my, mw, mh = zone_masquage(svg, x, y, w, h)
        if mw < 20 or mh < 10:
            continue
        masques.append((mx, my, mw, mh))
        lignes.append([page, f"{x:g}", f"{y:g}", f"{w:g}", f"{h:g}",
                       f"{mx:g}", f"{my:g}", f"{mw:g}", f"{mh:g}"])

    apercu = [svg.rstrip()[:-len("</svg>")]]
    for (mx, my, mw, mh) in masques:
        apercu.append(
            f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" '
            f'fill="#D9534F" fill-opacity="0.42" stroke="#D9534F" stroke-width="1"/>'
        )
    apercu.append("</svg>")
    (APERCU / f"{page}.svg").write_text("\n".join(apercu), encoding="utf-8")
    print(f"  {page} : {len(masques)} zones a masquer")

with open("donnees/zones_masquage.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Page", "Carte_X", "Carte_Y", "Carte_L", "Carte_H",
                "Masque_X", "Masque_Y", "Masque_L", "Masque_H"])
    w.writerows(lignes)
print(f"\n  donnees/zones_masquage.csv : {len(lignes)} lignes")
