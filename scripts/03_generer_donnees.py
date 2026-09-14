# -*- coding: utf-8 -*-
"""
Genere le jeu de donnees complet du tableau de bord (modele en etoile).

Contexte simule : pilotage de la capacite et du portefeuille d'une DSI.
Date de reference : 08/09/2026 -- le realise s'arrete fin aout 2026,
les mois suivants ne portent que du planifie. C'est ce qui produit la
"chute" de fin d'annee visible sur VISUEL_02 de la maquette.

Sortie : donnees/*.csv (separateur ';', encodage UTF-8 BOM, decimal ',')
"""
import csv
import datetime as dt
import pathlib
import random

random.seed(20260908)

SORTIE = pathlib.Path("donnees")
SORTIE.mkdir(parents=True, exist_ok=True)

DATE_REF = dt.date(2026, 9, 8)
DEBUT = dt.date(2025, 1, 1)
FIN = dt.date(2026, 12, 31)
DERNIER_MOIS_REALISE = dt.date(2026, 8, 1)

MOIS_LONG = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
             "août", "septembre", "octobre", "novembre", "décembre"]
MOIS_COURT = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
              "Juil", "Août", "Sept", "Oct", "Nov", "Déc"]
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def ecrire(nom, entetes, lignes):
    chemin = SORTIE / nom
    with chemin.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(entetes)
        w.writerows(lignes)
    print(f"  {nom:<22} {len(lignes):>7} lignes")


def nombre(valeur, decimales=2):
    """Format francais : virgule decimale, pas de separateur de milliers."""
    return f"{valeur:.{decimales}f}".replace(".", ",")


def mois_entre(debut, fin):
    courant = dt.date(debut.year, debut.month, 1)
    while courant <= fin:
        yield courant
        courant = dt.date(courant.year + (courant.month == 12),
                          courant.month % 12 + 1, 1)


# --------------------------------------------------------------------------
# 1. D_Calendrier
# --------------------------------------------------------------------------
lignes = []
jour = DEBUT
while jour <= FIN:
    ferie = (jour.month, jour.day) in {(1, 1), (5, 1), (5, 8), (7, 14),
                                       (8, 15), (11, 1), (11, 11), (12, 25)}
    ouvre = jour.weekday() < 5 and not ferie
    lignes.append([
        jour.isoformat(), jour.year, f"T{(jour.month - 1) // 3 + 1}",
        jour.month, MOIS_LONG[jour.month - 1], MOIS_COURT[jour.month - 1],
        f"{jour.year}-{jour.month:02d}", jour.year * 100 + jour.month,
        jour.day, JOURS[jour.weekday()], 1 if ouvre else 0,
        1 if jour <= DATE_REF else 0,
    ])
    jour += dt.timedelta(days=1)
ecrire("D_Calendrier.csv",
       ["Date", "Annee", "Trimestre", "MoisNum", "MoisNom", "MoisAbrege",
        "AnneeMois", "AnneeMoisTri", "Jour", "JourSemaine", "EstJourOuvre",
        "EstPasse"], lignes)

# --------------------------------------------------------------------------
# 2. D_Tribu / D_Squad
# --------------------------------------------------------------------------
DOMAINES = ["Digital", "Data", "Infrastructure", "Métier", "Transverse"]
tribus = []
for i in range(1, 13):
    tribus.append([f"T{i:02d}", f"Tribu {chr(64 + i)}", DOMAINES[(i - 1) % 5], i])
ecrire("D_Tribu.csv", ["TribuID", "Tribu", "Domaine", "OrdreTribu"], tribus)

squads = []
for tribu_id, *_ in tribus:
    for s in range(1, 6):
        squads.append([f"{tribu_id}-S{s:02d}", f"Squad {s:02d}", tribu_id])
ecrire("D_Squad.csv", ["SquadID", "Squad", "TribuID"], squads)

# --------------------------------------------------------------------------
# 3. D_Societe
# --------------------------------------------------------------------------
societes = [
    ["SOC01", "Société A", "Externe", 0.30],
    ["SOC02", "Société B", "Externe", 0.16],
    ["SOC03", "Société C", "Externe", 0.11],
    ["SOC04", "Société D", "Externe", 0.06],
    ["SOC05", "Société E", "Externe", 0.045],
    ["SOC06", "Société F", "Externe", 0.035],
    ["SOC99", "Interne",   "Interne", 0.29],
]
ecrire("D_Societe.csv", ["SocieteID", "Société", "TypeFournisseur"],
       [s[:3] for s in societes])

# --------------------------------------------------------------------------
# 4. D_Ressource  -- 1 510 ressources
# --------------------------------------------------------------------------
NB_RESSOURCES = 1510
# Repartition cible (coherente avec les KPI de la page Ressources)
TYPES = ([("Externe", "ADC")] * 760 + [("Externe", "PU")] * 266
         + [("Interne", "Interne")] * 399 + [("Alternant", "Alternant")] * 82
         + [("Stagiaire", "Stagiaire")] * 3)
random.shuffle(TYPES)

poids_soc_ext = [s[3] for s in societes[:6]]
soc_ext = [s[0] for s in societes[:6]]
# Les tribus sont volontairement desequilibrees : la maquette montre une
# decroissance marquee du nombre de ressources par tribu.
poids_tribu = [0.155, 0.150, 0.135, 0.115, 0.085, 0.070, 0.060, 0.055,
               0.050, 0.045, 0.045, 0.035]

ressources = []
for i in range(1, NB_RESSOURCES + 1):
    type_res, profil = TYPES[i - 1]
    tribu = random.choices([t[0] for t in tribus], weights=poids_tribu)[0]
    squad = f"{tribu}-S{random.randint(1, 5):02d}"
    societe = random.choices(soc_ext, weights=poids_soc_ext)[0] if type_res == "Externe" else "SOC99"
    entree = DEBUT + dt.timedelta(days=random.randint(-900, 500))
    # 22 % des ressources ont une date de sortie dans la periode
    sortie = ""
    if random.random() < 0.22:
        sortie = (max(entree, DEBUT) + dt.timedelta(days=random.randint(120, 900))).isoformat()
    tjm = {"ADC": (480, 780), "PU": (620, 980), "Interne": (390, 620),
           "Alternant": (180, 260), "Stagiaire": (90, 140)}[profil]
    tjm = random.randint(*tjm)
    ressources.append([
        f"RES{i:04d}", f"Ressource {i:04d}", tribu, squad, societe,
        type_res, profil, entree.isoformat(), sortie,
        tjm, nombre(tjm * random.uniform(1.05, 1.35), 0),
        nombre(random.uniform(0.62, 1.0), 4),
        nombre(random.uniform(0.0, 0.19), 4),
        nombre(random.choice([1.0, 1.0, 1.0, 0.8, 0.6, 0.5]), 2),
    ])
ecrire("D_Ressource.csv",
       ["ResID", "Ressource", "TribuID", "SquadID", "SocieteID", "TypeRessource",
        "Profil", "DateEntree", "DateSortie", "TJM_EUR", "CoutJournalier_EUR",
        "TauxActivite", "TauxAbsence", "FTE"], ressources)

# --------------------------------------------------------------------------
# 5. D_Portfolio
# --------------------------------------------------------------------------
SEGMENTS = ["Run", "Build", "Transformation"]
portfolios = [[f"PF{i:02d}", f"Portfolio {i:02d}", SEGMENTS[(i - 1) % 3], i]
              for i in range(1, 19)]
ecrire("D_Portfolio.csv", ["PortfolioID", "Portfolio", "Segment", "OrdrePortfolio"],
       portfolios)

# --------------------------------------------------------------------------
# 6. D_Statut
# --------------------------------------------------------------------------
statuts = [
    ["ST1", "À cadrer",   1, "#E8734A"],
    ["ST2", "Cadré",      2, "#E0B23A"],
    ["ST3", "En cours",   3, "#0B2A5B"],
    ["ST4", "En recette", 4, "#5B3F8F"],
    ["ST5", "Livré",      5, "#2E9E8F"],
    ["ST6", "Suspendu",   6, "#D9534F"],
    ["ST7", "Abandonné",  7, "#9CA3AF"],
]
ecrire("D_Statut.csv", ["StatutID", "Statut", "OrdreStatut", "CouleurStatut"], statuts)
poids_statut = [0.03, 0.02, 0.64, 0.07, 0.19, 0.03, 0.02]

# --------------------------------------------------------------------------
# 7. D_Objet : demandes (547) + projets de maintenance (20)
#    Une seule dimension pour les deux : les pages 4 et 5 partagent
#    exactement les memes visuels, seul le perimetre change.
# --------------------------------------------------------------------------
PRIORITES = ["P1 · Critique", "P2 · Haute", "P3 · Moyenne", "P4 · Basse"]
objets = []

for i in range(1, 548):
    pf = random.choices(portfolios, weights=[1.4 if p[2] == "Build" else 1.0
                                             for p in portfolios])[0][0]
    st = random.choices(statuts, weights=poids_statut)[0]
    objets.append([
        f"DMND{i:07d}", f"Demande {i:03d}", "Demande", pf,
        random.choices([t[0] for t in tribus], weights=poids_tribu)[0],
        st[0], random.choices(PRIORITES, weights=[0.08, 0.27, 0.45, 0.20])[0],
        (DEBUT + dt.timedelta(days=random.randint(-400, 550))).isoformat(),
    ])

for i in range(1, 21):
    st = random.choices(statuts, weights=poids_statut)[0]
    objets.append([
        f"PRO{i:07d}", f"Maint-Projet {i:02d}", "Projet de maintenance",
        portfolios[(i - 1) % 18][0],
        random.choices([t[0] for t in tribus], weights=poids_tribu)[0],
        st[0], random.choices(PRIORITES, weights=[0.15, 0.35, 0.40, 0.10])[0],
        (DEBUT + dt.timedelta(days=random.randint(-400, 300))).isoformat(),
    ])
ecrire("D_Objet.csv",
       ["ObjetID", "Objet", "TypeObjet", "PortfolioID", "TribuID", "StatutID",
        "Priorite", "DateCreation"], objets)

# --------------------------------------------------------------------------
# 8. F_Charge : le fait principal, au grain mois x ressource x objet
# --------------------------------------------------------------------------
# Saisonnalite : creux marque en aout et en decembre, pic au printemps.
SAISON = {1: 0.96, 2: 0.95, 3: 1.14, 4: 1.18, 5: 0.92, 6: 1.06,
          7: 1.02, 8: 0.44, 9: 1.08, 10: 1.10, 11: 1.05, 12: 0.78}

jours_ouvres_mois = {}
for m in mois_entre(DEBUT, FIN):
    n, j = 0, m
    while j.month == m.month:
        ferie = (j.month, j.day) in {(1, 1), (5, 1), (5, 8), (7, 14),
                                     (8, 15), (11, 1), (11, 11), (12, 25)}
        if j.weekday() < 5 and not ferie:
            n += 1
        j += dt.timedelta(days=1)
    jours_ouvres_mois[m] = n

objets_par_tribu = {}
for o in objets:
    objets_par_tribu.setdefault(o[4], []).append(o)

mois_liste = list(mois_entre(DEBUT, FIN))
charge = []
for res in ressources:
    (res_id, _, tribu, squad, societe, type_res, profil, entree, sortie,
     tjm, cout, tx_act, tx_abs, fte) = res
    entree_m = dt.date.fromisoformat(entree).replace(day=1)
    sortie_m = dt.date.fromisoformat(sortie).replace(day=1) if sortie else None
    cout_j = float(cout.replace(",", "."))
    tx_act_f = float(tx_act.replace(",", "."))
    fte_f = float(fte.replace(",", "."))
    candidats = objets_par_tribu.get(tribu) or objets
    portee = random.sample(candidats, k=min(len(candidats), random.choice([1, 1, 2, 2, 3])))
    for m in mois_liste:
        if m < entree_m or (sortie_m and m > sortie_m):
            continue
        realise = m <= DERNIER_MOIS_REALISE
        recul = (m.year - DERNIER_MOIS_REALISE.year) * 12 + m.month - DERNIER_MOIS_REALISE.month
        for objet in portee:
            base = jours_ouvres_mois[m] * fte_f * tx_act_f * SAISON[m.month] / len(portee)
            planifie = base * random.uniform(0.85, 1.15)
            if realise:
                consomme = planifie * random.uniform(0.78, 1.12)
            else:
                # Au-dela du dernier mois realise : rien de consomme, et le
                # planifie s'etiole. C'est ce qui cree la chute de fin d'annee.
                consomme = 0.0
                planifie *= max(0.0, 1.0 - 0.28 * recul)
            if planifie < 0.05 and consomme < 0.05:
                continue
            charge.append([
                m.isoformat(), res_id, objet[0], objet[3], tribu,
                nombre(planifie, 2), nombre(consomme, 2),
                nombre(consomme * cout_j, 2), nombre(planifie * cout_j, 2),
            ])
ecrire("F_Charge.csv",
       ["Date", "ResID", "ObjetID", "PortfolioID", "TribuID",
        "JH_Planifies", "JH_Consommes", "Cout_Consomme_EUR", "Cout_Planifie_EUR"],
       charge)

# --------------------------------------------------------------------------
# 9. F_Budget : au grain mois x objet
# --------------------------------------------------------------------------
# Budget initial tire par objet, puis etale sur sa fenetre d'activite.
consomme_par_objet = {}
for ligne in charge:
    consomme_par_objet.setdefault(ligne[2], {})
    consomme_par_objet[ligne[2]][ligne[0]] = (
        consomme_par_objet[ligne[2]].get(ligne[0], 0.0)
        + float(ligne[7].replace(",", "."))
    )

budget = []
for objet in objets:
    objet_id, _, type_objet, pf, tribu, statut, priorite, _ = objet
    mois_objet = consomme_par_objet.get(objet_id, {})
    if not mois_objet:
        continue
    total_consomme = sum(mois_objet.values())
    # Le budget initial encadre le consomme : certains objets derapent,
    # d'autres sous-consomment. C'est ce qui rend VISUEL_08 (% budget) lisible.
    facteur = random.uniform(0.72, 1.45)
    total_initial = total_consomme * facteur if total_consomme else random.uniform(5e4, 4e5)
    for mois, montant in sorted(mois_objet.items()):
        part = montant / total_consomme if total_consomme else 0
        initial = total_initial * part
        budget.append([
            mois, objet_id, pf, tribu,
            nombre(initial, 2),
            nombre(initial * random.uniform(0.88, 1.06), 2),
            nombre(montant, 2),
            nombre(max(0.0, initial - montant), 2),
        ])
ecrire("F_Budget.csv",
       ["Date", "ObjetID", "PortfolioID", "TribuID", "Budget_Initial_EUR",
        "Budget_Engage_EUR", "Budget_Consomme_EUR", "Reste_A_Faire_EUR"], budget)

# --------------------------------------------------------------------------
# 10. F_Effectif : photo mensuelle de l'effectif (presence 0/1)
#     Table separee car "compter des ressources" et "sommer des JH" ne se
#     font pas sur le meme grain : sans elle, les KPI d'effectif obligent
#     a des DISTINCTCOUNT couteux sur F_Charge.
# --------------------------------------------------------------------------
effectif = []
for res in ressources:
    res_id, _, tribu, squad, societe, type_res, profil = res[:7]
    entree_m = dt.date.fromisoformat(res[7]).replace(day=1)
    sortie_m = dt.date.fromisoformat(res[8]).replace(day=1) if res[8] else None
    fte_f = float(res[13].replace(",", "."))
    for m in mois_liste:
        if m < entree_m or (sortie_m and m > sortie_m):
            continue
        effectif.append([m.isoformat(), res_id, tribu, squad, societe,
                         type_res, profil, 1, nombre(fte_f, 2)])
ecrire("F_Effectif.csv",
       ["Date", "ResID", "TribuID", "SquadID", "SocieteID", "TypeRessource",
        "Profil", "Present", "FTE"], effectif)

print("\nControles de coherence")
print(f"  ressources                 : {len(ressources)}")
tot_jh = sum(float(l[6].replace(',', '.')) for l in charge)
tot_eur = sum(float(l[7].replace(',', '.')) for l in charge)
print(f"  JH consommes (2025+2026)   : {tot_jh:,.0f}".replace(",", " "))
print(f"  Cout consomme              : {tot_eur/1000:,.0f} K EUR".replace(",", " "))
jh_2026 = sum(float(l[6].replace(',', '.')) for l in charge if l[0].startswith("2026"))
print(f"  JH consommes 2026          : {jh_2026:,.0f}".replace(",", " "))
actifs_2026 = {l[1] for l in effectif if l[0].startswith("2026")}
print(f"  ressources actives en 2026 : {len(actifs_2026)}")
