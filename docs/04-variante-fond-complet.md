# 4 · Variante « maquette complète en arrière-plan »

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


## Page 2 · Capacité et charge

### Zones à masquer

| Repère | Carte (x, y, l × h) | **Masque (x, y, l × h)** |
|---|---|---|
| KPI_01 | 168, 58 · 217 × 76 | **169, 82 · 178 × 51** |
| KPI_02 | 393.7, 58 · 217 × 76 | **394.7, 82 · 178 × 51** |
| KPI_03 | 619.4, 58 · 217 × 76 | **620.4, 82 · 178 × 51** |
| KPI_04 | 845.1, 58 · 217 × 76 | **846.1, 82 · 178 × 51** |
| KPI_05 | 168, 145 · 443 × 75 | **169, 171 · 422 × 48** |
| KPI_06 | 620, 145 · 217 × 75 | **621, 169 · 178 × 50** |
| KPI_07 | 846, 145 · 216 × 75 | **847, 169 · 177 × 50** |
| VISUEL_01 | 168, 231 · 443 × 169 | **169, 267 · 441 × 132** |
| VISUEL_02 | 620, 231 · 442 × 169 | **621, 267 · 440 × 132** |
| VISUEL_03 | 168, 407 · 894 × 303 | **169, 436 · 892 × 273** |

### Segments à poser sur les listes dessinées

| Libellé imprimé | X | Y | Largeur | Hauteur |
|---|---:|---:|---:|---:|
| FILTRE_01 | 1081 | 87 | 172 | 21 |
| FILTRE_02 | 1081 | 156 | 172 | 21 |
| FILTRE_03 | 1081 | 202 | 172 | 21 |
| FILTRE_04 | 1081 | 271 | 172 | 21 |
| FILTRE_05 | 1081 | 317 | 172 | 21 |
| FILTRE_06 | 1081 | 386 | 172 | 21 |
| FILTRE_07 | 1081 | 432 | 172 | 21 |


## Page 3 · Ressources

### Zones à masquer

| Repère | Carte (x, y, l × h) | **Masque (x, y, l × h)** |
|---|---|---|
| KPI_21 | 168, 58 · 217 × 76 | **169, 82 · 178 × 51** |
| KPI_22 | 393.7, 58 · 217 × 76 | **394.7, 82 · 178 × 51** |
| KPI_23 | 619.4, 58 · 217 × 76 | **620.4, 82 · 178 × 51** |
| KPI_24 | 845.1, 58 · 217 × 76 | **846.1, 82 · 178 × 51** |
| VISUEL_09 | 168, 145 · 360 × 268 | **169, 178 · 358 × 234** |
| VISUEL_10 | 537, 145 · 525 × 268 | **538, 178 · 523 × 234** |
| VISUEL_11 | 168, 422 · 894 × 288 | **169, 452 · 892 × 257** |

### Segments à poser sur les listes dessinées

| Libellé imprimé | X | Y | Largeur | Hauteur |
|---|---:|---:|---:|---:|
| FILTRE_02 | 1081 | 87 | 172 | 21 |
| FILTRE_04 | 1081 | 133 | 172 | 21 |
| FILTRE_05 | 1081 | 179 | 172 | 21 |
| FILTRE_06 | 1081 | 248 | 172 | 21 |
| FILTRE_07 | 1081 | 294 | 172 | 21 |


## Page 4 · Demandes et portefeuille

### Zones à masquer

| Repère | Carte (x, y, l × h) | **Masque (x, y, l × h)** |
|---|---|---|
| KPI_08 | 168, 58 · 172.4 × 76 | **169, 82 · 133 × 51** |
| KPI_09 | 348.4, 58 · 172.4 × 76 | **349.4, 82 · 133 × 51** |
| KPI_10 | 528.8, 58 · 172.4 × 76 | **529.8, 82 · 133 × 51** |
| KPI_11 | 709.2, 58 · 172.4 × 76 | **710.2, 82 · 133 × 51** |
| KPI_12 | 889.6, 58 · 172.4 × 76 | **890.6, 82 · 133 × 51** |
| KPI_13 | 168, 145 · 142.3 × 48 | **246, 146 · 62 × 46** |
| KPI_14 | 318.3, 145 · 142.3 × 48 | **396.3, 146 · 62 × 46** |
| KPI_15 | 468.6, 145 · 142.3 × 48 | **546.6, 146 · 62 × 46** |
| KPI_16 | 618.9, 145 · 142.3 × 48 | **696.9, 146 · 62 × 46** |
| KPI_17 / KPI_18 | 769.2, 145 · 142.3 × 48 | **847.2, 146 · 62 × 46** |
| KPI_19 / KPI_20 | 919.5, 145 · 142.3 × 48 | **997.5, 146 · 62 × 46** |
| VISUEL_04 | 168, 205 · 313 × 182 | **169, 236 · 311 × 150** |
| VISUEL_05 | 489, 205 · 314 × 182 | **490, 230 · 312 × 156** |
| VISUEL_06 | 811, 205 · 251 × 182 | **812, 237 · 249 × 149** |
| VISUEL_07 | 168, 397 · 443 × 313 | **169, 423 · 441 × 286** |
| VISUEL_08 | 620, 397 · 442 × 313 | **621, 423 · 440 × 286** |

### Segments à poser sur les listes dessinées

| Libellé imprimé | X | Y | Largeur | Hauteur |
|---|---:|---:|---:|---:|
| FILTRE_08 | 1081 | 87 | 172 | 21 |
| FILTRE_09 | 1081 | 133 | 172 | 21 |
| Portfolio | 1081 | 179 | 172 | 21 |
| SECTION_05 | 1081 | 225 | 172 | 21 |
| FILTRE_07 | 1081 | 294 | 172 | 21 |
| FILTRE_10 | 1081 | 340 | 172 | 21 |
| FILTRE_11 | 1081 | 409 | 172 | 21 |
| FILTRE_12 | 1081 | 455 | 172 | 21 |
| FILTRE_13 | 1081 | 501 | 172 | 21 |


## Page 5 · Projets de maintenance

### Zones à masquer

| Repère | Carte (x, y, l × h) | **Masque (x, y, l × h)** |
|---|---|---|
| KPI_08 | 168, 58 · 172.4 × 76 | **169, 82 · 133 × 51** |
| KPI_25 | 348.4, 58 · 172.4 × 76 | **349.4, 82 · 133 × 51** |
| KPI_26 | 528.8, 58 · 172.4 × 76 | **529.8, 82 · 133 × 51** |
| KPI_11 | 709.2, 58 · 172.4 × 76 | **710.2, 82 · 133 × 51** |
| KPI_12 | 889.6, 58 · 172.4 × 76 | **890.6, 82 · 133 × 51** |
| KPI_13 | 168, 145 · 142.3 × 48 | **246, 146 · 62 × 46** |
| KPI_14 | 318.3, 145 · 142.3 × 48 | **396.3, 146 · 62 × 46** |
| KPI_15 | 468.6, 145 · 142.3 × 48 | **546.6, 146 · 62 × 46** |
| KPI_27 | 618.9, 145 · 142.3 × 48 | **696.9, 146 · 62 × 46** |
| KPI_28 / KPI_29 | 769.2, 145 · 142.3 × 48 | **847.2, 146 · 62 × 46** |
| KPI_30 / KPI_29 | 919.5, 145 · 142.3 × 48 | **997.5, 146 · 62 × 46** |
| VISUEL_12 | 168, 205 · 313 × 182 | **169, 236 · 311 × 150** |
| VISUEL_05 | 489, 205 · 314 × 182 | **490, 230 · 312 × 156** |
| VISUEL_13 | 811, 205 · 251 × 182 | **812, 237 · 249 × 149** |
| VISUEL_07 | 168, 397 · 443 × 313 | **169, 423 · 441 × 286** |
| VISUEL_08 | 620, 397 · 442 × 313 | **621, 423 · 440 × 286** |

### Segments à poser sur les listes dessinées

| Libellé imprimé | X | Y | Largeur | Hauteur |
|---|---:|---:|---:|---:|
| FILTRE_01 | 1081 | 87 | 172 | 21 |
| FILTRE_08 | 1081 | 156 | 172 | 21 |
| FILTRE_09 | 1081 | 202 | 172 | 21 |
| FILTRE_06 | 1081 | 271 | 172 | 21 |
| FILTRE_07 | 1081 | 317 | 172 | 21 |
| FILTRE_10 | 1081 | 363 | 172 | 21 |


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
