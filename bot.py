from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8871832997:AAGnZs_4GEAO2FrUIh0WH04IzHnTYRtOv6I"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇮🇳 Welcome to IndiaJobsAlertBot!\n\n"
        "Available Commands:\n"
        "/jobs - Latest jobs\n"
        "/freshers - Freshers jobs\n"
        "/wfh - Work From Home jobs\n"
        "/itjobs - IT jobs\n"
        "/help - Help menu"
    )

async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Latest Private Jobs in India\n\n"
        "1️⃣ Customer Support Executive - Hyderabad\n"
        "2️⃣ Data Entry Operator - Remote\n"
        "3️⃣ Admin Executive - Bangalore\n"
        "4️⃣ Sales Executive - Pune\n"
        "5️⃣ HR Executive - Chennai"
    )

async def freshers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 Freshers Jobs\n\n"
        "1️⃣ Process Associate - Hyderabad\n"
        "2️⃣ Customer Support - Bangalore\n"
        "3️⃣ Data Entry Operator - Remote"
    )

async def wfh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏠 Work From Home Jobs\n\n"
        "1️⃣ Data Entry Operator\n"
        "2️⃣ Customer Support Executive\n"
        "3️⃣ Online Sales Representative"
    )

async def itjobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💻 IT Jobs\n\n"
        "1️⃣ Python Developer - Bangalore\n"
        "2️⃣ Software Tester - Hyderabad\n"
        "3️⃣ Technical Support Engineer - Pune"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Use these commands:\n\n"
        "/jobs\n"
        "/freshers\n"
        "/wfh\n"
        "/itjobs"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("jobs", jobs))
app.add_handler(CommandHandler("freshers", freshers))
app.add_handler(CommandHandler("wfh", wfh))
app.add_handler(CommandHandler("itjobs", itjobs))
app.add_handler(CommandHandler("help", help_command))

app.run_polling()
