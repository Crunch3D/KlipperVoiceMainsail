import requests
import json
from dotenv import load_dotenv
import os
import logging

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'IP de l'imprimante depuis .env
PRINTER_IP = os.getenv('PRINTER_IP', '192.168.1.130')  # IP par défaut si non configurée
PRINTER_PORT = os.getenv('PRINTER_PORT', '7125')  # Port par défaut

# Lancement des Macros:
def execute_klipper_macro(macro_name, klipper_ip=None, port=None):
    if klipper_ip is None:
        klipper_ip = PRINTER_IP
    if port is None:
        port = PRINTER_PORT
        
    url = f"http://{klipper_ip}:{port}/printer/gcode/script"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'script': macro_name}

    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            return f"Macro {macro_name} exécutée avec succès."
        else:
            return f"Échec de l'exécution de la macro : Statut {response.status_code}"
    except Exception as e:
        return f"Une erreur est survenue lors de l'exécution de la macro : {e}"
    
# Lancement du Print:
def start_printing(klipper_ip, filename):
    url = f"http://{klipper_ip}:{PRINTER_PORT}/printer/print/start"
    headers = {'Content-Type': 'application/json'}
    data = {'filename': filename}
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Réponse de l'imprimante : {response.text}")
        return response.ok
    except Exception as e:
        print(f"Erreur lors du lancement de l'impression : {e}")
        return False

# Affichage du stl: 

def get_current_printing_filename():
    url = f"http://{PRINTER_IP}:{PRINTER_PORT}/server/printer/objects/query?webhooks&virtual_sdcard&print_stats"
    payload = {
        "objects": {
            "print_stats": None  # Vous pourriez avoir besoin de spécifier les attributs ici si nécessaire
        }
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        filename = data['result']['print_stats']['filename']
        if filename:
            return filename
        return None
    except requests.RequestException as e:
        print(f"Erreur de requête : {e}")
        return None

def get_print_stats():
    url = f"http://{PRINTER_IP}:{PRINTER_PORT}/server/printer/objects/query?webhooks&virtual_sdcard&print_stats"
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        return result.get('result', {}).get('status', {}).get('print_stats', {})
    except requests.RequestException as e:
        print(f"Erreur de requête : {e}")
        return {}
    
def get_file_metadata(filename): 
    url = f"http://{PRINTER_IP}:{PRINTER_PORT}/server/files/metadata?filename={filename}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        metadata = response.json()
        # logging.debug(f"Métadonnées reçues : {metadata}")
        return metadata.get('result', {})
    except requests.RequestException as e:
        # logging.error(f"Erreur de requête : {e}")
        print(f"Erreur de requête : {e}")
        return {}

# Visualisation du Bed_Mesh:
def get_bed_mesh_data():
    url = f"http://{PRINTER_IP}:{PRINTER_PORT}/printer/objects/query?bed_mesh"
    try:
        response = requests.get(url)
        response.raise_for_status()
        mesh_data = response.json()
        #print("Données du maillage récupérées : ", mesh_data)
        return mesh_data['result']['status']['bed_mesh']
    except requests.RequestException as e:
        print(f"Erreur de requête : {e}")
        return None

def process_mesh(bed_mesh):
    matrix = bed_mesh['probed_matrix']
    if not matrix or len(matrix) < 3 or not matrix[0] or len(matrix[0]) < 3:
        return None
    coordinates = []
    x_distance = (bed_mesh['mesh_max'][0] - bed_mesh['mesh_min'][0]) / (len(matrix[0]) - 1)
    y_distance = (bed_mesh['mesh_max'][1] - bed_mesh['mesh_min'][1]) / (len(matrix) - 1)
    y_idx = 0
    for y_axis in matrix:
        x_idx = 0
        y_coord = bed_mesh['mesh_min'][1] + (y_idx * y_distance)
        for z_coord in y_axis:
            x_coord = bed_mesh['mesh_min'][0] + (x_idx * x_distance)
            coordinates.append((x_coord, y_coord, z_coord))
            x_idx += 1
        y_idx += 1
    print("Coordonnées transformées du maillage : ", coordinates)
    return coordinates


# Jouer avec Offset:
def get_z_offset(ip):
    url = f"http://{ip}/printer/objects/query?gcode_move"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['result']['status']['gcode_move']['homing_origin'][2]
    else:
        return None
ip = PRINTER_IP  # Pour la compatibilité avec le code existant

def Z_ADJUST(ip):
    url = f"http://{ip}/printer/objects/query?gcode_move"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        z_adjust = data['result']['status']['gcode_move']['homing_origin'][2]  # Index 2 pour l'axe Z
        return z_adjust
    else:
        return "Erreur de connexion ou réponse non disponible."
