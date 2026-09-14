# 1 · Modèle de données

## Hypothèse métier retenue

Les libellés de la maquette sont symboliques, mais leur vocabulaire est cohérent
et non ambigu : *Tribu*, *Squad*, *Ressource*, *JH*, *Externe / Interne*,
*ADC / PU*, *FTE*, *Société*, *Portfolio*, *DMND*, *budget K€*.

→ **Scénario retenu : pilotage de la capacité et du portefeuille d'une DSI.**

Si ce cadrage ne correspond pas au besoin réel, rien n'est perdu : seuls les
*libellés* changent. La structure du modèle, les mesures et le montage des
visuels restent identiques.

## Date de référence

La maquette affiche « Dernière actualisation : 08/09/2026 » et le graphe mensuel
s'effondre après août. Le jeu de données reproduit exactement cela :

| | |
|---|---|
| Période couverte | 01/01/2025 → 31/12/2026 |
| Réalisé | jusqu'au 31/08/2026 |
| Planifié seul | à partir du 01/09/2026 |
| Année du rapport | 2026 (valeur du FILTRE_01) |

## Schéma en étoile

```
                    D_Calendrier
                         │
        D_Tribu ─┐       │       ┌─ D_Portfolio
        D_Squad ─┤       │       │
      D_Societe ─┼── F_Charge ───┤
     D_Ressource ┘   F_Effectif  └─ D_Objet ── D_Statut
                     F_Budget
```

## Tables

### Dimensions

| Table | Lignes | Clé | Contenu |
|---|---:|---|---|
| `D_Calendrier` | 730 | `Date` | Jour, mois, trimestre, année, jour ouvré, passé/futur |
| `D_Tribu` | 12 | `TribuID` | Tribu A → L, domaine, ordre d'affichage |
| `D_Squad` | 60 | `SquadID` | 5 squads par tribu |
| `D_Societe` | 7 | `SocieteID` | Société A → F + Interne |
| `D_Ressource` | 1 510 | `ResID` | Type, profil, dates d'entrée/sortie, TJM, coût, FTE |
| `D_Portfolio` | 18 | `PortfolioID` | Portfolio 01 → 18, segment Run / Build / Transformation |
| `D_Objet` | 567 | `ObjetID` | 547 demandes + 20 projets de maintenance |
| `D_Statut` | 7 | `StatutID` | Statut, ordre, couleur |

### Faits

| Table | Lignes | Grain | Mesures portées |
|---|---:|---|---|
| `F_Charge` | 50 663 | mois × ressource × objet | JH planifiés, JH consommés, coût |
| `F_Budget` | 12 715 | mois × objet | budget initial, engagé, consommé, reste à faire |
| `F_Effectif` | 30 125 | mois × ressource | présence, FTE |

> **Pourquoi trois tables de faits et pas une seule ?**
> Compter des ressources et sommer des JH ne se font pas au même grain.
> Avec une seule table, chaque KPI d'effectif imposerait un `DISTINCTCOUNT`
> sur 50 000 lignes, et le moindre filtre sur un objet fausserait le compte.
> `F_Effectif` isole la photo mensuelle de l'effectif : les KPI des pages
> Capacité et Ressources deviennent de simples sommes.

## Relations à créer

| De | Vers | Cardinalité | Sens du filtre |
|---|---|---|---|
| `F_Charge[Date]` | `D_Calendrier[Date]` | ∗ → 1 | simple |
| `F_Charge[ResID]` | `D_Ressource[ResID]` | ∗ → 1 | simple |
| `F_Charge[ObjetID]` | `D_Objet[ObjetID]` | ∗ → 1 | simple |
| `F_Effectif[Date]` | `D_Calendrier[Date]` | ∗ → 1 | simple |
| `F_Effectif[ResID]` | `D_Ressource[ResID]` | ∗ → 1 | simple |
| `F_Budget[Date]` | `D_Calendrier[Date]` | ∗ → 1 | simple |
| `F_Budget[ObjetID]` | `D_Objet[ObjetID]` | ∗ → 1 | simple |
| `D_Ressource[TribuID]` | `D_Tribu[TribuID]` | ∗ → 1 | simple |
| `D_Ressource[SquadID]` | `D_Squad[SquadID]` | ∗ → 1 | simple |
| `D_Ressource[SocieteID]` | `D_Societe[SocieteID]` | ∗ → 1 | simple |
| `D_Objet[PortfolioID]` | `D_Portfolio[PortfolioID]` | ∗ → 1 | simple |
| `D_Objet[StatutID]` | `D_Statut[StatutID]` | ∗ → 1 | simple |
| `D_Objet[TribuID]` | `D_Tribu[TribuID]` | ∗ → 1 | **inactive** |
| `D_Squad[TribuID]` | `D_Tribu[TribuID]` | ∗ → 1 | simple |

**Deux chemins mènent de `D_Tribu` aux faits** : par la ressource qui consomme,
et par la tribu propriétaire de l'objet. Power BI refusera le second en actif
(ambiguïté). Laissez-le **inactif** : la page Demandes l'active au besoin via
`USERELATIONSHIP`. La règle est simple — page Capacité et page Ressources
raisonnent *tribu de la ressource*, pages Demandes et Projets raisonnent
*tribu de l'objet*.

## Point de vigilance : grain mensuel

Les trois tables de faits sont au mois, stockées au **1er du mois**. La relation
vers un calendrier journalier fonctionne, et toute l'intelligence temporelle au
niveau mois / trimestre / année est exacte.

**En revanche, ne proposez jamais de segment au jour** : filtrer sur le 15 mars
renverrait une valeur vide. Dans la hiérarchie de dates, n'exposez que
Année → Trimestre → Mois.
