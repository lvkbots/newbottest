import logging
import os
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

    await update.message.reply_text("Bienvenue sur notre bot !", reply_markup=reply_markup)

# Fonction pour gérer les boutons
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'info_bots':
        await query.edit_message_text(text="Ici vous trouverez des informations sur les bots.")
    elif query.data == 'casino_withdrawal':
        await query.edit_message_text(text="Voici les détails sur le retrait du casino.")
    elif query.data == 'how_it_works':
        await query.edit_message_text(text="Voici comment ça fonctionne.")
    elif query.data == 'direct_contact':
        await query.edit_message_text(text="Contactez-nous directement via Telegram.")

# Fonction pour maintenir le bot actif
def keep_alive():
    def run():
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
    thread = threading.Thread(target=run)
    thread.start()

# Fonction principale
def main():
    try:
        application = Application.builder().token(TOKEN).build()

        # Ajout des gestionnaires pour les commandes et les boutons
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
