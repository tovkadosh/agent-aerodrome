import os
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")

SCHEMA = """
Tables disponibles :

avions (id, immatriculation, modele, compagnie)
vols (id, numero_vol, avion_id, origine, destination, heure_depart, statut)
pistes (id, numero, longueur_m, etat)

vols.avion_id correspond à avions.id
"""

def generer_sql(question):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""Tu es un générateur de requêtes SQL pour une base SQLite.

Voici le schéma de la base de données :
{SCHEMA}

Question de l'utilisateur : "{question}"

Réponds UNIQUEMENT avec la requête SQL, sans explication, sans markdown, sans ```sql```.
"""
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    sql = response.json()["choices"][0]["message"]["content"]
    return sql.strip()

def executer_sql(sql):
    conn = sqlite3.connect("aerodrome2.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    resultats = cursor.fetchall()
    conn.close()
    return resultats

def reformuler_reponse(question, resultats):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""L'utilisateur a demandé : "{question}"

Voici les résultats bruts de la base de données : {resultats}

Réponds en une ou deux phrases claires en français, comme si tu parlais à un humain. Ne mentionne pas de SQL."""
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"].strip()

def poser_question(question):
    sql = generer_sql(question)
    resultats = executer_sql(sql)
    reponse = reformuler_reponse(question, resultats)
    return reponse

if __name__ == "__main__":
    question = "Quels sont les vols retardés ?"
    print(poser_question(question))