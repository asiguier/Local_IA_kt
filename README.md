# Kill Team IA

Assistant IA local pour le jeu de figurines **Kill Team** (Games Workshop). Le projet expose les règles du jeu (actions universelles, règles spéciales d'armes, séquences) via une API Flask, et fournit les règles condensées en Markdown pour un pipeline RAG basé sur Ollama + Open WebUI.

## Architecture

- **Ollama** — moteur LLM local (modèle `mistral`)
- **nomic-embed-text** — modèle d'embeddings pour le RAG
- **Open WebUI** — interface de chat
- **Flask** (`serveur_kt.py`) — API de recherche fuzzy sur les règles structurées (JSON)
- **Markdown** (`core_rules/`) — règles condensées indexées par le RAG

## Prérequis

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)
- [Ollama](https://ollama.com/) avec les modèles :
  - `mistral`
  - `nomic-embed-text`

## Installation

```bash
uv venv
uv pip install -r requirements.txt
```

Ou directement :

```bash
uv pip install flask thefuzz python-Levenshtein
```

## Lancement

```bash
KT_JSON_DIR=./json uv run serveur_kt.py
```

Le serveur écoute par défaut sur `http://localhost:5001`.

### Endpoints

- `GET /recherche?q=<question>` — recherche unifiée (actions / armes)
- `GET /recherche-multiple?q=<question>` — recherche plusieurs règles dans une même question
- `GET /sante` — état du serveur

Exemples :

```bash
curl "http://localhost:5001/recherche?q=repositionnement"
curl "http://localhost:5001/recherche?q=brutale"
curl "http://localhost:5001/recherche-multiple?q=que%20sont%20choc%20et%20deflagration"
```

## Structure

```
.
├── serveur_kt.py           # API Flask
├── json/                   # Règles structurées (actions, armes, séquences)
│   ├── actions_universelles.json
│   ├── regles_armes.json
│   └── sequences.json
├── core_rules/             # Règles condensées en Markdown (RAG)
│   ├── 01_tournants.md
│   ├── 02_actions.md
│   └── ...
├── scripts/                # Outils d'extraction PDF → Markdown
│   ├── pdf_extract_page.py
│   ├── pdf_extract_document.py
│   └── split_markdown.py
└── requirements.txt
```

## Configuration

- `KT_JSON_DIR` — chemin vers le dossier `json/` (par défaut : `./json` à côté de `serveur_kt.py`)
