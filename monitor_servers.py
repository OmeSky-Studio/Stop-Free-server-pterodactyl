import os
import requests
import time
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les variables d'environnement
PANEL_URL = os.getenv("PANEL_URL")  # L'URL de votre panel
API_KEY = os.getenv("API_KEY")  # Votre clé API
NODE_NAME = os.getenv("NODE_NAME")  # Nom de la node
TIME_INACTIF = int(os.getenv("TIME_INACTIF", 5))  # Temps d'inactivité en minutes, par défaut 5
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
}

def get_server_resources(server_id):
    """
    Récupère les ressources d'un serveur.
    """
    url = f"{PANEL_URL}/servers/{server_id}/resources"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        stats = data.get("attributes", {}).get("resources", {})
        return {
            "cpu": stats.get("cpu_absolute", 0),  # Utilisation CPU en %
        }
    else:
        print(f"Erreur : Impossible de récupérer les ressources pour le serveur {server_id}.")
        print(f"Statut HTTP : {response.status_code}, Réponse : {response.text}")
        return None

def power_action(server_id, action):
    """
    Effectue une action d'alimentation sur le serveur (start, stop, restart).
    """
    url = f"{PANEL_URL}/servers/{server_id}/power"
    payload = {"signal": action}
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 204:
        print(f"Action '{action}' effectuée sur le serveur {server_id}.")
    else:
        print(f"Erreur : Impossible d'effectuer l'action '{action}' sur le serveur {server_id}.")
        print(f"Statut HTTP : {response.status_code}, Réponse : {response.text}")

def monitor_servers():
    """
    Surveille les performances des serveurs et éteint ceux qui n'utilisent pas plus de 50 % du CPU pendant 1 minute.
    """
    inactive_servers = {}  # Dictionnaire pour suivre l'inactivité des serveurs

    while True:
        response = requests.get(PANEL_URL, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()

            for server in data["data"]:
                server_id = server["attributes"]["identifier"]
                server_name = server["attributes"]["name"]
                server_node = server["attributes"]["node"]

                if server_node == NODE_NAME:
                    # Récupère les ressources du serveur
                    resources = get_server_resources(server_id)
                    if not resources:
                        continue

                    cpu_usage = resources["cpu"]
                    print(f"Serveur : {server_name} - CPU : {cpu_usage}%")

                    # Surveille l'utilisation du CPU
                    if cpu_usage <= 50:
                        if server_id in inactive_servers:
                            # Incrémente le temps d'inactivité
                            inactive_servers[server_id] += 10
                            print(f"Le serveur {server_name} est inactif depuis {inactive_servers[server_id]} secondes.")
                        else:
                            inactive_servers[server_id] = 10

                        # Si le serveur est inactif depuis plus de 60 secondes, éteignez-le
                        if inactive_servers[server_id] >= TIME_INACTIF * 60:
                            print(f"Éteindre le serveur {server_name} ({server_id}) pour inactivité.")
                            power_action(server_id, "stop")
                            del inactive_servers[server_id]  # Réinitialise l'état du serveur
                    else:
                        # Si le serveur devient actif, réinitialisez son état
                        if server_id in inactive_servers:
                            print(f"Le serveur {server_name} est de nouveau actif, réinitialisation de son compteur d'inactivité.")
                            del inactive_servers[server_id]

            time.sleep(10)  # Vérifiez les serveurs toutes les 10 secondes
        else:
            print(f"Erreur : Impossible de récupérer la liste des serveurs.")
            print(f"Statut HTTP : {response.status_code}, Réponse : {response.text}")
            time.sleep(10)

# Lancer la surveillance
monitor_servers()
