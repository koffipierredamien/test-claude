# 3 · Guide de montage Power BI, de A à Z

Les noms de menus sont donnés en français, puis en anglais entre parenthèses.

---

## Étape 0 · Le principe du montage

La maquette SVG contient **deux choses mélangées** :

| | Devient quoi dans Power BI |
|---|---|
| La **structure** : fond gris, cartes blanches, filets, panneau latéral | Image d'arrière-plan de page, figée |
| Le **contenu** : titres, chiffres, barres, courbes, lignes de tableau | De vrais visuels Power BI, par-dessus |

Utiliser la maquette telle quelle en arrière-plan ne marche pas : les faux
graphes resteraient visibles derrière les vrais. C'est pourquoi le dossier
`fonds/png/` contient des fonds **nettoyés** — uniquement la structure.

Le dossier `fonds/reference/` contient, lui, les maquettes complètes. Elles ne
servent pas de fond : elles servent de **calque de repérage**, à garder ouvert
sur un second écran pendant le montage.

> ⚠️ **Power BI n'accepte pas le SVG en arrière-plan de page.** Formats admis :
> PNG, JPG, BMP, GIF. Les PNG de `fonds/png/` sont exportés en 2560 × 1440,
> soit 2× le canevas, pour rester nets sur écran HiDPI.

---

## Étape 1 · Créer le fichier et régler le canevas

1. Power BI Desktop → **Fichier → Nouveau**.
2. Ne cliquez sur aucun visuel. Dans le volet **Format** de la page
   (Visualisations → icône pinceau, aucun visuel sélectionné) :
   - **Canevas** *(Canvas settings)* → Type = **Personnalisé** *(Custom)*
   - Largeur = **1280**, Hauteur = **720**
3. **Affichage → Ajuster à la page** *(View → Fit to page)*.

> C'est le réglage clé de tout le montage : le canevas fait exactement la
> taille du SVG. **Toutes les coordonnées de ce guide se reportent donc au
> pixel près** dans le volet Format → Général → Propriétés → Position.

4. **Affichage → Thème → Rechercher des thèmes** *(View → Themes → Browse for
   themes)* → sélectionnez `theme/theme-dashboard.json`.

Ce thème applique d'un coup la palette de la maquette, supprime les bordures et
en-têtes de visuels, et met les en-têtes de tableau en bleu nuit. Il vous
épargne plusieurs centaines de clics de mise en forme.

---

## Étape 2 · Importer les données

1. **Accueil → Obtenir les données → Texte/CSV** *(Get data → Text/CSV)*.
2. Importez les 11 fichiers de `donnees/`.
3. Pour chacun, dans l'aperçu : **Origine du fichier = UTF-8**,
   **Délimiteur = Point-virgule**.
4. **Transformer les données** *(Transform data)* avant de charger, et vérifiez
   les types :

| Colonne | Type attendu |
|---|---|
| `Date`, `DateEntree`, `DateSortie`, `DateCreation` | Date |
| `JH_*`, `Cout_*`, `Budget_*`, `Reste_A_Faire_EUR`, `FTE`, `Taux*` | Nombre décimal |
| `TJM_EUR`, `Annee`, `MoisNum`, `Jour`, `Present`, `EstJourOuvre`, `EstPasse`, `Ordre*`, `AnneeMoisTri` | Nombre entier |
| tout le reste | Texte |

> **Si les décimaux arrivent en texte ou en erreur** : les CSV utilisent la
> virgule décimale. Power Query doit lire en locale française. Clic droit sur
> la colonne → **Modifier le type → En utilisant les paramètres régionaux**
> → Type = Nombre décimal, Paramètres régionaux = **Français (France)**.

5. **Fermer et appliquer** *(Close & Apply)*.

---

## Étape 3 · Construire le modèle

Ouvrez la vue **Modèle** *(Model view)* et créez les relations du
[document 1](01-modele-de-donnees.md#relations-à-créer).

Points à ne pas rater :

1. `D_Objet[TribuID] → D_Tribu[TribuID]` doit rester **inactive**
   (double-clic sur le trait → décocher « Activer cette relation »).
2. Créez aussi **deux relations inactives** :
   `D_Ressource[DateEntree] → D_Calendrier[Date]` et
   `D_Ressource[DateSortie] → D_Calendrier[Date]` (pour `Entrées` / `Sorties`).
3. Sélectionnez `D_Calendrier` → **Outils de table → Marquer comme table de
   dates** *(Mark as date table)* → colonne `Date`.
4. Masquez des visuels (clic droit → Masquer dans la vue Rapport) toutes les
   colonnes techniques : `*ID`, `AnneeMoisTri`, `OrdreTribu`, `OrdrePortfolio`,
   `OrdreStatut`, `CouleurStatut`, `Present`.
5. Tri personnalisé — sélectionnez la colonne, puis **Colonnes → Trier par
   colonne** *(Sort by column)* :

| Colonne | Triée par |
|---|---|
| `D_Calendrier[MoisNom]` | `MoisNum` |
| `D_Calendrier[MoisAbrege]` | `MoisNum` |
| `D_Tribu[Tribu]` | `OrdreTribu` |
| `D_Portfolio[Portfolio]` | `OrdrePortfolio` |
| `D_Statut[Statut]` | `OrdreStatut` |

Sans cela, « Août » se retrouve entre « Avril » et « Décembre ».

---

## Étape 4 · Créer les mesures

1. **Accueil → Entrer des données** *(Enter data)* → nommez la table
   `_Mesures` → Charger. Masquez sa colonne unique.
2. Saisissez les mesures du [document 2](02-mesures-dax.md), **dans l'ordre**.
3. Rangez-les en dossiers d'affichage (volet Données → sélection → volet
   Propriétés → Dossier d'affichage) : `01 Socle`, `02 Effectif`,
   `03 Capacité`, `04 Budget`, `05 Libellés`.

---

## Étape 5 · Poser un fond de page

À refaire pour chacune des 5 pages :

1. Aucun visuel sélectionné → volet **Format** → **Arrière-plan du canevas**
   *(Canvas background)*
2. **Parcourir** → `fonds/png/Pn.png`
3. **Ajustement de l'image** *(Image fit)* = **Ajuster** *(Fit)*
4. **Transparence = 0 %** ← le réglage par défaut est 100 %, l'image serait
   invisible.

> Ne confondez pas avec *Papier peint* (*Wallpaper*), qui remplit la zone
> **autour** du canevas. C'est bien **Arrière-plan du canevas** qu'il faut.

---

## Étape 6 · Deux réglages qui servent sur toute la suite

### Positionner un visuel au pixel près

Sélectionnez le visuel → volet **Format** → **Général** → **Propriétés** →
**Position** : saisissez X, Y, Largeur, Hauteur. C'est ainsi que se reportent
toutes les coordonnées des tableaux qui suivent.

### Rendre un visuel transparent

Les cartes blanches sont déjà dessinées dans le fond. Chaque visuel posé
par-dessus doit donc être transparent :

- **Général → Effets → Arrière-plan** *(Effects → Background)* → **Désactivé**
- **Général → Effets → Bordure** → **Désactivé**
- **Général → En-tête du visuel** *(Header icons)* → **Désactivé**

Le thème JSON le fait déjà par défaut. Vérifiez seulement si un visuel
ressort en blanc opaque.

---

## Page 1 · Garde et sommaire — `P1.png`

Le fond conserve le décor (dégradé, carte, pastilles d'icônes). Il ne reste
qu'à poser le texte et la navigation.

| Élément | Type | X | Y | L | H |
|---|---|---:|---:|---:|---:|
| `RAPPORT_01 · CLIENT_1` | Zone de texte | 40 | 106 | 300 | 20 |
| `TITRE_RAPPORT_L1/L2` | Zone de texte, 2 lignes | 40 | 175 | 380 | 90 |
| `SOUS_TITRE_01` | Zone de texte | 40 | 288 | 300 | 24 |
| `BOUTON_01` | Bouton | 124 | 384 | 220 | 36 |
| `SOMMAIRE_01` | Zone de texte | 481 | 33 | 300 | 22 |
| Carte Page 1 | Bouton transparent | 481 | 73 | 757 | 71 |
| Carte Page 2 | Bouton transparent | 481 | 154 | 757 | 71 |
| Carte Page 3 | Bouton transparent | 481 | 235 | 757 | 71 |
| Carte Page 4 | Bouton transparent | 481 | 316 | 757 | 71 |
| Carte Page 5 | Bouton transparent | 481 | 397 | 757 | 71 |
| `Dernière actualisation` | Carte *(Card)* | 40 | 655 | 320 | 24 |
| `Version 1.0 · 08/09/2026` | Zone de texte | 1000 | 655 | 238 | 24 |

**Typographies** — Segoe UI. Titre 32 pt gras blanc, sous-titre 15 pt gras
blanc, sur-titre 10 pt blanc à 70 % d'opacité.

**Les 5 cartes de sommaire.** Chacune est un **Bouton** *(Insérer → Boutons →
Vide)* posé exactement sur la carte blanche du fond :

1. Format → **Remplissage** → Transparence **100 %**
2. Format → **Bordure** → Désactivé
3. Format → **Texte** → Activé → saisissez `PAGE_01`, aligné à gauche,
   marge intérieure gauche ≈ 70 px pour dégager la pastille du fond
4. Format → **Action** → Type = **Navigation de page** *(Page navigation)* →
   Destination = la page cible
5. Répétez pour les 4 autres.

> Le sous-titre `DESCRIPTION_0n` demande une seconde ligne : un bouton ne gère
> qu'un seul niveau de texte. Posez une **zone de texte** juste en dessous
> (Y + 28, hauteur 16, 8 pt, gris `#6B7280`) et **envoyez-la à l'arrière**
> pour que le bouton reste cliquable sur toute sa surface.

---

## Page 2 · Capacité et charge — `P2.png`

C'est la page la plus dense : montez-la en premier, les trois suivantes en
reprennent les recettes.

### Bandeau et navigation

| Élément | Type | X | Y | L | H |
|---|---|---:|---:|---:|---:|
| `RAPPORT_01` + `CLIENT_01` | 2 zones de texte | 10 | 14 | 140 | 44 |
| Boutons de navigation ×6 | Boutons | 7 | 90 + 68·n | 145 | 44 |
| `TITRE_01` | Zone de texte | 178 | 18 | 300 | 24 |
| `SOUS_TITRE_01` | Carte → `Sous-titre période` | 480 | 20 | 300 | 20 |

**Les boutons de navigation** se construisent une fois, puis se copient sur les
4 autres pages. Pour chacun : Action = Navigation de page, texte 9,5 pt,
remplissage transparent. Sur la page *courante*, dupliquez le bouton actif avec
remplissage `#0B2A5B` et texte blanc — c'est ce qui produit la pastille bleue
de la maquette.

> **Plus simple et plus robuste** : insérez un **Navigateur de pages**
> *(Insérer → Boutons → Navigateur → Navigateur de pages)* en X=7, Y=90,
> L=145, H=420. Il se remplit tout seul, gère l'état sélectionné, et se met à
> jour quand vous ajoutez une page. Masquez les pages que vous ne voulez pas y
> voir (clic droit sur l'onglet → Masquer la page).

### Rangée de KPI

| Repère | Visuel | Mesure | X | Y | L | H |
|---|---|---|---:|---:|---:|---:|
| KPI_01 | Carte | `Effectif` | 168 | 58 | 217 | 76 |
| KPI_02 | Carte | `JH consommés` | 393,7 | 58 | 217 | 76 |
| KPI_03 | Carte | `JH restant à planifier` | 619,4 | 58 | 217 | 76 |
| KPI_04 | Carte | `Coût consommé K€` | 845,1 | 58 | 217 | 76 |

Pour chaque carte :
- **Général → Effets → Arrière-plan** Désactivé, **Bordure** Désactivée
- **Valeur de légende** *(Callout value)* : Segoe UI Bold **22 pt**, `#0B2A5B`,
  aligné au centre
- **Étiquette de catégorie** *(Category label)* : **Désactivée**

Le libellé `KPI_01` et le sous-texte ne viennent **pas** de la carte : posez-les
séparément.
- Libellé : zone de texte en (X+9, Y+7), 8,5 pt, `#6B7280`
- Sous-texte KPI_01 : carte `Libellé mix effectif` en (X+9, Y+56), L=200, H=16
- Sous-texte KPI_02 / KPI_03 : zone de texte `JH`, centrée, 8 pt, `#6B7280`

> Les pastilles rondes colorées avec leur icône sont déjà dans le fond ? **Non**
> — elles ont été retirées avec le contenu. Reposez-les : Insérer → Formes →
> Cercle, 28 px, remplissage `#2E9E8F` / `#3F8F3F` / `#E8734A` / `#D9534F`,
> puis Insérer → Image pour l'icône. Ou laissez-les de côté dans un premier
> temps : la page fonctionne sans.

### Barre de répartition KPI_05

| Repère | Visuel | X | Y | L | H |
|---|---|---:|---:|---:|---:|
| KPI_05 | Graphique à barres empilées 100 % | 176 | 172 | 427 | 26 |

- **Axe Y** : rien *(la barre est unique)*
- **Valeurs** : `% coût externes`, `% coût internes`
- Axe X et axe Y : **Désactivés**
- **Étiquettes de données** : Activées, position **Au centre**, blanc, 8 pt
- **Couleurs** : `#5B3F8F` et `#2E9E8F`
- **Légende** : Désactivée — posez à la place deux cartes
  `Légende coût externes` et `Légende coût internes` en Y = 205

### KPI_06 et KPI_07

Deux cartes identiques aux précédentes : (620, 145, 217, 75) et
(846, 145, 216, 75), avec `Sorties` et `Entrées`.

### VISUEL_01 · Charge par tribu

| Visuel | X | Y | L | H |
|---|---:|---:|---:|---:|
| **Graphique en courbes et histogramme groupé** | 176 | 255 | 427 | 137 |

- **Axe X** : `D_Tribu[Tribu]`
- **Valeurs de colonne** : `JH planifiés`, `JH consommés`
- **Valeurs de ligne** : `Coût consommé K€`
- **Couleurs** : colonnes `#2E9E8F` et `#0B2A5B`, ligne `#0B2A5B`
- **Étiquettes de données** : Activées, 7 pt
- **Axe Y** (les deux) : Désactivés
- **Légende** : Haut à gauche, 8 pt
- **Titre** : `VISUEL_01`, gauche, 11 pt, `#0B2A5B`
- **Filtre** : dans le volet Filtres, `D_Tribu[Tribu]` → **N premiers** = 7,
  par `JH planifiés` (la maquette n'en montre que 7)

### VISUEL_02 · Saisonnalité mensuelle

| Visuel | X | Y | L | H |
|---|---:|---:|---:|---:|
| **Histogramme groupé** | 628 | 255 | 426 | 137 |

- **Axe X** : `D_Calendrier[MoisAbrege]`
- **Valeurs** : `JH consommés`
- **Couleur** : `#2E9E8F`
- **Étiquettes de données** : Activées, 7 pt
- **Axe Y** : Désactivé
- Volet Filtres → filtre de page `D_Calendrier[Annee] = 2026`

> **Pour que septembre à décembre apparaissent à 0** au lieu de disparaître :
> cliquez sur le champ `MoisAbrege` dans le puits Axe X → **Afficher les
> éléments sans données** *(Show items with no data)*. C'est exactement le
> rendu de la maquette.

### VISUEL_03 · Matrice mensuelle

| Visuel | X | Y | L | H |
|---|---:|---:|---:|---:|
| **Matrice** *(Matrix)* | 176 | 440 | 878 | 262 |

- **Lignes** : `Tribu`, `Squad`, `Objet`, `Portfolio`, `Priorité`, `Société`
- **Colonnes** : `D_Calendrier[MoisAbrege]`
- **Valeurs** : `JH consommés`
- **Format → Disposition** : **Disposition en tableau** *(Tabular)*,
  sous-totaux de lignes **Désactivés**, total général de colonnes **Activé**
- **En-têtes de colonnes** : fond `#0B2A5B`, texte blanc, 8 pt *(déjà dans le
  thème)*
- **Quadrillage** : horizontal `#E5E7EB`, vertical désactivé, remplissage 4

Le double niveau d'en-tête de la maquette (`COL_01` / `COL_02` au-dessus des
colonnes) vient d'une hiérarchie de colonnes : mettez `Annee` puis
`MoisAbrege` dans le puits Colonnes, et dépliez d'un niveau.

### Panneau de filtres

Le panneau blanc (1072, 11, 190, 699) accueille 7 segments *(Slicers)*
empilés, calés sur les filets du fond :

| Segment | Champ | X | Y | L | H |
|---|---|---:|---:|---:|---:|
| FILTRE_01 | `D_Calendrier[Annee]` | 1081 | 87 | 172 | 21 |
| FILTRE_02 | `D_Tribu[Tribu]` | 1081 | 160 | 172 | 24 |
| FILTRE_03 | `D_Squad[Squad]` | 1081 | 205 | 172 | 24 |
| FILTRE_04 | `D_Societe[Société]` | 1081 | 273 | 172 | 24 |
| FILTRE_05 | `D_Ressource[TypeRessource]` | 1081 | 318 | 172 | 24 |
| FILTRE_06 | `D_Portfolio[Portfolio]` | 1081 | 386 | 172 | 24 |
| FILTRE_07 | `D_Objet[Statut]` | 1081 | 431 | 172 | 24 |

Pour chacun : **Format → Paramètres du segment → Style = Liste déroulante**
*(Dropdown)*, en-tête **Désactivé**. Posez le libellé (`FILTRE_0n`) en zone de
texte 4 px au-dessus, 9 pt, `#1F2937`.

Le bouton « gomme » en haut à droite du panneau (1245, 20) :
Insérer → Boutons → **Réinitialiser** *(Reset)* → Action = Signet, pointant sur
un signet « État initial » capturé avant toute sélection.

### Pied de page

Carte `Dernière actualisation` en (10, 660, 150, 30), 7 pt, `#6B7280`.

---

## Page 3 · Ressources — `P3.png`

### KPI

| Repère | Mesure | X | Y | L | H |
|---|---|---:|---:|---:|---:|
| KPI_21 | `Effectif` | 168 | 58 | 217 | 76 |
| KPI_22 | `Effectif externes` | 393,7 | 58 | 217 | 76 |
| KPI_23 | `Effectif internes` | 619,4 | 58 | 217 | 76 |
| KPI_24 | `Effectif stagiaires` | 845,1 | 58 | 217 | 76 |

Sous-texte des trois derniers : carte `Libellé part empreinte`, ou la mesure
`% externes` / `% internes` / `% stagiaires` formatée en pourcentage.

### VISUEL_09 · Répartition par société

| Visuel | X | Y | L | H |
|---|---:|---:|---:|---:|
| **Anneau** *(Donut chart)* | 176 | 169 | 344 | 236 |

- **Légende** : `D_Societe[Société]`
- **Valeurs** : `Effectif`
- **Format → Tranches → Rayon intérieur** = 62 %
- **Étiquettes détaillées** *(Detail labels)* : Activées, Contenu =
  **Catégorie, valeur et pourcentage total**, Position = **À l'extérieur**
- **Légende** : Haut à gauche, 8 pt

### VISUEL_10 · Effectif par tribu

| Visuel | X | Y | L | H |
|---|---:|---:|---:|---:|
| **Histogramme empilé** *(Stacked column chart)* | 545 | 169 | 509 | 236 |

- **Axe X** : `D_Tribu[Tribu]`
- **Légende** : `D_Ressource[TypeRessource]`
- **Valeurs** : `Effectif`
- **Couleurs** : Externe `#2E9E8F`, Interne `#0B2A5B`
- **Étiquettes de données** : Activées, 7 pt, position **Extérieur de la fin**
  *(Outside end)* sur le total — activez **Total** dans les étiquettes
- **Axe X → Taille du texte** 7 pt, **Angle de rotation** −45°
- **Tri** : cliquez sur le menu « … » du visuel → Trier par `Effectif`, décroissant

### VISUEL_11 · Table des ressources

| Visuel | X | Y | L | H |
|---|---:|---:|---:|---:|
| **Table** | 176 | 440 | 878 | 262 |

Colonnes, dans l'ordre de la maquette :
`Ressource` · `Tribu` · `Squad` · `ResID` · `Objet` · `TypeRessource` ·
`Profil` · `Société` · `DateEntree` · `DateSortie` · `JH restant à planifier` ·
`TJM_EUR` · `CoutJournalier_EUR` · `TauxActivite` · `TauxAbsence` · `FTE`

- **Format → Largeur de colonne automatique** : **Désactivée**, puis ajustez
  chaque largeur à la main
- Alignez à droite toutes les colonnes numériques
- `TauxActivite` / `TauxAbsence` : format **Pourcentage, 0 décimale**

---

## Page 4 · Demandes et portefeuille — `P4.png`

### Grande rangée de KPI — 5 cartes de 172,4 × 76 en Y = 58

| Repère | Mesure | X |
|---|---|---:|
| KPI_08 | `Nb demandes` | 168 |
| KPI_09 | `Budget initial K€` | 348,4 |
| KPI_10 | `Budget consommé K€` | 528,8 |
| KPI_11 | `Budget engagé K€` | 709,2 |
| KPI_12 | `Reste à faire K€` | 889,6 |

Sous-texte de KPI_11 et KPI_12 : carte `Libellé atteinte budget`.

### Petite rangée de compteurs — 6 cartes de 142,3 × 48 en Y = 145

| Repère | Mesure | X |
|---|---|---:|
| KPI_13 | `Nb à cadrer` | 168 |
| KPI_14 | `Nb cadrés` | 318,3 |
| KPI_15 | `Nb suspendus` | 468,6 |
| KPI_16 | `Nb en recette` | 618,9 |
| KPI_17/18 | `Nb en cours` | 769,2 |
| KPI_19/20 | `Nb livrés` | 919,5 |

Ces cartes-là ont leur **valeur alignée à droite** et leur libellé à gauche de
la pastille. Posez la carte sur la moitié droite seulement :
X + 60, largeur 75.

### VISUEL_04 · Charge par portfolio

| Visuel | X | Y | L | H |
|---|---:|---:|---:|---:|
| **Histogramme groupé** | 176 | 229 | 297 | 150 |

Axe X `D_Portfolio[Portfolio]` · Valeurs `JH consommés` · couleur `#0B2A5B` ·
étiquettes 6,5 pt · axe X à −45°, 6 pt.

### VISUEL_05 · Top tribus, N vs N-1

| Visuel | X | Y | L | H |
|---|---:|---:|---:|---:|
| **Table** | 497 | 229 | 298 | 150 |

Colonnes : `Tribu` · `JH consommés N-1` · `JH consommés` · `Écart JH vs N-1` ·
`% écart JH vs N-1`.
Filtre du visuel : `Tribu` → **N premiers = 5** par `Écart JH vs N-1`.
Format de l'écart : personnalisé `+# ##0;-# ##0` pour afficher le signe.

### VISUEL_06 · Répartition par statut

| Visuel | X | Y | L | H |
|---|---:|---:|---:|---:|
| **Anneau** | 819 | 229 | 235 | 150 |

Légende `D_Statut[Statut]` · Valeurs `Nb objets` · rayon intérieur 65 % ·
**Légende à droite** · étiquettes détaillées désactivées (la maquette met tout
dans la légende : Contenu de la légende = *Catégorie, valeur et pourcentage*).

### VISUEL_07 et VISUEL_08 · Top 10

| Visuel | X | Y | L | H |
|---|---:|---:|---:|---:|
| VISUEL_07 — **Table** | 176 | 430 | 427 | 272 |
| VISUEL_08 — **Table** | 628 | 430 | 426 | 272 |

**VISUEL_07** : `ObjetID` · `Objet` · `JH planifiés` · `JH consommés` ·
`Écart JH vs N-1`. Filtre : N premiers = 10 par `JH consommés`.

**VISUEL_08** : `ObjetID` · `Objet` · `Budget initial K€` ·
`Budget consommé K€` · `% budget consommé`. Filtre : N premiers = 10 par
`Budget consommé K€`. Appliquez la couleur conditionnelle `Alerte budget` sur
la dernière colonne.

Le sélecteur « Top 10 » en haut à droite de chaque table (X = 803 / 1255,
Y = 40, L = 104, H = 22) est un **segment** sur un paramètre numérique :
**Modélisation → Nouveau paramètre → Plage numérique**, nom `Top N`, de 5 à 50,
pas de 5. Remplacez alors le filtre fixe par :

```dax
Rang objet =
RANKX ( ALLSELECTED ( D_Objet[Objet] ), [JH consommés], , DESC )
```
puis filtre du visuel : `Rang objet` ≤ `Valeur Top N`.

### Panneau de filtres

Même principe que page 2, avec les champs de la maquette : `Portfolio`,
`Segment`, `Statut`, `Priorite`, `Tribu`, `TypeObjet`.

---

## Page 5 · Projets de maintenance — `P5.png`

**La géométrie est strictement identique à la page 4.** Le plus rapide :

1. Clic droit sur l'onglet de la page 4 → **Dupliquer la page**
2. Changez le fond pour `P5.png`
3. Volet Filtres → **filtre au niveau de la page** :
   `D_Objet[TypeObjet]` est `Projet de maintenance`
4. Remplacez les 3 visuels qui diffèrent (ci-dessous)

| Repère | Mesure | X |
|---|---|---:|
| KPI_08 | `Nb projets` | 168 |
| KPI_25 | `JH planifiés` | 348,4 |
| KPI_26 | `JH consommés` | 528,8 |
| KPI_11 | `Budget engagé K€` | 709,2 |
| KPI_12 | `Reste à faire K€` | 889,6 |

**VISUEL_12** (176, 229, 297, 150) — **Histogramme groupé** :
Axe X `D_Objet[Objet]`, Valeurs `JH planifiés` **et** `JH consommés`,
couleurs `#0B2A5B` / `#2E9E8F`. Étiquettes 6 pt, unités d'affichage
**Milliers**.

**VISUEL_13** (819, 229, 235, 150) — **Anneau** :
Légende `D_Portfolio[Segment]` *(ou `D_Objet[Priorite]`)*, Valeurs
`JH consommés`, unités **Milliers**.

Les deux tables du bas et VISUEL_05 se conservent telles quelles : le filtre de
page fait le travail.

---

## Étape 7 · Interactions et finitions

### Interactions entre visuels

**Format → Modifier les interactions** *(Edit interactions)*. Réglages conseillés :

- Les segments filtrent tout : par défaut, rien à faire.
- VISUEL_01 / VISUEL_04 → mettez les autres visuels en **Filtrer** plutôt qu'en
  **Mettre en surbrillance** : les tables deviennent lisibles au clic.
- Les cartes de KPI → **Aucun** *(None)* en cible. Un KPI ne doit pas se
  refiltrer lui-même quand on clique ailleurs.

### Info-bulles

Les petits ⓘ de la maquette correspondent à des info-bulles. Créez une page
**Info-bulle** : Format de page → Type = **Info-bulle**, taille 320 × 180, puis
sur chaque visuel : Format → Général → **Info-bulles** → Type = Page de
rapport → choisissez la page.

### Explorer les données

Sur les visuels par tribu, ajoutez un **détail** *(drill-through)* : créez une
page masquée « Détail tribu », glissez `D_Tribu[Tribu]` dans le puits
**Extraction** *(Drill through)*.

### Avant de livrer

- [ ] Les 5 pages ont leur fond posé, transparence 0 %
- [ ] Aucun visuel n'affiche de bordure ni d'en-tête blanc
- [ ] Le tri par colonne est appliqué (mois, tribus, statuts)
- [ ] `D_Calendrier` est marquée comme table de dates
- [ ] Chaque page est en **Affichage → Ajuster à la page**
- [ ] Les onglets techniques (info-bulles, extraction) sont masqués
- [ ] Fichier → Options → Paramètres du rapport → **Ordre de tabulation**
      revu pour l'accessibilité
