# 2 · Mesures DAX

Toutes les mesures se rangent dans une table dédiée `_Mesures`
(Accueil → Entrer des données → une colonne, aucune ligne → Charger,
puis masquer la colonne). Le groupe `_` la fait remonter en tête du volet.

Les noms entre crochets renvoient à une mesure définie plus haut dans ce
document : créez-les dans l'ordre.

---

## 2.1 · Socle

```dax
JH consommés   = SUM ( F_Charge[JH_Consommes] )
JH planifiés   = SUM ( F_Charge[JH_Planifies] )
Coût consommé  = SUM ( F_Charge[Cout_Consomme_EUR] )
Coût planifié  = SUM ( F_Charge[Cout_Planifie_EUR] )

Budget initial   = SUM ( F_Budget[Budget_Initial_EUR] )
Budget engagé    = SUM ( F_Budget[Budget_Engage_EUR] )
Budget consommé  = SUM ( F_Budget[Budget_Consomme_EUR] )
Reste à faire    = SUM ( F_Budget[Reste_A_Faire_EUR] )

Jours ouvrés = CALCULATE ( SUM ( D_Calendrier[EstJourOuvre] ) )
```

### Déclinaisons en K€

La maquette n'affiche jamais d'euros bruts : tous les montants sont en K€.

```dax
Coût consommé K€    = DIVIDE ( [Coût consommé],   1000 )
Budget initial K€   = DIVIDE ( [Budget initial],  1000 )
Budget engagé K€    = DIVIDE ( [Budget engagé],   1000 )
Budget consommé K€  = DIVIDE ( [Budget consommé], 1000 )
Reste à faire K€    = DIVIDE ( [Reste à faire],   1000 )
```

> Format d'affichage pour ces cinq mesures : **Nombre décimal, 0 décimale,
> séparateur de milliers coché**, puis dans *Format personnalisé* :
> `#,##0 "K€"`.

---

## 2.1 bis · Supprimer les abréviations K / M

Par défaut, un visuel affiche `2K` au lieu de `2 000`, et `3M` au lieu de
`3 000 000`. Le coupable n'est pas la mesure mais un réglage du visuel :
**Unités d'affichage** *(Display units)*, qui vaut **Auto**.

**Ce réglage écrase la chaîne de format de la mesure.** Tant qu'il est sur Auto,
modifier le format du modèle ne change rien à l'écran — c'est la cause la plus
fréquente de « je n'arrive pas à enlever le K ».

### Les trois niveaux, dans l'ordre où il faut les traiter

| Niveau | Où | Effet |
|---|---|---|
| 1. Le thème | `theme-dashboard.json`, `labelDisplayUnits: 1` | Toute nouveauté naît en « Aucune » |
| 2. La mesure | Outils de mesure → Format | Fait foi partout où le visuel ne surcharge pas — tables et matrices notamment |
| 3. Le visuel | Format → Unités d'affichage = **Aucune** | Rattrape les visuels créés avant le thème |

### 0 · « Je ne vois ce réglage nulle part »

Quatre causes, par ordre de fréquence :

1. **Le visuel n'est pas sélectionné.** Le volet Format bascule alors sur les
   réglages *de la page*. Cliquez sur la carte : son cadre doit s'entourer de
   poignées.
2. **Vous êtes sur l'onglet Général.** Le volet a deux onglets, **Visuel** et
   **Général**. *Général* ne porte que position, taille, arrière-plan, bordure
   et titre. Les unités d'affichage sont sous **Visuel**.
3. **La section est repliée.** Utilisez la **zone de recherche en haut du volet
   Format** et tapez `unit` — le réglage remonte où qu'il soit. En anglais,
   `display`.
4. **Ce visuel n'a pas ce réglage.** Table, Matrice et Segment n'en ont pas :
   pour eux, tout vient du format de la mesure (niveau 2 ci-dessous).

#### Carte classique ou Carte (nouveau) ?

Les deux existent et n'ont pas les mêmes sections. Repérez-les dans
**Format → Visuel** :

| Sections visibles | Visuel |
|---|---|
| `Valeur de légende` · `Étiquette de catégorie` | **Carte** classique |
| `Cartes` · `Valeur de légende` · `Étiquettes` · `Image` | **Carte (nouveau)** |

`Disposition`, `Forme`, `Remplissage`, `Bordure`, `Diviseur`,
`Barre d'accentuation`, `Ombre` et `Lueur` appartiennent tous au groupe
**Cartes** de la Carte (nouveau) : ce sont des réglages d'apparence du bloc,
jamais de la valeur. Si vous les voyez, repliez le groupe `Cartes` en cliquant
sur son en-tête, puis descendez jusqu'à **`Valeur de légende`**.

#### La Carte (nouveau) n'a pas d'unités d'affichage

Vérifié dans l'interface : sa section **Valeur** ne contient que police,
couleur, transparence, alignement, « Afficher vide en tant que » et retour à la
ligne. **Ni unités d'affichage, ni décimales.** Son affichage numérique vient
donc *uniquement* du format du champ.

Sur ce visuel, il n'y a que deux voies :

1. **Le format de la mesure.** Volet Données → la mesure → ruban **Outils de
   mesure** → liste **Format** → `Personnalisé` → `#,##0` puis **Entrée**
   (le champ ne valide pas si l'on clique ailleurs). Si c'est une *colonne* qui
   est posée sur la carte — elle s'affiche « Somme de … » — le format se règle
   sur la colonne : **Outils de colonne → Format**.
2. **Une mesure texte**, qui ne dépend de rien (voir plus haut).

> **Le guide suppose la Carte classique** — valeur de légende à 22 pt, étiquette
> de catégorie désactivée, positionnement au pixel. C'est aussi la seule des
> deux qui expose les unités d'affichage. Pour basculer : dans le volet
> Visualisations, l'icône de la carte classique est **`123`** ; l'info-bulle au
> survol distingue *Carte* de *Carte (nouveau)*. Le champ reste en place.

#### Le test qui tranche

Sélectionnez la carte, puis basculez-la en **Table** depuis le volet
Visualisations :

- la table affiche `1 061` → le format de la mesure est bon, le coupable est
  l'unité d'affichage du visuel ;
- la table affiche `2K` elle aussi → c'est le format de la mesure qui n'a pas
  été appliqué.

Re-cliquez ensuite sur Carte pour revenir.

Si rien n'y fait, l'échappatoire imparable est une mesure qui renvoie du
**texte** — Power BI ne peut pas abréger du texte :

```dax
KPI_01 · libellé = FORMAT ( [Effectif], "#,##0" )
```

À réserver aux cartes d'affichage : une mesure texte ne se trie plus et ne se
compare plus numériquement, donc jamais dans une colonne de tableau ni sur un axe.

### 1 · Le thème

Le fichier fourni force déjà `labelDisplayUnits: 1` (= Aucune) sur les cartes,
les étiquettes de données et les axes. **Un thème ne s'applique qu'aux propriétés
que vous n'avez pas déjà modifiées à la main** : réappliquez-le
(Affichage → Thème → Rechercher des thèmes), et pour un visuel déjà retouché,
remettez la propriété à zéro avec le petit bouton **Réinitialiser**
*(Revert to default)* en regard du réglage.

### 2 · La mesure

Sélectionnez la mesure dans le volet Données → onglet **Outils de mesure**
*(Measure tools)* → champ **Format** :

| Type de mesure | Format à saisir | Rendu |
|---|---|---|
| Compteur d'entiers | `#,##0` | `1 061` |
| Montant en K€ | `#,##0 "K€"` | `103 273 K€` |
| Jours-hommes | `#,##0 " JH"` | `244 413 JH` |
| Écart signé | `+#,##0;-#,##0;0` | `+1 422` / `-631` |
| Pourcentage | `0,0 %` | `19,1 %` |

Le `,` d'un format personnalisé n'est pas une virgule littérale : c'est le
marqueur de groupement des milliers, rendu selon la locale — donc une espace en
français. N'écrivez pas l'espace vous-même.

### 3 · Les tables et matrices

Elles n'ont pas de réglage « Unités d'affichage » : leur affichage vient
**uniquement** de la chaîne de format de la mesure. Corriger le niveau 2 les
corrige toutes d'un coup.

### Là où l'abréviation est voulue

Deux visuels de la maquette affichent délibérément des valeurs abrégées :
<span>`VISUEL_12`</span> (page 5, `2,6K`) et les KPI `KPI_25` / `KPI_26`
(`37,5K`, `24K`). Sur ces trois-là seulement, remettez
**Unités d'affichage = Milliers**.

---

## 2.2 · Effectif

```dax
Effectif = DISTINCTCOUNT ( F_Effectif[ResID] )

Effectif fin de période =
VAR DernierMois = MAX ( F_Effectif[Date] )
RETURN
    CALCULATE (
        DISTINCTCOUNT ( F_Effectif[ResID] ),
        F_Effectif[Date] = DernierMois
    )

Effectif externes  = CALCULATE ( [Effectif], D_Ressource[TypeRessource] = "Externe"   )
Effectif internes  = CALCULATE ( [Effectif], D_Ressource[TypeRessource] = "Interne"   )
Effectif alternants= CALCULATE ( [Effectif], D_Ressource[TypeRessource] = "Alternant" )
Effectif stagiaires= CALCULATE ( [Effectif], D_Ressource[TypeRessource] = "Stagiaire" )

% externes   = DIVIDE ( [Effectif externes],   [Effectif] )
% internes   = DIVIDE ( [Effectif internes],   [Effectif] )
% alternants = DIVIDE ( [Effectif alternants], [Effectif] )
% stagiaires = DIVIDE ( [Effectif stagiaires], [Effectif] )
```

### Mouvements

```dax
Entrées =
CALCULATE (
    DISTINCTCOUNT ( D_Ressource[ResID] ),
    USERELATIONSHIP ( D_Ressource[DateEntree], D_Calendrier[Date] )
)

Sorties =
CALCULATE (
    DISTINCTCOUNT ( D_Ressource[ResID] ),
    USERELATIONSHIP ( D_Ressource[DateSortie], D_Calendrier[Date] )
)
```

> Ces deux mesures supposent deux relations **inactives** supplémentaires,
> de `D_Ressource[DateEntree]` et `D_Ressource[DateSortie]` vers
> `D_Calendrier[Date]`. Créez-les dans la vue Modèle, décochez « Activer ».

---

## 2.3 · Capacité et taux d'occupation

```dax
Capacité JH =
SUMX (
    VALUES ( D_Calendrier[AnneeMois] ),
    CALCULATE ( SUM ( F_Effectif[FTE] ) ) * CALCULATE ( SUM ( D_Calendrier[EstJourOuvre] ) )
)

JH restant à planifier = MAX ( 0, [Capacité JH] - [JH planifiés] )

Taux d'occupation = DIVIDE ( [JH consommés], [Capacité JH] )
Taux de réalisation = DIVIDE ( [JH consommés], [JH planifiés] )
```

---

## 2.4 · Répartition du coût (KPI_05, barre 100 %)

```dax
Coût externes K€ = CALCULATE ( [Coût consommé K€], D_Ressource[TypeRessource] = "Externe" )
Coût internes K€ = CALCULATE ( [Coût consommé K€], D_Ressource[TypeRessource] = "Interne" )

% coût externes = DIVIDE ( [Coût externes K€], [Coût consommé K€] )
% coût internes = DIVIDE ( [Coût internes K€], [Coût consommé K€] )

Légende coût externes = "DIM_01 · " & FORMAT ( [Coût externes K€], "#,##0" ) & " K€"
Légende coût internes = "DIM_02 · " & FORMAT ( [Coût internes K€], "#,##0" ) & " K€"
```

---

## 2.5 · Comparaison N vs N-1 (VISUEL_05)

```dax
JH consommés N-1 =
CALCULATE ( [JH consommés], SAMEPERIODLASTYEAR ( D_Calendrier[Date] ) )

Écart JH vs N-1   = [JH consommés] - [JH consommés N-1]
% écart JH vs N-1 = DIVIDE ( [Écart JH vs N-1], [JH consommés N-1] )
```

> `SAMEPERIODLASTYEAR` exige que `D_Calendrier` soit **marquée comme table de
> dates** (Outils de table → Marquer comme table de dates → colonne `Date`).
> Sans cela, la mesure renvoie une erreur ou des valeurs fausses.

---

## 2.6 · Portefeuille : demandes et projets

```dax
Nb demandes = CALCULATE ( DISTINCTCOUNT ( D_Objet[ObjetID] ), D_Objet[TypeObjet] = "Demande" )
Nb projets  = CALCULATE ( DISTINCTCOUNT ( D_Objet[ObjetID] ), D_Objet[TypeObjet] = "Projet de maintenance" )
Nb objets   = DISTINCTCOUNT ( D_Objet[ObjetID] )
```

### Compteurs par statut (KPI_13 → KPI_20)

Une seule mesure paramétrable plutôt que sept quasi-identiques :

```dax
Nb objets par statut =
VAR StatutCible = SELECTEDVALUE ( D_Statut[Statut] )
RETURN CALCULATE ( [Nb objets], D_Statut[Statut] = StatutCible )
```

Puis, pour les cartes fixes de la maquette :

```dax
Nb à cadrer   = CALCULATE ( [Nb objets], D_Statut[Statut] = "À cadrer"   )
Nb cadrés     = CALCULATE ( [Nb objets], D_Statut[Statut] = "Cadré"      )
Nb en cours   = CALCULATE ( [Nb objets], D_Statut[Statut] = "En cours"   )
Nb en recette = CALCULATE ( [Nb objets], D_Statut[Statut] = "En recette" )
Nb livrés     = CALCULATE ( [Nb objets], D_Statut[Statut] = "Livré"      )
Nb suspendus  = CALCULATE ( [Nb objets], D_Statut[Statut] = "Suspendu"   )
Nb abandonnés = CALCULATE ( [Nb objets], D_Statut[Statut] = "Abandonné"  )
```

### Consommation budgétaire (VISUEL_08, colonne COL_21)

```dax
% budget consommé = DIVIDE ( [Budget consommé], [Budget initial] )
% budget engagé   = DIVIDE ( [Budget engagé],   [Budget initial] )

Écart budget K€ = [Budget initial K€] - [Budget consommé K€]

Alerte budget =
SWITCH (
    TRUE (),
    [% budget consommé] > 1.10, "#D9534F",
    [% budget consommé] > 0.95, "#E0B23A",
    "#2E9E8F"
)
```

> `Alerte budget` ne s'affiche pas : elle sert de **couleur par expression**
> sur la colonne `% budget consommé` (Format → Éléments visuels → Couleur de
> police → *fx* → Format par = Valeur du champ).

---

## 2.7 · Bascule « tribu de la ressource » ↔ « tribu de l'objet »

Les pages Demandes et Projets analysent la tribu **propriétaire de l'objet**,
pas celle de la ressource qui consomme. D'où l'usage de la relation inactive :

```dax
JH consommés (tribu objet) =
CALCULATE (
    [JH consommés],
    USERELATIONSHIP ( D_Objet[TribuID], D_Tribu[TribuID] )
)

Budget consommé K€ (tribu objet) =
CALCULATE (
    [Budget consommé K€],
    USERELATIONSHIP ( D_Objet[TribuID], D_Tribu[TribuID] )
)
```

---

## 2.8 · Textes dynamiques

```dax
Libellé mix effectif =
FORMAT ( [Effectif externes], "#,##0" ) & " externes  |  "
    & FORMAT ( [Effectif internes], "#,##0" ) & " internes"

Libellé part empreinte =
FORMAT ( DIVIDE ( [Effectif externes], [Effectif] ), "0,00 %" ) & " de l'empreinte"

Libellé atteinte budget =
FORMAT ( DIVIDE ( [Budget engagé], [Budget initial] ), "0,0 %" ) & " du budget cible"

Sous-titre période =
VAR Deb = MIN ( D_Calendrier[Date] )
VAR Fin = MAX ( D_Calendrier[Date] )
RETURN FORMAT ( Deb, "MMMM yyyy" ) & " → " & FORMAT ( Fin, "MMMM yyyy" )
```

### Horodatage du pied de page

`NOW()` se recalcule à chaque interaction : il ne convient pas. Créez plutôt
une requête Power Query dédiée.

1. Accueil → Transformer les données → Nouvelle source → **Requête vide**
2. Dans la barre de formule : `= #table({"Rafraichissement"}, {{DateTime.LocalNow()}})`
3. Renommez la requête `_Rafraichissement`, type de colonne = Date/Heure, Fermer et appliquer.

```dax
Dernière actualisation =
"Dernière actualisation : "
    & FORMAT ( MAX ( _Rafraichissement[Rafraichissement] ), "dd/MM/yyyy HH:mm" )
```

---

## 2.9 · Récapitulatif : quelle mesure pour quel KPI

| Page | Repère maquette | Mesure |
|---|---|---|
| Capacité | KPI_01 | `Effectif` + `Libellé mix effectif` |
| Capacité | KPI_02 | `JH consommés` |
| Capacité | KPI_03 | `JH restant à planifier` |
| Capacité | KPI_04 | `Coût consommé K€` |
| Capacité | KPI_05 | `% coût externes` / `% coût internes` |
| Capacité | KPI_06 | `Sorties` |
| Capacité | KPI_07 | `Entrées` |
| Ressources | KPI_21 | `Effectif` |
| Ressources | KPI_22 | `Effectif externes` + `Libellé part empreinte` |
| Ressources | KPI_23 | `Effectif internes` |
| Ressources | KPI_24 | `Effectif stagiaires` |
| Demandes | KPI_08 | `Nb demandes` |
| Demandes | KPI_09 | `Budget initial K€` |
| Demandes | KPI_10 | `Budget consommé K€` |
| Demandes | KPI_11 | `Budget engagé K€` + `Libellé atteinte budget` |
| Demandes | KPI_12 | `Reste à faire K€` |
| Demandes | KPI_13 → 20 | `Nb à cadrer`, `Nb en cours`, … |
| Projets | KPI_25 / KPI_26 | `JH planifiés` / `JH consommés` |
