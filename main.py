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
TEXT_PRINCIPAL_1 = "🎲 Programme de gains au casino 💰\n\n1800 personnes ont déjà gagné avec notre méthode unique.\n\nGagnez de l'argent sans effort !"
VIDEO_URL = "https://youtube.com/shorts/wCvzIiQTT_4?si=MYYP5TR-BPr_x0VW"
TEXT_PRINCIPAL_2 = "🏆 Témoignages de nos gagnants !"
FOOTER_IMAGE = "https://aviator.com.in/wp-content/uploads/2024/04/Aviator-Predictor-in-India.webp"

CASINO_PROOFS = [
    {"url": "https://example.com/proof1.jpg", "caption": "💸 Preuve #1 - Alice: 500€"},
    {"url": "https://example.com/proof2.jpg", "caption": "💸 Preuve #2 - Bob: 750€"}
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
    keyboard = [
        [InlineKeyboardButton("💡 Comment ça marche", callback_data='how_works')],
        [InlineKeyboardButton("💰 Preuves de gains", callback_data='payment_proof')],
        [InlineKeyboardButton("📞 Contactez-nous", url="https://t.me/support_casino_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=WELCOME_IMAGE, 
        caption=TEXT_PRINCIPAL_1,
        reply_markup=reply_markup
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("💡 Comment ça marche", callback_data='how_works')],
        [InlineKeyboardButton("💰 Preuves de gains", callback_data='payment_proof')],
        [InlineKeyboardButton("📞 Contactez-nous", url="https://t.me/support_casino_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data == 'how_works':
        await query.edit_message_caption(
            caption=(
                "🔍 Comment notre système fonctionne :\n\n"
                "• Algorithme exclusif de prédiction\n"
                "• Analyse en temps réel\n"
                "• Garantie de gains"
            ),
            reply_markup=reply_markup
        )

    elif query.data == 'payment_proof':
        await query.edit_message_caption(
            caption="💸 Preuves de gains vérifiables !",
            reply_markup=reply_markup
        )
        for proof in CASINO_PROOFS:
            await query.message.reply_photo(
                photo=proof["url"], 
                caption=proof["caption"]
            )

def keep_alive():
    def run():
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
    thread = threading.Thread(target=run)
    thread.start()

def auto_ping():
    while True:
        try:
            requests.get("https://newbottest-p886.onrender.com")
            logging.info("Ping envoyé pour garder l'application active")
        except Exception as e:
            logging.error(f"Erreur lors du ping: {e}")
        time.sleep(300)

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logging.error("Token Telegram manquant!")
        return

    try:
        application = Application.builder().token(token).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_button))

        keep_alive()

        ping_thread = threading.Thread(target=auto_ping)
        ping_thread.daemon = True
        ping_thread.start()

        WEBHOOK_URL = "https://newbottest-p886.onrender.com"
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get('PORT', 10000)),
            url_path=token,
            webhook_url=f"{WEBHOOK_URL}/{token}"
        )

    except Exception as e:
        logging.error(f"Erreur de démarrage du bot: {e}")

if __name__ == '__main__':
    main()
