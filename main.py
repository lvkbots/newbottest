import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Gestionnaire de commandes
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bonjour! Je suis votre assistant bot. Voici mes commandes disponibles:\n"
        "/start - Afficher ce message\n"
        "/help - Obtenir de l'aide\n"
        "/info - Informations sur le bot"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Comment puis-je vous aider?\n"
        "- Envoyez-moi un message et je vous répondrai\n"
        "- Utilisez /info pour plus d'informations"
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Information sur le bot:\n"
        "Version: 1.0.0\n"
        "Créé en 2025\n"
        "Hébergé sur Render"
    )

# Gestionnaire de messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Vous avez dit: {update.message.text}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Une erreur s'est produite: {context.error}")
    if update:
        await update.message.reply_text("Désolé, une erreur s'est produite.")

def main():
    # Récupération du token depuis les variables d'environnement
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logging.error("Token Telegram non trouvé!")
        return

    # Création de l'application
    application = Application.builder().token(token).build()

    # Ajout des gestionnaires de commandes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    
    # Gestionnaire de messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Gestionnaire d'erreurs
    application.add_error_handler(error_handler)

    # Démarrage du bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
