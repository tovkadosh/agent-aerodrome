# Agent IA Aérodrome

Agent IA connecté à une base de données aéronautique via API LLM (Mistral). Permet d'interroger une base de données SQL en langage naturel et d'obtenir une réponse claire, sans écrire de SQL.

## Fonctionnement

1. L'utilisateur pose une question en français (ex: *"Quels sont les vols retardés ?"*)
2. L'agent envoie la question + le schéma de la base à l'API Mistral, qui génère la requête SQL correspondante
3. La requête est exécutée sur la base SQLite
4. Les résultats bruts sont renvoyés à Mistral pour être reformulés en une réponse naturelle
5. La réponse est retournée à l'utilisateur via une API REST (FastAPI)

## Stack technique

- **Python** — langage principal
- **FastAPI** — exposition de l'agent via une API REST
- **SQLite** — base de données aéronautique (avions, vols, pistes)
- **API Mistral** — génération de SQL et reformulation en langage naturel
- **python-dotenv** — gestion sécurisée de la clé API

## Structure du projet

```
agent-aerodrome/
├── database.py      # création de la base de données + données d'exemple
├── agent.py          # logique de l'agent (appel Mistral + exécution SQL)
├── main.py           # API FastAPI exposant l'agent
├── .env               # clé API Mistral (non versionné)
└── README.md
```

## Base de données

Trois tables :

- **avions** : id, immatriculation, modele, compagnie
- **vols** : id, numero_vol, avion_id, origine, destination, heure_depart, statut
- **pistes** : id, numero, longueur_m, etat

## Installation

```bash
pip install requests fastapi uvicorn python-dotenv
```

Créer un fichier `.env` à la racine du projet avec votre clé API Mistral :

```
MISTRAL_API_KEY=votre_clé_ici
```

## Initialiser la base de données

```bash
python database.py
```

Crée le fichier `aerodrome2.db` et y insère des données d'exemple (5 avions, 5 vols, 3 pistes).

## Lancer l'API

```bash
uvicorn main:app --reload
```

L'API est accessible sur `http://127.0.0.1:8000`. La documentation interactive (Swagger) est disponible sur `http://127.0.0.1:8000/docs`.

## Exemple d'utilisation

**Requête** : `POST /demander`

```json
{
  "texte": "Quels avions sont d'Air France ?"
}
```

**Réponse** :

```json
{
  "question": "Quels avions sont d'Air France ?",
  "reponse": "Voici deux avions d'Air France : un Airbus A320 immatriculé F-GKXA et un Airbus A350 immatriculé F-HBNA."
}
```

## Pistes d'amélioration

- Ajouter une interface web simple (formulaire HTML) pour interagir sans passer par Swagger
- Gérer les erreurs si Mistral génère une requête SQL invalide
- Étendre le schéma avec plus de tables (personnel, maintenance, météo)

## Auteur

Tov-Kadosh MABUILA TUKEBA — Étudiant Ingénieur Aéronautique, spécialisation Intelligence Artificielle (IPSA)
