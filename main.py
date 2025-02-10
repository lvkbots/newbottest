import logging
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
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

# Token du bot
TOKEN = '7184666905:AAFd2arfmIFZ86cp9NNVp57dKkH6hAVi4iM'

# URLs des images
MAIN_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png"

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
        [InlineKeyboardButton("🔴 Informations sur les bots", callback_data='info_bots')],
        [InlineKeyboardButton("🔵 Retrait du casino", callback_data='casino_withdrawal')],
        [InlineKeyboardButton("✍️ Écrivez-moi à", url="https://t.me/judespronos")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /start"""
    message = """BILL GATES, BONJOUR ❗

Je suis un programmeur vénézuélien et je connais la combine pour retirer l'argent du jeu des casinos.

1800 personnes ont déjà gagné avec moi. Et je peux vous garantir en toute confiance que vous gagnerez.

Vous pouvez gagner de l'argent sans rien faire, car j'ai déjà fait tout le programme pour vous."""
    
    reply_markup = create_keyboard()
    await update.message.reply_photo(
        photo=MAIN_IMAGE,
        caption=message,
        reply_markup=reply_markup
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les clics sur les boutons"""
    query = update.callback_query
    await query.answer()

    if query.data == 'casino_withdrawal':
        # Envoie d'abord le message explicatif
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🎰 Voici les derniers retraits effectués par nos utilisateurs ! Des gains garantis avec notre méthode unique. N'attendez plus pour nous rejoindre et commencer à gagner. 💰"
        )
        # Puis envoie les images
        media_group = [InputMediaPhoto(media=url) for url in PAYMENT_PROOF_IMAGES]
        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=media_group
        )
    
    elif query.data == 'info_bots':
        # Envoie d'abord le message explicatif
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🤖 Découvrez notre technologie unique qui permet de gagner à coup sûr. Notre bot utilise un algorithme sophistiqué pour garantir des gains constants. Plus de 1800 utilisateurs satisfaits ! 🚀"
        )
        # Puis envoie les images
        media_group = [InputMediaPhoto(media=url) for url in INFO_IMAGES]
        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=media_group
        )

def keep_alive():
    """Maintient le bot actif avec Flask"""
    def run():
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
    thread = threading.Thread(target=run)
    thread.start()

def main():
    """Fonction principale pour démarrer le bot"""
    try:
        # Création de l'application
        application = Application.builder().token(TOKEN).build()

        # Ajout des gestionnaires
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_button))

        # Maintenir le bot actif avec Flask
        keep_alive()

        # Lancer le bot
        application.run_polling()

    except Exception as e:
        logging.error(f"Erreur de démarrage du bot: {e}")

if __name__ == '__main__':
    main()
