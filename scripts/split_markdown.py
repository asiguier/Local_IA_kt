"""
Découpage de regles_condensees.md en fichiers thématiques avec en-têtes de métadonnées.
Prérequis : aucun (stdlib uniquement)
"""

import os
import re

SOURCE = "regles_condensees.md"
DOSSIER = "core_rules"

# ── Définition des sections et de leurs métadonnées ──────────────
# Chaque entrée : (titre_h1_dans_le_md, nom_fichier, sujet, mots_cles)
SECTIONS = [
    (
        "TOURNANTS",
        "01_tournants.md",
        "Structure d'une partie Kill Team : séquence des tournants, phase de stratégie (initiative, préparation, manœuvres) et phase d'affrontement (ordres, activation des agents, actions).",
        "tournant, phase, stratégie, affrontement, initiative, préparation, manœuvre, activation, ordre, engagement, dissimulation, PC, indisponible, préparé"
    ),
    (
        "ACTIONS",
        "02a_types_actions.md",
        "Règles générales sur les actions : définition des effets (→) et conditions (⚠), types d'actions (universelle, unique, mission, gratuite) et leurs règles générales. Ne contient PAS la liste des actions universelles détaillées.",
        "action, type, universel, unique, mission, gratuit, PA, effet, condition, LPA"
    ),
    (
        "ACTIONS_UNIVERSELLES_DETAIL",
        "02b_actions_universelles.md",
        "Liste complète et détaillée de toutes les actions universelles disponibles pour tous les agents avec leur coût en PA : Repositionnement (1PA), Sprinter (1PA), Battre en retraite (2PA), Charger (1PA), Ramasser un marqueur (1PA), Placer un marqueur (1PA), Contre-attaquer (0PA), Tirer (1PA), Combattre (1PA), Garde (1PA).",
        "repositionnement, sprinter, battre en retraite, charger, ramasser marqueur, placer marqueur, contre-attaquer, tirer, combattre, garde, PA, coût, action universelle, séquence tir, séquence combat, dés attaque, dés défense"
    ),
    (
        "PRINCIPES CLÉ",
        "03_principes_cles.md",
        "Principes fondamentaux du jeu : socles, portée de contrôle, dégâts, couvert, cartes techniques, dés, relances, distances, équipements, interposé, mots-clés, marqueurs, pions, tir au dé, agents, masqué, ordres, visibilité, sol de la killzone, subterfuges, règles prioritaires.",
        "socle, portée de contrôle, dégâts, couvert, carte technique, dé, D6, D3, relance, distance, pouce, équipement, interposé, mot-clé, marqueur, pion, tir au dé, agent, masqué, ordre, engagement, dissimulation, visible, subterfuge, PC, règle prioritaire, neutralisé, blessé, estropié"
    ),
    (
        "CARTES TECHNIQUES",
        "04_cartes_techniques.md",
        "Description des cartes techniques des agents : type d'agent, caractéristiques (LPA, Mouvement, Sauvegarde, Points de Vie), caractéristiques des armes (Attaques, Dégâts, type), règles additionnelles, mots-clés et taille du socle.",
        "carte technique, LPA, mouvement, sauvegarde, points de vie, PV, attaques, dégâts normaux, dégâts critiques, arme de tir, arme de mêlée, mot-clé, socle, caractéristique"
    ),
    (
        "TERRAIN ET MOUVEMENT",
        "05_terrain_mouvement.md",
        "Règles de terrain et de mouvement : escalader, se laisser tomber, sauter. Types de terrain : Lourd, Léger, Accessible, Bloquant, Insignifiant, Exposé, Promontoire.",
        "terrain, mouvement, escalader, tomber, sauter, lourd, léger, accessible, bloquant, insignifiant, exposé, promontoire, rempart, garde-corps"
    ),
    (
        "KILLZONE : VOLKUS",
        "06_killzone_volkus.md",
        "Règles spécifiques à la killzone Volkus : types de terrain du bastion et de la grande ruine, petites ruines, gravats, règles de combat urbain, bastion exigu, garnison de bastion, action Combattre à travers une porte.",
        "killzone, volkus, bastion, grande ruine, gravats, combat urbain, bastion exigu, garnison, porte, promontoire, lourd, accessible"
    ),
    (
        "KILLZONE : GALLOWDARK",
        "07_killzone_gallowdark.md",
        "Règles spécifiques à la killzone Gallowdark : murs, écoutilles (ouvertes/fermées), combat rapproché, environnement confiné, règle En garde, actions Actionner une écoutille et Combattre à travers une écoutille.",
        "killzone, gallowdark, mur, écoutille, ouvert, fermé, actionner, combat rapproché, environnement confiné, en garde, garde, tir à bout portant, létale"
    ),
    (
        "KILLZONE : BHETA-DECIMA",
        "08_killzone_bheta_decima.md",
        "Règles spécifiques à la killzone Bheta-Decima : passerelles, condensateur thermométrique, zones dangereuses, mouvement limité, ciblage limité, équipement sur promontoire.",
        "killzone, bheta-decima, passerelle, condensateur, zone dangereuse, mouvement limité, ciblage limité, promontoire, accessible"
    ),
    (
        "SÉQUENCE DE JEU (OPÉS PRÉLIMINAIRES)",
        "09_sequence_opes_preliminaires.md",
        "Séquence de jeu pour les opérations préliminaires : mise en place, sélection des agents, placement, déroulement de la bataille et fin de partie.",
        "séquence, opé, préliminaire, mise en place, sélection, agent, placement, zone d'insertion, opé critique, PdV, victoire"
    ),
    (
        "SÉQUENCE DE JEU (OPÉS APPROUVÉES)",
        "10_sequence_opes_approuvees.md",
        "Séquence de jeu pour les opérations approuvées : mise en place, sélection des agents, placement, reconnaissance, déroulement de la bataille, opé primaire et fin de partie.",
        "séquence, opé, approuvée, mise en place, sélection, agent, placement, reconnaissance, opé primaire, opé tactique, opé critique, opé nettoyage, PdV, victoire"
    ),
    (
        "RÈGLES DES ARMES",
        "11_regles_armes.md",
        "Liste et description de toutes les règles spéciales des armes : Brutale, Choc, Déflagration, Dévastatrice, Équilibrée, Étourdissante, Fatale, Fracassante, Implacable, Inexorable, Létale, Limitée, Lourde, Perforante, Portée, Précision, Saturation, Silencieuse, Surchauffe, Torrent, Traqueuse, Vengeresse.",
        "règle arme, brutale, choc, déflagration, dévastatrice, équilibrée, étourdissante, fatale, fracassante, implacable, inexorable, létale, limitée, lourde, perforante, portée, précision, saturation, silencieuse, surchauffe, torrent, traqueuse, vengeresse, réussite critique, réussite normale, dégâts"
    ),
]

def generer_entete(nom_fichier, sujet, mots_cles):
    return f"""---
titre: {nom_fichier.replace('.md', '').replace('_', ' ').title()}
sujet: {sujet}
mots_cles: {mots_cles}
---

"""

def decouper_markdown(source, dossier, sections):
    # Lire le fichier source
    with open(source, "r", encoding="utf-8") as f:
        contenu = f.read()

    os.makedirs(dossier, exist_ok=True)

    # Découper par titres # (h1)
    parties = re.split(r'\n(?=# )', contenu)

    # Construire un dict {titre_h1: contenu}
    dict_sections = {}
    for partie in parties:
        lignes = partie.strip().split("\n")
        if lignes and lignes[0].startswith("# "):
            titre = lignes[0][2:].strip()
            dict_sections[titre] = partie.strip()

    print(f"📄 Sections trouvées dans le fichier :")
    for t in dict_sections:
        print(f"   # {t}")

    print(f"\n✂️  Découpage en cours...\n")

    nb_ok, nb_manquants = 0, 0
    for titre_md, nom_fichier, sujet, mots_cles in sections:
        if titre_md not in dict_sections:
            print(f"   ⚠️  Section non trouvée : '{titre_md}'")
            nb_manquants += 1
            continue

        entete = generer_entete(nom_fichier, sujet, mots_cles)
        contenu_section = dict_sections[titre_md]

        chemin = os.path.join(dossier, nom_fichier)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(entete + contenu_section + "\n")

        nb_mots = len(contenu_section.split())
        print(f"   ✅ {nom_fichier} ({nb_mots} mots)")
        nb_ok += 1

    print(f"\n{'='*50}")
    print(f"✅ {nb_ok} fichier(s) créé(s) dans ./{dossier}/")
    if nb_manquants:
        print(f"⚠️  {nb_manquants} section(s) non trouvée(s) — vérifiez les titres ci-dessus")

if __name__ == "__main__":
    decouper_markdown(SOURCE, DOSSIER, SECTIONS)
