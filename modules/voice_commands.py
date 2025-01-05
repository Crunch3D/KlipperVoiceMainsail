from modules.speak import speak
from modules.time_klipper import time_klipper
from modules.execute_klipper_macro import process_mesh, get_bed_mesh_data, execute_klipper_macro, start_printing, get_file_metadata, get_print_stats, PRINTER_IP, PRINTER_PORT
import re
import os
import requests

def check_printer_connection():
    """Vérifie si l'imprimante est connectée et accessible."""
    try:
        response = requests.get(f"http://{PRINTER_IP}:{PRINTER_PORT}/printer/info", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_file_exists(filename):
    """Vérifie si un fichier gcode existe sur l'imprimante."""
    try:
        print(f"Recherche du fichier : {filename}")
        response = requests.get(f"http://{PRINTER_IP}:{PRINTER_PORT}/server/files/list?root=gcodes")
        if response.status_code == 200:
            files = response.json()['result']
            print("Liste des fichiers disponibles :")
            for file in files:
                if isinstance(file, dict):
                    print(f"- {file.get('filename', 'Nom inconnu')}")
                    if file.get('filename') == filename:
                        print(f"Fichier trouvé : {filename}")
                        return True
            print(f"Fichier {filename} non trouvé dans la liste")
            return False
        print(f"Erreur lors de la requête : {response.status_code}")
        return False
    except Exception as e:
        print(f"Erreur lors de la vérification du fichier : {e}")
        return False

def get_printer_state():
    """Récupère l'état actuel de l'imprimante."""
    try:
        response = requests.get(f"http://{PRINTER_IP}:{PRINTER_PORT}/printer/objects/query?print_stats")
        if response.status_code == 200:
            return response.json()['result']['status']['print_stats']['state']
        return None
    except:
        return None

def handle_voice_command_print(text, ui):
        print(f"Commande reçue : {text}")
        
        # Gestion des salutations
        if any(greeting in text.lower() for greeting in ["salut", "bonjour", "hello", "coucou"]):
            if "vz" in text.lower():
                speak("Salut Foxtrot ! Comment vas-tu ? Que veux-tu faire avec l'imprimante aujourd'hui ?", ui, emotion="excited")
            else:
                speak("Salut Fokstrott, comment vas-tu ? Que puis-je faire pour toi ?", ui, emotion="calm")
            return
        
        # Vérifier d'abord la connexion à l'imprimante pour les autres commandes
        if not check_printer_connection():
            speak("Je ne peux pas communiquer avec l'imprimante. Veuillez vérifier qu'elle est allumée et connectée au réseau.", ui, emotion="sad")
            return
        
# Temps restant à Klipper Vzbot :
        if "temps d'impression restant" in text or "temps d'impression" in text:
            remaining_time_formatted = time_klipper(PRINTER_IP, PRINTER_PORT)
            print(f"Temps restant : {remaining_time_formatted}")
            
            if "n'est pas en cours d'impression" in remaining_time_formatted:
                speak("Aucune impression n'est en cours actuellement.", ui, emotion="calm")
            elif "erreur" in remaining_time_formatted.lower():
                speak("Désolé, je n'arrive pas à obtenir le temps d'impression. Il y a peut-être un problème de connexion.", ui, emotion="sad")
            else:
                speak(f"D'après mes calculs, il reste {remaining_time_formatted} avant la fin de l'impression.", ui, emotion="thoughtful")
            
# Macro chauffe buse à 190:
        elif "active la chauffe" in text:
            if get_printer_state() == "printing":
                speak("Une impression est en cours. Je ne peux pas modifier la température de la buse maintenant.", ui, emotion="hesitant")
                return
                
            speak("Je lance la chauffe de la buse à 190 degrés. Je vous préviendrai quand la température sera atteinte.", ui, emotion="authoritative")
            macro_name = "BUSE_190"
            response = execute_klipper_macro(macro_name) 
            print(response)
            
# Macro refoidissement buse à 0:                
        elif "chauffe désactivée" in text or "chauffe désactivé" in text or "chauffe désactiver" in text or "arrête le chauffe" in text or "stop la chauffe" in text:
            if get_printer_state() == "printing":
                speak("Une impression est en cours. Je ne peux pas arrêter la chauffe maintenant.", ui, emotion="hesitant")
                return
                
            speak("J'arrête la chauffe de la buse. La température va progressivement redescendre.", ui, emotion="calm")
            macro_name = "CHAUFFE_OFF"
            response = execute_klipper_macro(macro_name)
            print(response)
            
# Macro Désactiver les moteurs:                
        elif "désactive les moteurs" in text or "désactive le moteur" in text or "désactiver les moteurs" in text:
            if get_printer_state() == "printing":
                speak("Une impression est en cours. Je ne peux pas désactiver les moteurs maintenant.", ui, emotion="hesitant")
                return
                
            speak("Les moteurs sont maintenant désactivés. Vous pouvez déplacer les axes manuellement.", ui, emotion="calm")
            macro_name = "STEPPER_OFF"
            response = execute_klipper_macro(macro_name)
            print(response)
            
# Macro Auto home:                
        elif "fais un home" in text or "fais un rhome" in text or "photos home" in text or "auto home" in text:
            if get_printer_state() == "printing":
                speak("Une impression est en cours. Je ne peux pas faire de home maintenant.", ui, emotion="hesitant")
                return
                
            speak("Je lance la procédure de home. Veuillez patienter pendant que je calibre tous les axes.", ui, emotion="authoritative")
            macro_name = "HOME_HA"
            response = execute_klipper_macro(macro_name)
            print(response)
            
# Macro Prechauffe:                
        elif "prechauffe" in text or "préchauffe" in text:
            if get_printer_state() == "printing":
                speak("Une impression est en cours. Je ne peux pas modifier les températures maintenant.", ui, emotion="hesitant")
                return
                
            speak("Je lance la procédure de préchauffage. La buse et le plateau vont monter en température.", ui, emotion="authoritative")
            macro_name = "PRECHAUFFE"
            response = execute_klipper_macro(macro_name)
            print(response)
            
# Démarrage du print:        
        elif "lance le fichier" in text:
            if get_printer_state() == "printing":
                speak("Une impression est déjà en cours. Je ne peux pas en démarrer une autre maintenant.", ui, emotion="hesitant")
                return
                
            # Extraire le nom du fichier sans l'extension
            filename_base = text.split("lance le fichier ")[-1].strip()
            filename = filename_base + ".gcode"
            print(f"Tentative de lancement du fichier : {filename}")
            
            speak(f"Je vais démarrer l'impression du fichier {filename_base} j'ai code. Je surveillerai l'avancement pour vous.", ui, emotion="excited")
            if start_printing(PRINTER_IP, filename):
                print(f"Le fichier {filename} va commencer à s'imprimer.")
            else:
                speak("Je suis désolé, mais je ne peux pas lancer l'impression. Il y a peut-être un problème avec l'imprimante.", ui, emotion="sad")
                print("Échec du démarrage de l'impression.")
                
# Macro bedmesh:
        elif "fait un mesh" in text or "meche" in text or "fais un mèche" in text:
            if get_printer_state() == "printing":
                speak("Une impression est en cours. Je ne peux pas faire de mesh maintenant.", ui, emotion="hesitant")
                return
                
            speak("Je lance le maillage du plateau. Cette opération prendra moins d'une minute pour assurer une impression parfaite.", ui, emotion="authoritative")
            macro_name = "Mesh_Print"
            response = execute_klipper_macro(macro_name)
            print(response)
            
# Macro reglage de l'offset:
        elif "offset à" in text or "offset a" in text or "règle l'offset a" in text or "règle l'offset à" in text:
            if get_printer_state() == "printing":
                speak("Une impression est en cours. Je ne peux pas modifier l'offset maintenant.", ui, emotion="hesitant")
                return
                
            match = re.search(r'(?:à|a)\s*(-?\d*\.?\d+)', text)
            if match:
                offset_value = match.group(1)
                if text.count('moins') > 0 or text.count('-') > 0:
                    offset_value = '-' + offset_value.strip()
                speak(f"Je vais ajuster l'offset Z à {offset_value} millimètres pour améliorer l'adhérence de la première couche.", ui, emotion="thoughtful")
                response = execute_klipper_macro(f"Offset_voice Z={offset_value}")
                print(response)
            else:
                print("Valeur d'offset non reconnue.")
                speak("Je n'ai pas compris la valeur de l'offset. Veuillez réessayer en précisant une valeur numérique.", ui, emotion="hesitant")
