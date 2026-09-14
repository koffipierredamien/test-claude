# -*- coding: utf-8 -*-
"""
Genere les fonds de page "propres" a partir des maquettes SVG.

Principe : la maquette contient a la fois la STRUCTURE (canevas, cartes,
separateurs) et le CONTENU simule (textes, barres, courbes, lignes de
tableau). Seule la structure doit rester en arriere-plan dans Power BI :
tout le contenu est reconstruit avec de vrais visuels par-dessus.

Sortie : fonds/svg_propres/*.svg
"""
import re
import pathlib

SRC = pathlib.Path("fonds/svg")
DST = pathlib.Path("fonds/svg_propres")
DST.mkdir(parents=True, exist_ok=True)

ENTETE = (
    '<svg width="1280" height="720" viewBox="0 0 1280 720" '
    'xmlns="http://www.w3.org/2000/svg">\n'
)


def sans_metadonnees(svg: str) -> str:
    return re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)


def fond_page_garde(svg: str) -> str:
    """P1 : page de garde. Le decor (degrade, carte, pastilles) fait partie
    du design et doit rester. On ne retire que les textes."""
    svg = re.sub(r"<text\b.*?</text>", "", svg, flags=re.S)
    return svg


def fond_page_standard(svg: str) -> str:
    """P2 a P5 : on ne conserve que le canevas, les cartes blanches et les
    filets de separation."""
    garde = []
    for m in re.finditer(r"<rect\b[^>]*/>", svg):
        balise = m.group(0)
        largeur = float(re.search(r'width="([\d.]+)"', balise).group(1))
        hauteur = float(re.search(r'height="([\d.]+)"', balise).group(1))
        remplissage = re.search(r'fill="([^"]+)"', balise)
        remplissage = remplissage.group(1) if remplissage else ""
        canevas = largeur == 1280 and hauteur == 720
        carte = remplissage.lower() in ("white", "#fff", "#ffffff")
        if canevas or (carte and largeur > 60 and hauteur > 30):
            garde.append(balise)
    for m in re.finditer(r"<line\b[^>]*/>", svg):
        if "#E5E7EB" in m.group(0):
            garde.append(m.group(0))
    return ENTETE + "\n".join(garde) + "\n</svg>"


for chemin in sorted(SRC.glob("P*.svg")):
    brut = sans_metadonnees(chemin.read_text(encoding="utf-8"))
    propre = fond_page_garde(brut) if chemin.stem == "P1" else fond_page_standard(brut)
    (DST / chemin.name).write_text(propre, encoding="utf-8")
    print(f"{chemin.name} -> {len(propre):>6} octets")
