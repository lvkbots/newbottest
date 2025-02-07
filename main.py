import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from flask import Flask
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
INFO_IMAGES = [
    "https://w7.pngwing.com/pngs/218/24/png-transparent-white-and-green-number-1-number-number-1-blue-image-file-formats-text-thumbnail.png",
    "https://cdn-icons-png.flaticon.com/512/8068/8068073.png",
    "https://example.com/image3.png"
]

CASINO_PROOFS = [
    {"url": "https://cdn-icons-png.flaticon.com/512/8068/8068073.png", "caption": "💸 Preuve de retrait #1 - Gagnant: Alice, Montant: 500€"},
    {"url": "https://w7.pngwing.com/pngs/218/24/png-transparent-white-and-green-number-1-number-number-1-blue-image-file-formats-text-thumbnail.png", "caption": "💸 Preuve de retrait #2 - Gagnant: Bob, Montant: 750€"},
    {"url": "https://example.com/proof3.jpg", "caption": "💸 Preuve de retrait #3 - Gagnant: Charlie, Montant: 1000€"}
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption=(
            "BILL GATES, BONJOUR ❗\n\n"
            "Je suis un programmeur vénézuélien et je connais la combine pour retirer l'argent du jeu des casinos.\n\n"
            "1800 personnes ont déjà gagné avec moi. Et je peux vous garantir en toute confiance que vous gagnerez.\n\n"
            "Vous pouvez gagner de l'argent sans rien faire, car j'ai déjà fait tout le programme pour vous."
        )
    )

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

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# Fonction pour garder l'application active
def keep_alive():
    def run():
        app.run(host='0.0.0.0', port=8080)

    thread = threading.Thread(target=run)
    thread.start()

# Ping du serveur toutes les 5 minutes
def auto_ping():
    while True:
        try:
            requests.get("https://votre-app-render-url.com")  # Remplace par l'URL Render de ton app
            logging.info("Ping envoyé pour garder l'application active")
        except Exception as e:
            logging.error(f"Erreur lors du ping: {e}")
        time.sleep(300)  # Ping toutes les 5 minutes


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logging.error("Token Telegram manquant!")
        return

    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button))

    keep_alive()

    # Lancer la tâche de ping automatique
    ping_thread = threading.Thread(target=auto_ping)
    ping_thread.start()

    logging.info("Bot démarré et en cours d'exécution...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
