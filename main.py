import logging
import os
import requests
import threading
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, request
from datetime import datetime
import time

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
    return "Bot actif et opérationnel!"

# Token du bot (défini directement ici)
TOKEN = '7184666905:AAFd2arfmIFZ86cp9NNVp57dKkH6hAVi4iM'

# URL de votre domaine sur Render
RENDER_URL = 'https://newbottest-p886.onrender.com'

# Médias
INTRO_VIDEO = "https://drive.google.com/uc?export=download&id=1NREjyyYDfdgGtx4r-Lna-sKgpCHIC1ia"
MAIN_IMAGE = "https://i.ytimg.com/vi/KolFup7TxOM/hq720.jpg"
BOTTOM_IMAGE = "https://aviator.com.in/wp-content/uploads/2024/04/Aviator-Predictor-in-India.png"

# Fonction pour créer les boutons
def create_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎯 Informations sur les bots", callback_data='info_bots')],
        [InlineKeyboardButton("💰 Retrait du casino", callback_data='casino_withdrawal')],
        [InlineKeyboardButton("📱 Contacter l'expert", url="https://t.me/judespronos")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Fonction de démarrage
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
        message = f"""🎯 BILL GATES, BONJOUR ❗️

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

        # Envoie de l'image du bas
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=BOTTOM_IMAGE,
            caption="🏆 Rejoignez les gagnants dès aujourd'hui !"
        )

        logger.info(f"Nouvel utilisateur: {update.effective_user.id}")

    except Exception as e:
        logger.error(f"Erreur lors du démarrage: {e}")

# Fonction pour gérer les clics sur les boutons
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'casino_withdrawal':
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
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="""🤖 NOTRE TECHNOLOGIE UNIQUE 🤖

✅ Intelligence artificielle avancée
🎯 Taux de réussite de 98.7%
💫 Mise à jour quotidienne des algorithmes
⚡️ Plus de 1800 utilisateurs satisfaits

👇 Découvrez notre système en images 👇"""
            )
            
            media_group = [InputMediaPhoto(media=url) for url in INFO_IMAGES]
            await context.bot.send_media_group(
                chat_id=update.effective_chat.id,
                media=media_group
            )
            
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

# Webhook handler
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    """Recevoir les mises à jour Telegram via un webhook"""
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, application.bot)
    application.process_update(update)
    return 'OK', 200

def keep_alive():
    """Maintient le bot actif avec Flask et envoie des pings toutes les 2 secondes"""
    def ping_render():
        while True:
            try:
                response = requests.get(RENDER_URL)  # Envoi d'un ping à votre URL Render
                if response.status_code == 200:
                    logger.info("Ping réussi. Le bot est actif.")
                else:
                    logger.warning(f"Échec du ping: {response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Erreur lors de l'envoi du ping: {e}")

            time.sleep(2)  # Attendre 2 secondes avant de pinguer à nouveau
    
    thread = threading.Thread(target=ping_render)
    thread.daemon = True
    thread.start()

def main():
    """Fonction principale pour démarrer le bot"""
    try:
        global application
        application = Application.builder().token(TOKEN).build()

        # Ajout des gestionnaires
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_button))

        # Configurer le webhook
        application.bot.set_webhook(f"{RENDER_URL}/{TOKEN}")

        # Démarrer l'application Flask
        keep_alive()

        logger.info("Bot démarré avec succès!")
        application.run_polling()  # Utilisation du polling si vous ne souhaitez pas webhooks

    except Exception as e:
        logger.critical(f"Erreur fatale: {e}")
        raise

if __name__ == '__main__':
    main()
