import pyttsx3
import pygame

# Initialisation du moteur de synthèse vocale
engine = pyttsx3.init()

def configure_voice():
    """Configure la voix pour utiliser une voix masculine en français."""
    voices = engine.getProperty('voices')
    
    # Afficher toutes les voix disponibles pour le débogage
    print("Voix disponibles:")
    for voice in voices:
        print(f"ID: {voice.id}")
        print(f"Nom: {voice.name}")
        print(f"Langues: {voice.languages}")
        print("---")
    
    # Recherche d'une voix masculine en français
    french_male_voice = None
    for voice in voices:
        name = voice.name.lower()
        # Recherche spécifique des voix masculines françaises
        if ('french' in name or 'français' in name or 'fr' in name) and \
           ('david' in name or 'paul' in name or 'male' in name or 'homme' in name):
            french_male_voice = voice
            break
    
    # Si une voix masculine française est trouvée, l'utiliser
    if french_male_voice:
        engine.setProperty('voice', french_male_voice.id)
        print(f"Voix masculine sélectionnée : {french_male_voice.name}")
    else:
        # Sinon, chercher une voix française quelconque
        for voice in voices:
            if 'french' in voice.name.lower() or 'français' in voice.name.lower() or 'fr' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                print(f"Voix française sélectionnée : {voice.name}")
                break
    
    # Configuration par défaut
    engine.setProperty('rate', 150)  # Vitesse de parole
    engine.setProperty('volume', 0.9)  # Volume
    engine.setProperty('pitch', 50)  # Ton plus grave pour une voix plus masculine

configure_voice()

def play_sound(sound_data):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_data)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def speak(text, ui=None, rate=150, emotion=None):
    """Fonction pour parler en utilisant pyttsx3 avec des ajustements pour la fluidité."""
    if ui:
        ui.activate_gif(True)
    
    # Ajustement du ton selon l'émotion
    if emotion:
        adjust_for_emotion(engine, emotion)
    
    # Dire le texte
    engine.say(text)
    engine.runAndWait()
    
    # Réinitialiser les paramètres par défaut
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.setProperty('pitch', 50)
    
    if ui:
        ui.activate_gif(False)

def is_speaking():
    """Vérifie si le moteur est en train de parler."""
    return engine.isBusy()

def adjust_for_emotion(engine, emotion):
    """Ajuste les propriétés de la voix selon l'émotion."""
    if emotion == "excited":
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        engine.setProperty('pitch', 55)
    elif emotion == "sad":
        engine.setProperty('rate', 130)
        engine.setProperty('volume', 0.7)
        engine.setProperty('pitch', 45)
    elif emotion == "hesitant":
        engine.setProperty('rate', 140)
        engine.setProperty('volume', 0.8)
        engine.setProperty('pitch', 48)
    elif emotion == "authoritative":
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.setProperty('pitch', 40)
    elif emotion == "calm":
        engine.setProperty('rate', 145)
        engine.setProperty('volume', 0.85)
        engine.setProperty('pitch', 47)
    elif emotion == "thoughtful":
        engine.setProperty('rate', 140)
        engine.setProperty('volume', 0.9)
        engine.setProperty('pitch', 45)

def update_terminal(text, ui):
    if ui and hasattr(ui, 'update_terminal'):
        ui.update_terminal(text)
