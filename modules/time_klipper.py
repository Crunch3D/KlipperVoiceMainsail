import requests
import json
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'IP de l'imprimante depuis .env
PRINTER_IP = os.getenv('PRINTER_IP', '192.168.1.130')  # IP par défaut si non configurée
PRINTER_PORT = os.getenv('PRINTER_PORT', '7125')  # Port par défaut

def format_seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours)} heures, {int(minutes)} minutes et {int(seconds)} secondes"

def time_klipper(klipper_ip=None, port=None):
    if klipper_ip is None:
        klipper_ip = PRINTER_IP
    if port is None:
        port = PRINTER_PORT
        
    url = f"http://{klipper_ip}:{port}/printer/objects/query"
    headers = {'Content-Type': 'application/json'}
    data = {
        'objects': {
            'heater_bed': None,
            'extruder': None,
            'print_stats': None,
            'toolhead': None,
            'display_status': None,
            'virtual_sdcard': None,
            'gcode_move': None
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            data = response.json()
            print_stats = data.get('result', {}).get('status', {}).get('print_stats', {})
            display_status = data.get('result', {}).get('status', {}).get('display_status', {})
            
            # Afficher les données pour le débogage
            print(f"État de l'impression : {print_stats.get('state')}")
            print(f"Progression : {display_status.get('progress')}")
            print(f"Durée d'impression : {print_stats.get('print_duration')}")
            
            if print_stats.get('state') == 'printing' and display_status.get('progress', 0) > 0:
                print_duration = print_stats.get('print_duration', 0)
                progress = display_status.get('progress')
                remaining_time = (print_duration / progress) - print_duration
                remaining_time_formatted = format_seconds_to_hms(remaining_time)
                return remaining_time_formatted
            else:
                return "L'imprimante n'est pas en cours d'impression ou la progression est nulle."
        else:
            return f"Échec de la requête HTTP : Statut {response.status_code}"
    except Exception as e:
        return f"Une erreur est survenue : {e}"
