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

# Configuration des messages et médias
IMAGE_PRINCIPALE_1 = "https://i.pinimg.com/originals/e3/bd/c0/e3bdc0eb3a3addb16affb830442286d2.png"
TEXTE_PRINCIPAL_1 = "🌪 Programme de gains au casino 💰\n\n1800 personnes ont déjà gagné avec notre méthode unique.\n\nGagnez de l'argent sans effort !"
VIDEO_URL = "https://youtube.com/shorts/wCvzIiQTT_4?si=MYYP5TR-BPr_x0VW"
TEXTE_PRINCIPAL_2 = "🏆 Témoignages de nos gagnants !"
FOOTER_IMAGE = "https://aviator.com.in/wp-content/uploads/2024/04/Aviator-Predictor-in-India.webp"

CASINO_PROOFS = [
    {"url": "https://example.com/proof1.jpg", "caption": "💸 Preuve #1 - Alice: 500€"},
    {"url": "https://example.com/proof2.jpg", "caption": "💸 Preuve #2 - Bob: 750€"}
]

# Token du bot
TOKEN = '7184666905:AAFd2arfmIFZ86cp9NNVp57dKkH6hAVi4iM'  # Remplacez ce token par celui que vous avez

# Fonction de démarrage du bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Envoyer l'image principale 1
    await update.message.reply_photo(photo=IMAGE_PRINCIPALE_1)

    # Envoyer le texte principal 1
    await update.message.reply_text(TEXTE_PRINCIPAL_1)

    # Envoyer la vidéo
    await update.message.reply_video(video=VIDEO_URL)

    # Envoyer le texte principal 2
    await update.message.reply_text(TEXTE_PRINCIPAL_2)

    # Afficher les boutons
    keyboard = [
        [InlineKeyboardButton("💡 Comment ça marche", callback_data='how_works')],
        [InlineKeyboardButton("💰 Preuve de paiement", callback_data='payment_proof')],
        [InlineKeyboardButton("📞 Contactez-nous", url="https://t.me/support_casino_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choisissez une option :", reply_markup=reply_markup)

    # Envoyer l'image en bas des boutons
    await update.message.reply_photo(photo=FOOTER_IMAGE)

# Fonction pour gérer les boutons
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'how_works':
        await query.edit_message_text(
            text=(
                "🔍 Comment notre système fonctionne :\n\n"
                "• Algorithme exclusif de prédiction\n"
                "• Analyse en temps réel\n"
                "• Garantie de gains"
            )
        )
    elif query.data == 'payment_proof':
        await query.message.reply_text("💸 Voici les preuves de paiement vérifiables :")
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

# Fonction principale
def main():
    global application
    try:
        application = Application.builder().token(TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_button))

        keep_alive()

        # Lancer le bot
        application.run_polling()

    except Exception as e:
        logging.error(f"Erreur de démarrage du bot: {e}")

if __name__ == '__main__':
    main()
