# VzbotVoice - Contrôle Vocal pour Imprimante 3D Vzbot

Ce projet permet de contrôler votre imprimante 3D Vzbot à l'aide de commandes vocales en français. Il utilise la reconnaissance vocale pour interpréter vos commandes et effectuer diverses actions sur votre imprimante.

## 🎯 Fonctionnalités

### Commandes Vocales Disponibles

1. **Salutations**
   - "Salut VZ" / "Bonjour" : L'assistant vous répond et attend vos instructions

2. **Gestion de la Température**
   - "Active la chauffe" : Chauffe la buse à 190°C
   - "Chauffe désactivée" / "Arrête la chauffe" : Désactive la chauffe de la buse
   - "Préchauffe" : Lance la procédure de préchauffage (buse et plateau)

3. **Mouvements et Calibration**
   - "Fais un home" / "Auto home" : Effectue un homing de l'imprimante
   - "Désactive les moteurs" : Désactive tous les moteurs
   - "Fait un mesh" / "Fais un mèche" : Lance un bed mesh (maillage du plateau)
   - "Offset à [valeur]" : Règle l'offset Z (exemple : "offset à -0.2")

4. **Impression**
   - "Lance le fichier [nom]" : Démarre l'impression du fichier spécifié (sans l'extension .gcode)
   - "Temps d'impression restant" : Annonce le temps restant de l'impression en cours

## 🚀 Installation

### Prérequis
- Windows 10 ou 11
- Python 3.11 ou supérieur
- Un microphone fonctionnel
- Une imprimante Vzbot configurée avec Klipper et Mainsail/Fluidd

### Étapes d'Installation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/Eloura74/KlipperVoiceMainsail.git
   cd KlipperVoiceMainsail
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

### ⚙️ Configuration

1. **Configuration de l'imprimante**
   - Créez un fichier `.env` à la racine du projet avec le contenu suivant :
     ```env
     PRINTER_IP=192.168.1.xxx  # Remplacez par l'IP de votre imprimante
     PRINTER_PORT=7125         # Le port par défaut est 7125
     ```

2. **Trouver l'IP de votre imprimante**
   - Ouvrez Mainsail/Fluidd dans votre navigateur
   - L'adresse dans la barre de navigation est votre IP
   - Exemple : si vous accédez à `http://192.168.1.100:7125`
     - IP = 192.168.1.100
     - Port = 7125

3. **Configuration du Microphone**
   - Ouvrez les Paramètres Windows
   - Allez dans Système > Son
   - Sélectionnez votre microphone comme périphérique d'entrée par défaut
   - Testez le microphone pour vérifier qu'il fonctionne

## 🎤 Utilisation

1. **Démarrer le programme**
   ```bash
   python run.py
   ```

2. **Utiliser les commandes vocales**
   - Attendez le message "Écoute en cours... Parlez maintenant"
   - Dites "Salut VZ" ou une autre commande
   - Parlez clairement et distinctement
   - L'assistant confirmera votre commande vocalement

## 🔧 Dépannage

1. **La reconnaissance vocale ne fonctionne pas**
   - Vérifiez que votre microphone est bien sélectionné dans Windows
   - Parlez plus fort et plus clairement
   - Réduisez les bruits ambiants
   - Vérifiez que le microphone n'est pas en sourdine

2. **L'imprimante ne répond pas**
   - Vérifiez que l'imprimante est allumée
   - Vérifiez la connexion réseau de l'imprimante
   - Confirmez que l'IP dans le fichier `.env` est correcte
   - Assurez-vous que Klipper fonctionne (via Mainsail/Fluidd)

3. **Les fichiers ne sont pas trouvés**
   - Vérifiez que le fichier est bien présent dans Mainsail/Fluidd
   - Ne prononcez pas l'extension ".gcode"
   - Prononcez le nom du fichier exactement comme il apparaît

## 🔒 Sécurité

- Ne partagez jamais votre fichier `.env`
- Gardez votre imprimante sur un réseau local sécurisé
- Mettez régulièrement à jour votre système et Klipper

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## ✨ Remerciements

- L'équipe Klipper pour leur excellent firmware
- La communauté Vzbot pour leur support
- Tous les contributeurs du projet
