import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, request
import requests

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Configuration
TOKEN = os.getenv('TELEGRAM_TOKEN', '7184666905:AAFd2arfmIFZ86cp9NNVp57dKkH6hAVi4iM')
PORT = int(os.getenv('PORT', 10000))
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-app.onrender.com')

# Flask app
app = Flask(__name__)
bot_app = None  # Pour stocker l'instance de l'application du bot

# Médias
INTRO_VIDEO = os.getenv('INTRO_VIDEO', "URL_DE_VOTRE_VIDEO")
MAIN_IMAGE = os.getenv('MAIN_IMAGE', "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png")
BOTTOM_IMAGE = os.getenv('BOTTOM_IMAGE', "URL_DE_VOTRE_IMAGE_BAS")

# Images pour les preuves de paiement
PAYMENT_PROOF_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png"
] * 5  # Répété 5 fois

# Images pour les informations
INFO_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png"
] * 5  # Répété 5 fois

def create_keyboard():
    """Crée le clavier avec les boutons"""
    keyboard = [
        [InlineKeyboardButton("🎯 Informations sur les bots", callback_data='info_bots')],
        [InlineKeyboardButton("💰 Retrait du casino", callback_data='casino_withdrawal')],
        [InlineKeyboardButton("📱 Contacter l'expert", url="https://t.me/judespronos")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_program_button():
    """Crée le bouton pour obtenir le programme"""
    keyboard = [[InlineKeyboardButton("🚀 OBTENIR LE PROGRAMME MAINTENANT", url="https://t.me/judespronos")]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /start"""
    try:
        # Envoie la vidéo d'introduction
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=INTRO_VIDEO,
            caption="🎮 Découvrez notre méthode révolutionnaire ! 🎰"
        )

        # Message principal avec image
        message = f"""🎯 BILL GATES, BONJOUR ❗

Je suis un programmeur vénézuélien et je connais la combine pour retirer l'argent du jeu des casinos.

✅ 1800 personnes ont déjà gagné avec moi. Et je peux vous garantir en toute confiance que vous gagnerez.

💫 Vous pouvez gagner de l'argent sans rien faire, car j'ai déjà fait tout le programme pour vous.

🔥 Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y')}"""
    
        reply_markup = create_keyboard()
        await update.message.reply_photo(
            photo=MAIN_IMAGE,
            caption=message,
            reply_markup=reply_markup
        )

        # Envoie l'image du bas
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=BOTTOM_IMAGE,
            caption="🏆 Rejoignez les gagnants dès aujourd'hui !"
        )

        logger.info(f"Nouvel utilisateur: {update.effective_user.id}")

    except Exception as e:
        logger.error(f"Erreur lors du démarrage: {e}")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les clics sur les boutons"""
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'casino_withdrawal':
            # Message initial
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="""🎰 PREUVES DE PAIEMENT RÉCENTES 🎰

💎 Ces retraits ont été effectués dans les dernières 24 heures
✨ Nos utilisateurs gagnent en moyenne 500€ par jour
⚡️ Méthode 100% automatisée et garantie
🔒 Aucun risque de perte

👇 Voici les preuves en images 👇"""
            )
            
            # Envoi des images
            media_group = [InputMediaPhoto(media=url) for url in PAYMENT_PROOF_IMAGES]
            await context.bot.send_media_group(
                chat_id=update.effective_chat.id,
                media=media_group
            )
            
            # Bouton final
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🌟 Prêt à commencer votre succès ?",
                reply_markup=create_program_button()
            )
    
        elif query.data == 'info_bots':
            # Message initial
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="""🤖 NOTRE TECHNOLOGIE UNIQUE 🤖

✅ Intelligence artificielle avancée
🎯 Taux de réussite de 98.7%
💫 Mise à jour quotidienne des algorithmes
⚡️ Plus de 1800 utilisateurs satisfaits

👇 Découvrez notre système en images 👇"""
            )
            
            # Envoi des images
            media_group = [InputMediaPhoto(media=url) for url in INFO_IMAGES]
            await context.bot.send_media_group(
                chat_id=update.effective_chat.id,
                media=media_group
            )
            
            # Bouton final
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🚀 Prêt à révolutionner vos gains ?",
                reply_markup=create_program_button()
            )

        logger.info(f"Bouton {query.data} cliqué par l'utilisateur {update.effective_user.id}")

    except Exception as e:
        logger.error(f"Erreur lors du traitement du bouton: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Une erreur est survenue. Veuillez réessayer."
        )

@app.route('/')
def home():
    """Page d'accueil simple"""
    return f"Bot actif et opérationnel depuis {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook():
    """Gestion des webhooks de Telegram"""
    if request.method == "POST":
        await bot_app.update_queue.put(Update.de_json(request.get_json(), bot_app.bot))
        return "ok"
    return "only POST requests are accepted"

async def setup_webhook():
    """Configure le webhook"""
    webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
    await bot_app.bot.set_webhook(url=webhook_url)
    logger.info(f"Webhook configuré sur {webhook_url}")

async def main():
    """Fonction principale"""
    global bot_app
    
    try:
        # Création de l'application
        bot_app = Application.builder().token(TOKEN).build()

        # Ajout des gestionnaires
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.add_handler(CallbackQueryHandler(handle_button))

        # Configuration du webhook
        await setup_webhook()

        # Démarrage de l'application Flask
        logger.info("Bot démarré avec succès!")
        return bot_app
    
    except Exception as e:
        logger.critical(f"Erreur fatale: {e}")
        raise

if __name__ == '__main__':
    # Créer le fichier .env avec les variables nécessaires
    from pathlib import Path
    env_path = Path('.env')
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write(f"""TELEGRAM_TOKEN={TOKEN}
WEBHOOK_URL={WEBHOOK_URL}
PORT={PORT}
""")
    
    # Démarrer l'application
    from asyncio import get_event_loop
    loop = get_event_loop()
    loop.run_until_complete(main())
    
    # Démarrer Flask avec gunicorn
    app.run(host='0.0.0.0', port=PORT)
