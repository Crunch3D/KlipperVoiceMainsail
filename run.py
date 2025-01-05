import os
import sys
import speech_recognition as sr
import pyttsx3
from modules.voice_commands import handle_voice_command_print

# Initialisation de la synthèse vocale
engine = pyttsx3.init()

def speak(text):
    """Prononce le texte donné."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Écoute la commande vocale."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Écoute en cours... Parlez maintenant.")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="fr-FR")
            print(f"Vous avez dit : {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Je n'ai pas compris.")
            return None
        except sr.RequestError as e:
            print(f"Erreur avec le service de reconnaissance vocale : {e}")
            return None
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            return None

def main():
    """Boucle principale pour l'écoute et le traitement des commandes."""
    print("Système prêt. Dites une commande...")
    while True:
        command = listen()
        if command:
            handle_voice_command_print(command, None)  # Aucun UI pour le moment
        if command == "arrête" or command == "stop":
            speak("Arrêt du programme.")
            break

if __name__ == "__main__":
    main()
