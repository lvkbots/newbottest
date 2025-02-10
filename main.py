import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import threading
import requests
import time

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
load_dotenv()

# Flask app pour garder le bot actif
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot actif!"

# Configuration des messages et images
WELCOME_IMAGE = "https://i.pinimg.com/originals/e3/bd/c0/e3bdc0eb3a3addb16affb830442286d2.png"
TEXT_PRINCIPAL_1 = "BILL GATES, BONJOUR ❗\n\nJe suis un programmeur vénézuélien et je connais la combine pour retirer l'argent du jeu des casinos.\n\n1800 personnes ont déjà gagné avec moi. Et je peux vous garantir en toute confiance que vous gagnerez.\n\nVous pouvez gagner de l'argent sans rien faire, car j'ai déjà fait tout le programme pour vous."
VIDEO_URL = "https://youtube.com/shorts/wCvzIiQTT_4?si=MYYP5TR-BPr_x0VW"
TEXT_PRINCIPAL_2 = "Voici des témoignages vidéo de personnes ayant déjà gagné grâce à notre programme. Vous pouvez être le prochain gagnant !"
FOOTER_IMAGE = "https://aviator.com.in/wp-content/uploads/2024/04/Aviator-Predictor-in-India.webp"

CASINO_PROOFS = [
    {"url": "https://example.com/proof1.jpg", "caption": "💸 Preuve de paiement #1 - Gagnant: Alice, Montant: 500€"},
    {"url": "https://example.com/proof2.jpg", "caption": "💸 Preuve de paiement #2 - Gagnant: Bob, Montant: 750€"},
    {"url": "https://example.com/proof3.jpg", "caption": "💸 Preuve de paiement #3 - Gagnant: Charlie, Montant: 1000€"}
]

# Endpoint pour le webhook
@app.route(f'/{os.getenv("TELEGRAM_BOT_TOKEN")}', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.process_update(update)
        return 'ok'
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_photo(photo=WELCOME_IMAGE)
        await update.message.reply_text(TEXT_PRINCIPAL_1)
        await update.message.reply_video(video=VIDEO_URL)
        await update.message.reply_text(TEXT_PRINCIPAL_2)

        keyboard = [
            [InlineKeyboardButton("🔴 Informations sur les bots", callback_data='info_bots')],
            [InlineKeyboardButton("🔵 Preuve de paiement", callback_data='payment_proof')],
            [InlineKeyboardButton("✍️ Écrivez-moi à", url="https://t.me/votre_username")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Choisissez une option ci-dessous:",
            reply_markup=reply_markup
        )

        await update.message.reply_photo(photo=FOOTER_IMAGE)
    except Exception as e:
        logging.error(f"Error in start command: {e}")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("🔴 Informations sur les bots", callback_data='info_bots')],
            [InlineKeyboardButton("🔵 Preuve de paiement", callback_data='payment_proof')],
            [InlineKeyboardButton("✍️ Écrivez-moi à", url="https://t.me/votre_username")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if query.data == 'info_bots':
            await query.edit_message_text(
                text=(
                    "ℹ️ Informations importantes sur les bots:\n\n"
                    "• Les bots sont des assistants automatisés\n"
                    "• Ils peuvent vous aider pour diverses tâches\n"
                    "• Restez vigilant face aux demandes suspectes"
                ),
                reply_markup=reply_markup
            )

        elif query.data == 'payment_proof':
            await query.edit_message_text(
                text=(
                    "🛑 Preuve de paiement:\n\n"
                    "Voici les preuves de paiements réussis. Assurez-vous de suivre les instructions à la lettre pour éviter tout problème."
                ),
                reply_markup=reply_markup
            )
            for proof in CASINO_PROOFS:
                await query.message.reply_photo(photo=proof["url"], caption=proof["caption"])

            await query.message.reply_photo(photo=FOOTER_IMAGE)
    except Exception as e:
        logging.error(f"Error in handle_button: {e}")

# Fonction pour garder l'application active
def keep_alive():
    def run():
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

    thread = threading.Thread(target=run)
    thread.start()

# Ping du serveur toutes les 5 minutes
def auto_ping():
    while True:
        try:
            # Utiliser l'URL de votre Render ou hébergement
            requests.get("https://your-render-app-url.com")  
            logging.info("Ping envoyé pour garder l'application active")
        except Exception as e:
            logging.error(f"Erreur lors du ping: {e}")
        time.sleep(300)  # Ping toutes les 5 minutes

def main():
    global application
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logging.error("Token Telegram manquant!")
        return

    try:
        application = Application.builder().token(token).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_button))

        keep_alive()

        # Lancer la tâche de ping automatique
        ping_thread = threading.Thread(target=auto_ping)
        ping_thread.daemon = True
        ping_thread.start()

        # URL de webhook à remplacer par votre propre URL
        WEBHOOK_URL = "https://your-render-app-url.com"
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get('PORT', 8080)),
            url_path=token,
            webhook_url=f"{WEBHOOK_URL}/{token}"
        )

    except Exception as e:
        logging.error(f"Erreur de démarrage du bot: {e}")

if __name__ == '__main__':
    main()
