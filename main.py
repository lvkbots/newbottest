import logging
import os
import time
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
import threading
from datetime import datetime

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

# Flask app pour garder le bot actif
app = Flask(__name__)

@app.route('/')
def home():
    return f"Bot actif et opérationnel depuis {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Token du bot
TOKEN = '7184666905:AAFd2arfmIFZ86cp9NNVp57dKkH6hAVi4iM'

# Médias
INTRO_VIDEO = "URL_DE_VOTRE_VIDEO"  # À remplacer par l'URL de votre vidéo
MAIN_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png"
BOTTOM_IMAGE = "URL_DE_VOTRE_IMAGE_BAS"  # À remplacer par l'URL de l'image du bas

# Images pour les preuves de paiement
PAYMENT_PROOF_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png"
]

# Images pour les informations
INFO_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png"
]

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
        message = """🎯 BILL GATES, BONJOUR ❗

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

def ping_server():
    """Fonction pour faire un ping régulier du serveur"""
    while True:
        try:
            # Faire une requête à votre propre URL
            response = requests.get(f"https://{os.environ.get('RENDER_EXTERNAL_URL', 'your-app.onrender.com')}")
            logger.info(f"Ping serveur effectué - Status: {response.status_code}")
        except Exception as e:
            logger.error(f"Erreur lors du ping: {e}")
        time.sleep(300)  # Attendre 5 minutes avant le prochain ping

def keep_alive():
    """Maintient le bot actif avec Flask et le système de ping"""
    def run_flask():
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
    
    # Thread pour Flask
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Thread pour le ping automatique
    ping_thread = threading.Thread(target=ping_server)
    ping_thread.daemon = True
    ping_thread.start()

def main():
    """Fonction principale pour démarrer le bot"""
    try:
        # Création de l'application
        application = Application.builder().token(TOKEN).build()

        # Ajout des gestionnaires
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_button))

        # Maintenir le bot actif avec Flask et le système de ping
        keep_alive()

        # Lancer le bot
        logger.info("Bot démarré avec succès!")
        application.run_polling()

    except Exception as e:
        logger.critical(f"Erreur fatale: {e}")
        raise

if __name__ == '__main__':
    main()
