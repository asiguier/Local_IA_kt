"""
Serveur unifié Kill Team - Flask + fuzzy matching
Gère : actions universelles, règles des armes (et extensible)
Prérequis : uv pip install flask thefuzz python-Levenshtein
"""

import json
import os
import re
from flask import Flask, request, jsonify
from thefuzz import fuzz, process

app = Flask(__name__)

# ── Chargement des données ────────────────────────────────────────
CATALOGUES = {}

def charger_catalogue(nom, fichier, cle_liste):
    """Charge un fichier JSON et construit son index de recherche."""
    with open(fichier, encoding="utf-8") as f:
        data = json.load(f)
    entrees = data[cle_liste]
    index = []
    for entree in entrees:
        index.append((entree["nom"].lower(), entree))
        for alias in entree.get("alias", []):
            index.append((alias.lower(), entree))
        if "nom_en" in entree:
            index.append((entree["nom_en"].lower(), entree))
        for tag in entree.get("tags", []):
            index.append((tag.lower(), entree))
    CATALOGUES[nom] = {
        "entrees": entrees,
        "index": index,
        "termes": [t for t, _ in index],
        "meta": data.get("meta", {})
    }
    print(f"   ✅ '{nom}' — {len(entrees)} entrées chargées")

JSON_DIR = os.environ.get("KT_JSON_DIR", os.path.join(os.path.dirname(__file__), "json"))

charger_catalogue("actions", os.path.join(JSON_DIR, "actions_universelles.json"), "actions")
charger_catalogue("armes",   os.path.join(JSON_DIR, "regles_armes.json"),         "regles")

# Chargement des séquences
with open(os.path.join(JSON_DIR, "sequences.json"), encoding="utf-8") as f:
    SEQUENCES = {s["id"]: s for s in json.load(f)["sequences"]}
print(f"   ✅ séquences — {len(SEQUENCES)} séquences chargées")

# ── Helpers ───────────────────────────────────────────────────────
MOTS_LISTE = ["liste", "toutes", "quelles", "quels", "différentes",
              "disponibles", "possibles", "ensemble"]

def chercher(catalogue_nom, question, seuil=60):
    """Cherche dans un catalogue et retourne (entree, score)."""
    cat = CATALOGUES[catalogue_nom]
    question = question.lower()

    # Correspondance exacte sur nom et alias uniquement (pas les tags)
    for terme, entree in cat["index"]:
        # Ignorer les tags pour la correspondance exacte
        est_tag = terme in entree.get("tags", [])
        if not est_tag and terme in question:
            return entree, 100

    # Fuzzy matching sur noms et alias uniquement
    index_sans_tags = [
        (terme, entree) for terme, entree in cat["index"]
        if terme not in entree.get("tags", [])
    ]
    termes_sans_tags = [t for t, _ in index_sans_tags]

    resultat = process.extractOne(
        question, termes_sans_tags, scorer=fuzz.partial_ratio
    )
    if resultat and resultat[1] >= seuil:
        terme_trouve = resultat[0]
        for terme, entree in index_sans_tags:
            if terme == terme_trouve:
                return entree, resultat[1]

    return None, 0

def formater_sequence(seq):
    """Formate une séquence de résolution."""
    lignes = [f"### {seq['nom']}", "", f"*{seq['intro']}*", ""]
    for e in seq["etapes"]:
        lignes.append(f"**{e['num']}. {e['nom']}**")
        lignes.append(e["detail"])
        for sr in e.get("sous_regles", []):
            lignes.append(f"  - {sr}")
        lignes.append("")
    if seq.get("note"):
        lignes.append(f"*{seq['note']}*")
    return "\n".join(lignes)

def formater_action(a):
    lignes = [f"## {a['nom']} — {a['cout_pa']} PA", ""]
    lignes.append("**Effets (→) :**")
    for e in a["effets"]:
        lignes.append(f"- → {e}")
    lignes.append("")
    lignes.append("**Conditions (⚠) :**")
    for c in a["conditions"]:
        lignes.append(f"- ⚠ {c}")
    if "fin_garde" in a:
        lignes += ["", "**Fin de la garde si :**"]
        for f in a["fin_garde"]:
            lignes.append(f"- {f}")
    if a.get("note"):
        lignes += ["", f"*{a['note']}*"]
    # Injecter la séquence si elle existe
    if "sequence_ref" in a and a["sequence_ref"] in SEQUENCES:
        lignes += ["", "---", "", formater_sequence(SEQUENCES[a["sequence_ref"]])]
    return "\n".join(lignes)

def formater_regle_arme(r):
    param = f" {r['parametre_nom']}" if r["parametre"] else ""
    return (
        f"## {r['nom']}{param} / {r['nom_en']}\n\n"
        f"{r['description']}"
    )

def formater_liste_actions():
    lignes = ["## Actions universelles\n"]
    for a in CATALOGUES["actions"]["entrees"]:
        conditions = " | ".join(a["conditions"])
        lignes.append(
            f"### {a['nom']} — {a['cout_pa']} PA\n"
            f"**Effets :** {' '.join(a['effets'])}\n"
            f"**Conditions :** {conditions}\n"
        )
    return "\n".join(lignes)

def formater_liste_armes():
    lignes = ["## Règles spéciales des armes\n"]
    for r in CATALOGUES["armes"]["entrees"]:
        param = f" {r['parametre_nom']}" if r["parametre"] else ""
        lignes.append(f"**{r['nom']}{param}** / {r['nom_en']} : {r['description']}")
    return "\n".join(lignes)

# ── Routes ────────────────────────────────────────────────────────
@app.route("/recherche", methods=["GET"])
def recherche():
    """
    Recherche unifiée.
    Paramètres :
      - q       : la question
      - categorie : 'actions' | 'armes' | 'auto' (défaut)
    """
    question   = request.args.get("q", "").strip()
    categorie  = request.args.get("categorie", "auto").strip()

    if not question:
        return jsonify({"erreur": "Paramètre 'q' manquant"}), 400

    # ── Détection automatique de la catégorie ─────────────────────
    if categorie == "auto":
        mots_armes   = ["arme", "règle arme", "weapon", "blast",
                        "perfor", "déflagration", "torrent", "brutal"]
        mots_actions = ["action", "activation", "pa ", "point d'action",
                        "repositionn", "sprinter", "charger", "combattre", "garde"]
        q = question.lower()
        if "action" in q:
            categorie = "actions"
        elif any(m in q for m in mots_armes):
            categorie = "armes"
        elif any(m in q for m in mots_actions):
            categorie = "actions"
        else:
            categorie = "actions"  # fallback

    # ── Demande de liste ──────────────────────────────────────────
    if any(m in question.lower() for m in MOTS_LISTE):
        if categorie == "armes":
            return jsonify({
                "type": "liste", "categorie": "armes",
                "reponse": formater_liste_armes(),
                "nb": len(CATALOGUES["armes"]["entrees"])
            })
        else:
            return jsonify({
                "type": "liste", "categorie": "actions",
                "reponse": formater_liste_actions(),
                "nb": len(CATALOGUES["actions"]["entrees"])
            })

    # ── Recherche dans la catégorie détectée ──────────────────────
    entree, score = chercher(categorie, question)

    if entree:
        if categorie == "actions":
            reponse = formater_action(entree)
        else:
            reponse = formater_regle_arme(entree)
        return jsonify({
            "type": "trouvee",
            "categorie": categorie,
            "nom": entree["nom"],
            "score": score,
            "reponse": reponse,
            "donnees": entree
        })

    # ── Rien trouvé — essayer l'autre catégorie ───────────────────
    autre = "armes" if categorie == "actions" else "actions"
    entree2, score2 = chercher(autre, question)
    if entree2:
        if autre == "actions":
            reponse = formater_action(entree2)
        else:
            reponse = formater_regle_arme(entree2)
        return jsonify({
            "type": "trouvee",
            "categorie": autre,
            "nom": entree2["nom"],
            "score": score2,
            "reponse": reponse,
            "donnees": entree2
        })

    return jsonify({
        "type": "non_trouve",
        "question": question,
        "reponse": (
            f"Aucune règle trouvée pour : '{question}'.\n"
            f"Actions : {', '.join(a['nom'] for a in CATALOGUES['actions']['entrees'])}.\n"
            f"Règles armes : {', '.join(r['nom'] for r in CATALOGUES['armes']['entrees'])}."
        )
    })

@app.route("/recherche-multiple", methods=["GET"])
def recherche_multiple():
    """
    Recherche plusieurs règles dans une même question.
    Paramètre : ?q=que sont choc, déflagration et fatale
    """
    question = request.args.get("q", "").strip()
    if not question:
        return jsonify({"erreur": "Paramètre 'q' manquant"}), 400

    # Construire un index global (toutes catégories confondues)
    index_global = []
    for nom_cat, cat in CATALOGUES.items():
        for entree in cat["entrees"]:
            index_global.append((entree["nom"].lower(), entree, nom_cat))
            for alias in entree.get("alias", []):
                index_global.append((alias.lower(), entree, nom_cat))
            if "nom_en" in entree:
                index_global.append((entree["nom_en"].lower(), entree, nom_cat))

    # Chercher toutes les correspondances dans la question
    question_lower = question.lower()
    resultats = {}  # nom → (entree, categorie) pour éviter les doublons

    for terme, entree, categorie in index_global:
        if terme in question_lower and entree["nom"] not in resultats:
            resultats[entree["nom"]] = (entree, categorie)

    # Si aucune correspondance exacte, essayer le fuzzy sur chaque mot
    if not resultats:
        mots = re.findall(r'\b\w{4,}\b', question_lower)  # mots de 4+ lettres
        for mot in mots:
            entree, score = chercher("actions", mot, seuil=80)
            if not entree:
                entree, score = chercher("armes", mot, seuil=80)
            if entree and entree["nom"] not in resultats:
                cat = "actions" if entree in CATALOGUES["actions"]["entrees"] else "armes"
                resultats[entree["nom"]] = (entree, cat)

    if not resultats:
        return jsonify({
            "type": "non_trouve",
            "question": question,
            "reponse": f"Aucune règle trouvée pour : '{question}'"
        })

    # Formater toutes les réponses
    reponses = []
    for nom, (entree, categorie) in resultats.items():
        if categorie == "actions":
            reponses.append(formater_action(entree))
        else:
            reponses.append(formater_regle_arme(entree))

    return jsonify({
        "type": "multiple",
        "question": question,
        "nb_resultats": len(resultats),
        "noms": list(resultats.keys()),
        "reponse": "\n\n---\n\n".join(reponses)
    })


def catalogues():
    """Liste les catalogues disponibles et leur contenu."""
    return jsonify({
        nom: {
            "nb_entrees": len(cat["entrees"]),
            "noms": [e["nom"] for e in cat["entrees"]]
        }
        for nom, cat in CATALOGUES.items()
    })

@app.route("/sante", methods=["GET"])
def sante():
    return jsonify({
        "statut": "ok",
        "catalogues": {nom: len(cat["entrees"]) for nom, cat in CATALOGUES.items()}
    })

if __name__ == "__main__":
    print(f"\n🎲 Serveur Kill Team unifié")
    for nom, cat in CATALOGUES.items():
        print(f"   {nom} : {len(cat['entrees'])} entrées")
    print(f"\n   → http://localhost:5001/recherche?q=repositionnement")
    print(f"   → http://localhost:5001/recherche?q=brutale")
    print(f"   → http://localhost:5001/recherche?q=repositionnement&categorie=actions")
    print(f"   → http://localhost:5001/catalogues\n")
    app.run(host="0.0.0.0", port=5001, debug=True)
