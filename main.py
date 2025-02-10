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
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",  # Image 1
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",  # Image 2
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",  # Image 3
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",  # Image 4
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png"   # Image 5
]

# Images pour les informations
INFO_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",  # Info Image 1
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",  # Info Image 2
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",  # Info Image 3
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png",  # Info Image 4
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Circle_sign_2.svg/1024px-Circle_sign_2.svg.png"   # Info Image 5
]

def create_keyboard():
    """Crée le clavier avec les boutons"""
    keyboard = [
        [InlineKeyboardButton("🔴 Informations sur les bots", callback_data='info_bots')],
        [InlineKeyboardButton("🔵 Retrait du casino", callback_data='casino_withdrawal')],
        [InlineKeyboardButton("✍️ Écrivez-moi à", callback_data='write_to_me')]
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
        # Envoie les 5 images de preuve de paiement
        media_group = [InputMediaPhoto(media=url) for url in PAYMENT_PROOF_IMAGES]
        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=media_group
        )
        await query.edit_message_caption(
            caption="Voici les preuves de paiement récentes ! 💰\nContactez-nous pour plus d'informations.",
            reply_markup=create_keyboard()
        )
    
    elif query.data == 'info_bots':
        # Envoie les 5 images d'information
        media_group = [InputMediaPhoto(media=url) for url in INFO_IMAGES]
        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=media_group
        )
        await query.edit_message_caption(
            caption="Voici les informations sur nos bots ! 🤖\nContactez-nous pour en savoir plus.",
            reply_markup=create_keyboard()
        )
    
    elif query.data == 'write_to_me':
        await query.edit_message_caption(
            caption="Contactez-moi directement pour commencer...",
            reply_markup=create_keyboard()
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
