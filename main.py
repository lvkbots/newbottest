import logging
import os
from typing import Final
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError
from flask import Flask
import threading
from datetime import datetime

# Configure logging with more detailed format
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)

# Constants
TOKEN: Final = '7184666905:AAFd2arfmIFZ86cp9NNVp57dKkH6hAVi4iM'
SUPPORT_USERNAME: Final = 'support_casino_bot'
WEBSITE_URL: Final = 'https://example.com'

class Button:
    """Button text and callback data constants"""
    INFO_BOTS = "🔴 Informations sur les bots"
    CASINO_WITHDRAWAL = "🔵 Retrait du casino"
    HOW_IT_WORKS = "🔹 Comment ça fonctionne"
    DIRECT_CONTACT = "🔸 Contact direct"
    VISIT_WEBSITE = "🌐 Visitez notre site"
    CONTACT_SUPPORT = "🌫️ Écrivez-moi à"

class Messages:
    """Message text constants"""
    WELCOME = """
Bienvenue sur notre bot de casino! 🎰

Nous sommes là pour vous aider avec vos retraits et répondre à toutes vos questions.
Utilisez les boutons ci-dessous pour naviguer.
    """
    
    INFO_BOTS = """
ℹ️ Informations sur nos bots:

• Disponibles 24/7
• Traitement rapide des retraits
• Support multilingue
• Sécurité maximale
    """
    
    CASINO_WITHDRAWAL = """
💰 Retrait du casino:

1. Minimum de retrait: 50€
2. Délai de traitement: 24-48h
3. Vérification d'identité requise
4. Méthodes disponibles:
   - Virement bancaire
   - Crypto-monnaies
   - Cartes bancaires
    """
    
    HOW_IT_WORKS = """
🎮 Fonctionnement du système:

1. Choisissez votre méthode de retrait
2. Entrez le montant souhaité
3. Fournissez les informations nécessaires
4. Attendez la confirmation

Notre équipe traitera votre demande dans les plus brefs délais.
    """
    
    DIRECT_CONTACT = f"""
📞 Contact direct:

Pour toute assistance immédiate:
• Telegram: @{SUPPORT_USERNAME}
• Disponible: 24/7
• Temps de réponse moyen: 5-10 minutes
    """

@app.route('/')
def home():
    """Flask route to keep the bot alive"""
    return f"Bot actif! Dernière vérification: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def create_keyboard() -> InlineKeyboardMarkup:
    """Create the main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(Button.INFO_BOTS, callback_data='info_bots')],
        [InlineKeyboardButton(Button.CASINO_WITHDRAWAL, callback_data='casino_withdrawal')],
        [InlineKeyboardButton(Button.HOW_IT_WORKS, callback_data='how_it_works')],
        [InlineKeyboardButton(Button.DIRECT_CONTACT, callback_data='direct_contact')],
        [InlineKeyboardButton(Button.VISIT_WEBSITE, url=WEBSITE_URL)],
        [InlineKeyboardButton(Button.CONTACT_SUPPORT, url=f"https://t.me/{SUPPORT_USERNAME}")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command"""
    try:
        await update.message.reply_text(
            text=Messages.WELCOME,
            reply_markup=create_keyboard()
        )
        logger.info(f"New user started the bot: {update.effective_user.id}")
    except TelegramError as e:
        logger.error(f"Error sending welcome message: {e}")
        await update.message.reply_text("Une erreur est survenue. Veuillez réessayer.")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    try:
        await query.answer()
        
        # Map callback data to messages
        message_map = {
            'info_bots': Messages.INFO_BOTS,
            'casino_withdrawal': Messages.CASINO_WITHDRAWAL,
            'how_it_works': Messages.HOW_IT_WORKS,
            'direct_contact': Messages.DIRECT_CONTACT
        }
        
        # Get message text based on callback data
        message_text = message_map.get(query.data)
        if message_text:
            # Add a "Retour" (Back) button to return to main menu
            keyboard = [[InlineKeyboardButton("↩️ Retour", callback_data='main_menu')]]
            await query.edit_message_text(
                text=message_text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif query.data == 'main_menu':
            await query.edit_message_text(
                text=Messages.WELCOME,
                reply_markup=create_keyboard()
            )
            
        logger.info(f"Button pressed: {query.data} by user: {update.effective_user.id}")
    except TelegramError as e:
        logger.error(f"Error handling button: {e}")
        await query.edit_message_text("Une erreur est survenue. Veuillez réessayer.")

def keep_alive() -> None:
    """Start Flask server in a separate thread"""
    def run():
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
    server_thread = threading.Thread(target=run, daemon=True)
    server_thread.start()

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the bot"""
    logger.error(f"Update {update} caused error {context.error}")
    try:
        if update.effective_message:
            await update.effective_message.reply_text(
                "Une erreur est survenue. Notre équipe a été notifiée. "
                "Veuillez réessayer plus tard."
            )
    except TelegramError as e:
        logger.error(f"Error sending error message: {e}")

def main() -> None:
    """Main function to start the bot"""
    try:
        # Create application instance
        application = Application.builder().token(TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_button))
        application.add_error_handler(error_handler)
        
        # Start Flask server
        keep_alive()
        
        # Start bot
        logger.info("Bot started successfully")
        application.run_polling()
    except Exception as e:
        logger.critical(f"Fatal error starting bot: {e}")
        raise

if __name__ == '__main__':
    main()
