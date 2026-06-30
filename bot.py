from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os

TOKEN = os.getenv("BOT_TOKEN")
keyboard = [
    ["📋 Latest Jobs", "🎓 Freshers Jobs"],
    ["🏠 Work From Home", "💻 IT Jobs"],
    ["⭐ Premium", "ℹ️ Help"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇮🇳 Welcome to India Jobs Alert Bot!\n\n"
        "Choose an option below:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 Latest Jobs":
        await update.message.reply_text(
            "🔥 Latest Private Jobs in India\n\n"
            "1️⃣ Customer Support Executive - Hyderabad\n"
            "2️⃣ Data Entry Operator - Remote\n"
            "3️⃣ Admin Executive - Bangalore"
        )

    elif text == "🎓 Freshers Jobs":
        await update.message.reply_text(
            "🎓 Freshers Jobs\n\n"
            "1️⃣ Process Associate - Hyderabad\n"
            "2️⃣ Customer Support - Bangalore\n"
            "3️⃣ Data Entry Operator - Remote"
        )

    elif text == "🏠 Work From Home":
        await update.message.reply_text(
            "🏠 Work From Home Jobs\n\n"
            "1️⃣ Data Entry Operator\n"
            "2️⃣ Customer Support Executive\n"
            "3️⃣ Online Sales Representative"
        )

    elif text == "💻 IT Jobs":
        await update.message.reply_text(
            "💻 IT Jobs\n\n"
            "1️⃣ Python Developer - Bangalore\n"
            "2️⃣ Software Tester - Hyderabad\n"
            "3️⃣ Technical Support Engineer - Pune"
        )

    elif text == "⭐ Premium":
        await update.message.reply_text(
            "⭐ Premium Plans\n\n"
            "₹99/month - Instant alerts\n"
            "₹199/month - Resume review\n"
            "₹299/month - Priority support"
        )

    elif text == "ℹ️ Help":
        await update.message.reply_text(
            "Tap any button below to browse jobs."
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

app.run_polling()
