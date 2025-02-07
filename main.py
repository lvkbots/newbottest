import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv

# Configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
load_dotenv()

# Configuration des messages et images
WELCOME_IMAGE = "https://i.pinimg.com/originals/e3/bd/c0/e3bdc0eb3a3addb16affb830442286d2.png"  # À remplacer par votre URL
INFO_IMAGES = [
    "https://w7.pngwing.com/pngs/218/24/png-transparent-white-and-green-number-1-number-number-1-blue-image-file-formats-text-thumbnail.png",  # À remplacer par vos URLs
    "https://cdn-icons-png.flaticon.com/512/8068/8068073.png",
    "URL_IMAGE_3"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Message d'accueil avec image
    await update.message.reply_photo(
        photo=WELCOME_IMAGE,
        caption="🌟 BIENVENUE ! 🌟\n\nJe suis votre assistant d'information.\nChoisissez une option ci-dessous:"
    )
    
    # Création du clavier personnalisé
    keyboard = [
        [KeyboardButton("🔴 Informations sur les bots")],
        [KeyboardButton("🔵 Centre d'information")],
        [KeyboardButton("✍️ Écrivez-moi à")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Sélectionnez une option:",
        reply_markup=reply_markup
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if "Informations sur les bots" in msg:
        await update.message.reply_text(
            "ℹ️ Informations importantes sur les bots:\n\n"
            "• Les bots sont des assistants automatisés\n"
            "• Ils peuvent vous aider pour diverses tâches\n"
            "• Restez vigilant face aux demandes suspectes"
        )

    elif "Centre d'information" in msg:
        # Envoi des images d'information
        for image_url in INFO_IMAGES:
            await update.message.reply_photo(
                photo=image_url,
                caption="Information importante à connaître 📚"
            )
        
        await update.message.reply_text(
            "Voici quelques informations importantes à retenir:\n\n"
            "1. Vérifiez toujours les sources\n"
            "2. Ne partagez jamais d'informations sensibles\n"
            "3. En cas de doute, demandez conseil"
        )

    elif "Écrivez-moi à" in msg:
        # Création d'un bouton inline pour le contact
        keyboard = [[InlineKeyboardButton("📧 Contacter le support", url="https://t.me/votre_username")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Pour me contacter directement:\n"
            "Cliquez sur le bouton ci-dessous 👇",
            reply_markup=reply_markup
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Gestion des messages texte généraux
    if not update.message.text.startswith('/'):
        await update.message.reply_text(
            "Pour accéder aux options, utilisez le menu ou tapez /start"
        )

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logging.error("Token Telegram manquant!")
        return

    application = Application.builder().token(token).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))

    # Lancement du bot
    print("Bot démarré...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
