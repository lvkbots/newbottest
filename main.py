import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
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
        caption=(
            "BILL GATES, BONJOUR ❗\n\n"
            "Je suis un programmeur vénézuélien et je connais la combine pour retirer l'argent du jeu des casinos.\n\n"
            "1800 personnes ont déjà gagné avec moi. Et je peux vous garantir en toute confiance que vous gagnerez.\n\n"
            "Vous pouvez gagner de l'argent sans rien faire, car j'ai déjà fait tout le programme pour vous."
        )
    )
    
    # Création des boutons flottants
    keyboard = [
        [InlineKeyboardButton("🔴 Informations sur les bots", callback_data='info_bots')],
        [InlineKeyboardButton("🔵 Retrait du casino", callback_data='casino_withdraw')],
        [InlineKeyboardButton("✍️ Écrivez-moi à", url="https://t.me/votre_username")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Choisissez une option ci-dessous:",
        reply_markup=reply_markup
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'info_bots':
        await query.edit_message_text(
            "ℹ️ Informations importantes sur les bots:\n\n"
            "• Les bots sont des assistants automatisés\n"
            "• Ils peuvent vous aider pour diverses tâches\n"
            "• Restez vigilant face aux demandes suspectes"
        )

    elif query.data == 'casino_withdraw':
        await query.edit_message_text(
            "🚫 Retrait du casino:\n\n"
            "Voici comment retirer vos gains en toute sécurité. Assurez-vous de suivre les instructions à la lettre pour éviter tout problème."
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Gestion des messages texte généraux
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
    application.add_handler(CallbackQueryHandler(handle_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Lancement du bot
    print("Bot démarré...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
