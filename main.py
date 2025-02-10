import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, request
import threading
import time

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Flask app pour garder le bot actif
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot actif!"

# Configuration des messages et images
WELCOME_IMAGE = "https://i.pinimg.com/originals/e3/bd/c0/e3bdc0eb3a3addb16affb830442286d2.png"
TEXT_PRINCIPAL_1 = "🌪 Programme de gains au casino 💰\n\n1800 personnes ont déjà gagné avec notre méthode unique.\n\nGagnez de l'argent sans effort !"
VIDEO_URL = "https://youtube.com/shorts/wCvzIiQTT_4?si=MYYP5TR-BPr_x0VW"
TEXT_PRINCIPAL_2 = "🏆 Témoignages de nos gagnants !"
FOOTER_IMAGE = "https://aviator.com.in/wp-content/uploads/2024/04/Aviator-Predictor-in-India.webp"

CASINO_PROOFS = [
    {"url": "https://example.com/proof1.jpg", "caption": "💸 Preuve #1 - Alice: 500€"},
    {"url": "https://example.com/proof2.jpg", "caption": "💸 Preuve #2 - Bob: 750€"}
]

# Token du bot
TOKEN = '7184666905:AAFd2arfmIFZ86cp9NNVp57dKkH6hAVi4iM'  # Remplacez ce token par celui que vous avez

# Fonction de démarrage du bot
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

# Fonction pour gérer les boutons
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

# Fonction pour maintenir le bot actif
def keep_alive():
    def run():
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
    thread = threading.Thread(target=run)
    thread.start()

# Fonction pour envoyer un signal de prédiction après 10 secondes
def send_prediction_signal():
    time.sleep(10)
    # Envoyer un signal de prédiction
    application.bot.send_message(
        chat_id=os.getenv('CHAT_ID'),
        text="🎯 Signal de prédiction Aviator: Gagnez maintenant!"
    )

# Fonction principale
def main():
    global application
    try:
        application = Application.builder().token(TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_button))

        keep_alive()

        # Thread pour envoyer un signal de prédiction après 10 secondes
        prediction_thread = threading.Thread(target=send_prediction_signal)
        prediction_thread.daemon = True
        prediction_thread.start()

        # Lancer le bot
        application.run_polling()

    except Exception as e:
        logging.error(f"Erreur de démarrage du bot: {e}")

if __name__ == '__main__':
    main()
