"""
Extraction PDF → Markdown (v6)
- Saute les pages de sommaire
- Fusionne les actions en début de page
- Convertit les légendes d'images en blockquotes
Prérequis : uv pip install pdfplumber
"""

import re
import pdfplumber

PDF    = "./../PDF/Rules/Règles condensées - Juillet 2025.pdf"
SORTIE = "regles_condensees.md"

# ── Couleurs ──────────────────────────────────────────────────────
COULEUR_EFFET     = (0.2196, 0.4627, 0.1137)
COULEUR_CONDITION = (0.8, 0.0, 0.0)
SEUIL             = 0.01

def couleurs_proches(c1, c2):
    return all(abs(a - b) < SEUIL for a, b in zip(c1, c2))

def construire_map_fleches(page):
    remplacements = []
    for c in page.chars:
        if c["text"] == "▶":
            couleur = c.get("non_stroking_color", ())
            if isinstance(couleur, (list, tuple)):
                if couleurs_proches(couleur, COULEUR_EFFET):
                    remplacements.append("→")
                elif couleurs_proches(couleur, COULEUR_CONDITION):
                    remplacements.append("⚠")
                else:
                    remplacements.append("▶")
            else:
                remplacements.append("▶")
    return remplacements

def appliquer_remplacements(texte, remplacements):
    iter_rempl = iter(remplacements)
    return re.sub(r'▶', lambda m: next(iter_rempl, "▶"), texte)

# ── Détection de page sommaire ────────────────────────────────────
def est_page_sommaire(page):
    """Vrai si >30% des lignes contiennent des points de suspension."""
    texte = page.extract_text() or ""
    lignes = [l for l in texte.split("\n") if l.strip()]
    if not lignes:
        return False
    lignes_avec_points = sum(1 for l in lignes if "......" in l)
    return lignes_avec_points / len(lignes) > 0.3

# ── Détection des légendes d'images ──────────────────────────────
def extraire_legendes(page):
    """
    Les légendes d'images sont dans des tableaux à 2 colonnes
    où la première colonne est vide (image) et la seconde contient du texte.
    Retourne un set des textes de légende.
    """
    legendes = set()
    for tableau in page.find_tables():
        data = tableau.extract()
        if not data or len(data[0]) != 2:
            continue
        for ligne in data:
            col0 = (ligne[0] or "").strip()
            col1 = (ligne[1] or "").strip()
            # Colonne gauche vide + colonne droite avec texte = légende d'image
            if not col0 and col1 and len(col1) > 10:
                # Ajouter chaque phrase de la légende
                for phrase in col1.split("\n"):
                    phrase = phrase.strip()
                    if phrase:
                        legendes.add(phrase[:60])  # clé partielle pour matching
    return legendes

# ── Helpers ───────────────────────────────────────────────────────
def est_titre_principal(texte):
    t = texte.strip()
    return t.isupper() and len(t) > 2 and not t.replace(" ", "").isdigit()

def est_cout_pa(texte):
    return bool(re.match(r'^\d+ PA$', texte.strip()))

def est_nom_action(texte):
    return bool(re.match(r'^[A-ZÀÂÄÉÈÊËÎÏÔÙÛÜŒ\s\-]+ \d+ PA$', texte.strip()))

def nettoyer_ligne(texte):
    texte = re.sub(r'\s+', ' ', texte).strip()
    if re.match(r'^\d{1,2}$', texte):
        return None
    if len(texte) < 2:
        return None
    return texte

def est_debut_liste(texte):
    return texte.rstrip().endswith(":")

def est_element_liste(texte):
    return texte.startswith(("●", "- ", "→", "⚠"))

def est_legende(ligne, legendes):
    """Vérifie si une ligne correspond à une légende d'image."""
    for cle in legendes:
        if ligne.startswith(cle[:40]):
            return True
    return False

# ── Conversion ────────────────────────────────────────────────────
def convertir_page_en_markdown(page, premiere_page=False):
    lignes_md = []
    remplacements = construire_map_fleches(page)
    legendes = extraire_legendes(page)

    # Texte brut
    texte_brut = page.extract_text() or ""
    texte_brut = appliquer_remplacements(texte_brut, remplacements)
    lignes_brutes = [nettoyer_ligne(l) for l in texte_brut.split("\n")]
    lignes_brutes = [l for l in lignes_brutes if l]  # retirer les None

    premiere_ligne         = True
    dans_sous_liste        = False
    dans_action            = False
    continuation_sous_liste = False

    i = 0
    while i < len(lignes_brutes):
        lg = lignes_brutes[i]

        # ── Premier titre de la page ─────────────────────────────
        if premiere_ligne and est_titre_principal(lg):
            premiere_ligne = False
            # Regarder si la ligne suivante est un coût PA → c'est une action
            suite = lignes_brutes[i + 1] if i + 1 < len(lignes_brutes) else ""
            if est_cout_pa(suite):
                lignes_md.append(f"\n### {lg} — {suite}\n")
                dans_action = True
                i += 2
                continue
            # Sinon : # uniquement pour la première page, ## pour les autres
            niveau = "#" if premiere_page else "##"
            lignes_md.append(f"{niveau} {lg}\n")
            i += 1
            continue
        premiere_ligne = False

        # ── Fusion titre + coût PA (action en début de page) ─────
        # Si on a un titre seul suivi d'une ligne "X PA", c'est une action
        if (est_titre_principal(lg) and not est_nom_action(lg)
                and i + 1 < len(lignes_brutes)
                and est_cout_pa(lignes_brutes[i + 1])):
            nom  = lg.strip()
            cout = lignes_brutes[i + 1].strip()
            lignes_md.append(f"\n### {nom} — {cout}\n")
            dans_sous_liste = False
            dans_action     = True
            i += 2
            continue

        # ── Légende d'image → blockquote ─────────────────────────
        if est_legende(lg, legendes):
            lignes_md.append(f"> {lg}")
            i += 1
            continue

        # ── Titre de section → ## ─────────────────────────────────
        if est_titre_principal(lg) and not est_cout_pa(lg) and not est_nom_action(lg):
            dans_sous_liste = False
            dans_action     = False
            lignes_md.append(f"\n## {lg}\n")

        # ── Nom d'action + coût → ### ────────────────────────────
        elif est_nom_action(lg):
            parts = lg.rsplit(" ", 2)
            nom  = parts[0].strip()
            cout = f"{parts[1]} {parts[2]}"
            lignes_md.append(f"\n### {nom} — {cout}\n")
            dans_sous_liste = False
            dans_action     = True

        # ── Effets → et conditions ⚠ ─────────────────────────────
        elif lg.startswith("→") or lg.startswith("⚠"):
            lignes_md.append(f"- {lg}")
            dans_sous_liste = False

        # ── Bullet ● ─────────────────────────────────────────────
        elif lg.startswith("●"):
            contenu = lg[1:].strip()
            lignes_md.append(f"- {contenu}")
            dans_sous_liste = est_debut_liste(contenu)

        # ── Tiret - ──────────────────────────────────────────────
        elif lg.startswith("- "):
            contenu = lg[2:].strip()
            if dans_sous_liste:
                lignes_md.append(f"  - {contenu}")
                continuation_sous_liste = not est_debut_liste(contenu)
            else:
                lignes_md.append(f"- {contenu}")
                continuation_sous_liste = False
            if est_debut_liste(contenu):
                dans_sous_liste = True

        # ── Texte normal ─────────────────────────────────────────
        else:
            if continuation_sous_liste:
                lignes_md.append(f"    {lg}")
            else:
                lignes_md.append(lg)
            if est_debut_liste(lg):
                dans_sous_liste = True
                continuation_sous_liste = False
            elif not est_element_liste(lg):
                continuation_sous_liste = False

        i += 1

    return "\n".join(lignes_md)

# ── Main ──────────────────────────────────────────────────────────
def main():
    print(f"📄 Extraction complète → {SORTIE}\n")

    pages_md = []
    with pdfplumber.open(PDF) as pdf:
        nb = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            print(f"  [{i+1:02d}/{nb}] Page {i+1}...", end=" ", flush=True)

            mots = page.extract_words()
            if len(mots) <= 1:
                print("(vide, ignorée)")
                continue

            if est_page_sommaire(page):
                print("(sommaire, ignoré)")
                continue

            contenu = convertir_page_en_markdown(page, premiere_page=(len(pages_md) == 0))
            if contenu.strip():
                pages_md.append(contenu)
                print("✅")
            else:
                print("(rien extrait)")

    document = "\n\n---\n\n".join(pages_md)

    with open(SORTIE, "w", encoding="utf-8") as f:
        f.write(document)

    print(f"\n✅ {SORTIE} — {len(pages_md)} pages, {len(document)} caractères")

if __name__ == "__main__":
    main()
