import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
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

# Configuration des messages et media
WELCOME_IMAGE = "https://i.pinimg.com/originals/e3/bd/c0/e3bdc0eb3a3addb16affb830442286d2.png"
VIDEO_URL = "https://example.com/video.mp4"  # Remplacez par votre lien de vidéo
BOTTOM_IMAGE = "https://i.pinimg.com/originals/e3/bd/c0/e3bdc0eb3a3addb16affb830442286d2.png"  # Remplacez par votre image en bas des boutons

TEXT_PRINCIPAL_1 = (
    "BILL GATES, BONJOUR 🛑\n\n"
    "Je suis un programmeur vénézuélien et je connais la combine pour retirer l'argent du jeu des casinos.\n\n"
    "1800 personnes ont déjà gagné avec moi. Et je peux vous garantir en toute confiance que vous gagnerez.\n\n"
    "Vous pouvez gagner de l'argent sans rien faire, car j'ai déjà fait tout le programme pour vous."
)

TEXT_PRINCIPAL_2 = (
    "🔍 Comment ça marche ?\n\n"
    "1. Algorithme exclusif de prédiction\n"
    "2. Analyse en temps réel\n"
    "3. Garantie de gains"
)

CASINO_PROOFS = [
    {"url": "https://i.pinimg.com/originals/e3/bd/c0/e3bdc0eb3a3addb16affb830442286d2.png"},
    {"url": "https://i.pinimg.com/originals/e3/bd/c0/e3bdc0eb3a3addb16affb830442286d2.png", "caption": "💸 Preuve #2 - Bob: 750€"}
]

# Token du bot
TOKEN = '7184666905:AAFd2arfmIFZ86cp9NNVp57dKkH6hAVi4iM'  # Remplacez par votre token

# Fonction de démarrage du bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔴 Informations sur les bots", callback_data='how_works')],
        [InlineKeyboardButton("🔵 Retrait du casino", callback_data='casino_withdrawal')],
        [InlineKeyboardButton("✍️ Écrivez-moi à", url="https://t.me/support_casino_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envoi des différents médias et textes
    await update.message.reply_photo(photo=WELCOME_IMAGE)
    await update.message.reply_text(TEXT_PRINCIPAL_1)
    await update.message.reply_video(video=VIDEO_URL)
    await update.message.reply_text(TEXT_PRINCIPAL_2, reply_markup=reply_markup)
    await update.message.reply_photo(photo=BOTTOM_IMAGE)

# Fonction pour gérer les boutons
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'how_works':
        await query.message.reply_text(TEXT_PRINCIPAL_2)
    elif query.data == 'casino_withdrawal':
        for proof in CASINO_PROOFS:
            await query.message.reply_photo(photo=proof["url"], caption=proof["caption"])

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
