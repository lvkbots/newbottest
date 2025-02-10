import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, request
import threading

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
BOTTOM_IMAGE = "https://example.com/bottom_image.jpg"
VIDEO_URL = "https://example.com/video.mp4"
TEXT_PRINCIPAL_1 = (
    "BILL GATES, BONJOUR !\n\n"
    "Je suis un programmeur vénézuélien et je connais la combine pour retirer l'argent du jeu des casinos."
)

TEXT_PRINCIPAL_2 = (
    "1800 personnes ont déjà gagné avec moi. Et je peux vous garantir en toute confiance que vous gagnerez.\n\n"
    "Vous pouvez gagner de l'argent sans rien faire, car j'ai déjà fait tout le programme pour vous."
)

CASINO_PROOFS = [
    {"url": "https://example.com/proof1.jpg", "caption": "💸 Preuve #1 - Alice: 500€"},
    {"url": "https://example.com/proof2.jpg", "caption": "💸 Preuve #2 - Bob: 750€"},
    {"url": "https://example.com/proof3.jpg", "caption": "💸 Preuve #3 - Charlie: 1000€"},
    {"url": "https://example.com/proof4.jpg", "caption": "💸 Preuve #4 - David: 1200€"},
    {"url": "https://example.com/proof5.jpg", "caption": "💸 Preuve #5 - Eva: 1500€"}
]

# Token du bot
TOKEN = '7184666905:AAFd2arfmIFZ86cp9NNVp57dKkH6hAVi4iM'

# Fonction de démarrage du bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔴 Informations sur les bots", callback_data='info_bots')],
        [InlineKeyboardButton("🔵 Retrait du casino", callback_data='casino_withdrawal')],
        [InlineKeyboardButton("🔹 Comment ça fonctionne", callback_data='how_it_works')],
        [InlineKeyboardButton("🔸 Contact direct", callback_data='direct_contact')],
        [InlineKeyboardButton("🌐 Visitez notre site", url="https://example.com")],
        [InlineKeyboardButton("🌫️ Écrivez-moi à", url="https://t.me/support_casino_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(photo=WELCOME_IMAGE)
    await update.message.reply_text(TEXT_PRINCIPAL_1)
    await update.message.reply_video(video=VIDEO_URL)
    await update.message.reply_text(TEXT_PRINCIPAL_2, reply_markup=reply_markup)
    await update.message.reply_photo(photo=BOTTOM_IMAGE)

# Fonction pour gérer les boutons
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'info_bots':
        for proof in CASINO_PROOFS:
            await query.message.reply_photo(photo=proof["url"], caption=proof["caption"])
    elif query.data == 'casino_withdrawal':
        keyboard = [
            [InlineKeyboardButton("🔹 Comment ça fonctionne", callback_data='how_it_works')],
            [InlineKeyboardButton("🔸 Contact direct", callback_data='direct_contact')],
            [InlineKeyboardButton("🔴 Informations sur les bots", callback_data='info_bots')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="💸 Preuves de gains vérifiables !", reply_markup=reply_markup)
        for proof in CASINO_PROOFS:
            await query.message.reply_photo(photo=proof["url"], caption=proof["caption"])
    elif query.data == 'how_it_works':
        await query.edit_message_text(
            text=(
                "🔍 Voici comment ça fonctionne :\n\n"
                "1. Inscrivez-vous\n"
                "2. Utilisez notre programme\n"
                "3. Retirez vos gains"
            )
        )
    elif query.data == 'direct_contact':
        await query.edit_message_text(text="📢 Contactez-nous directement via Telegram pour toute question !")

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
