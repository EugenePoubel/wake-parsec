import json
import subprocess
import os
import time


def display_loading_bar(duration, bar_length=30):
    print("Lancement de la bécane 🖥️")

    for i in range(bar_length):
        # Calculer le pourcentage de progression
        progress = (i + 1) / bar_length
        time.sleep(duration / bar_length)

        # Construire la barre de chargement
        # Le caractère "█" représente la partie remplie et le caractère " " la partie vide
        filled_length = int(round(bar_length * progress))
        bar = '█' * filled_length + ' ' * (bar_length - filled_length)

        # Afficher la barre de chargement avec le pourcentage
        print(f'\r[{bar}] {int(progress * 100)}%', end='', flush=True)

    # Afficher un retour à la ligne à la fin
    print('\n')
def wireguard_connect(config_name, system="Mac"):
    # Récuperation des informations depuis le fichier de configuration
    config_path = f"config/{config_name}.conf"

    # Lecture et chargement des données JSON
    with open(config_path, 'r') as file:
        config = json.load(file)

    # Extraction des informations de configuration
    ip = config.get('ip')
    mac = config.get('mac')
    peer_id = config.get('peer_id')
    profile_path = config.get('profile_path')

    # Vérification si le fichier de profil existe
    if not os.path.exists(profile_path):
        print(f"Erreur: le fichier {profile_path} n'existe pas.")
        return

    # Commandes pour activer et désactiver WireGuard
    up_command = ["wg-quick", "up", profile_path]
    down_command = ["wg-quick", "down", profile_path]

    try:
        # Activer le VPN
        output = subprocess.run(up_command, capture_output=True, check=True)
        print(output.stdout.decode('utf-8'))
        print(f"WireGuard connecté avec le profil !")

        # Envoie le paquet magique pour allumer l'ordinateur
        wol = ["wakeonlan", "-i", ip, mac]

        print("Wake up ! ")

        subprocess.run(wol, capture_output=True, check=True)

        # Eteindre le VPN
        subprocess.run(down_command, capture_output=True, check=True)
        print("WireGuard déconnecté.")

        display_loading_bar(60)
        print("Lancement de Parsec...")

        # Lancement de Parsec pour se connecter au PC
        if os == "Windows":
            #TODO: Rendre l'appli compatible Windows
            print("Windows n\'est pas pris en charge pour le moment.")
            exit(1)
        elif os == "Mac":
            os.system("/Applications/Parsec.app/Contents/MacOS/parsecd peer_id="+peer_id)
        return

    except subprocess.CalledProcessError as e:
        # Eteindre le VPN s'il est déjà actif
        subprocess.run(down_command, capture_output=True, check=True)
        print(f"Erreur lors de la connexion à WireGuard: {e.output.decode('utf-8')}")
        print(f"STDERR: {e.stderr.decode('utf-8')}")
        return