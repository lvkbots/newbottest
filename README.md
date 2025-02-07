# Bot Telegram Simple

Un bot Telegram simple et facile à déployer sur Render.

## Configuration requise

- Python 3.9+
- Un token de bot Telegram
- Un compte Render

## Installation locale

1. Cloner le repository
```bash
git clone https://github.com/votre-username/telegram-bot.git
cd telegram-bot
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix
venv\Scripts\activate     # Sur Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement
- Copier `.env.example` vers `.env`
- Ajouter votre token Telegram dans le fichier `.env`

5. Lancer le bot
```bash
python main.py
```

## Déploiement sur Render

1. Créer un nouveau Web Service sur Render
2. Connecter votre repository GitHub
3. Ajouter la variable d'environnement TELEGRAM_BOT_TOKEN
4. Déployer!

## Fonctionnalités

- Commande /start pour démarrer le bot
- Commande /help pour obtenir de l'aide
- Commande /info pour les informations du bot
- Echo des messages reçus
- Gestion des erreurs
