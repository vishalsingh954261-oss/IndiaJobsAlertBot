from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import os
import json
import requests

TOKEN = os.getenv("BOT_TOKEN")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
ADMIN_ID = 6486827183

if not TOKEN:
    raise ValueError("BOT_TOKEN not found")

JOBS_FILE = "jobs.json"

# -------------------
# Load jobs
# -------------------
def load_jobs():
    try:
        with open(JOBS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# -------------------
# Save jobs
# -------------------
def save_jobs(jobs):
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f, indent=4)

# -------------------
# Keyboard
# -------------------
keyboard = [
    ["📋 Latest Jobs", "🎓 Freshers Jobs"],
    ["🏠 Work From Home", "💻 IT Jobs"],
    ["⭐ Premium", "ℹ️ Help"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

# -------------------
# Start
# -------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇮🇳 Welcome to India Jobs Alert Bot",
        reply_markup=reply_markup
    )

# -------------------
# Admin
# -------------------
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Access Denied")
        return

    await update.message.reply_text(
        "🔧 ADMIN PANEL\n\n"
        "/addjob\n"
        "/listjobs\n"
        "/deletejob\n"
        "/broadcast"
    )

# -------------------
# Add Job
# -------------------
async def addjob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = update.message.text.replace("/addjob ", "")

    parts = text.split("|")

    if len(parts) != 10:
        await update.message.reply_text(
            "Format:\n"
            "/addjob Job Title | Company | Salary | City | Area | Experience | Job Type | Skills | Description | Apply Link"
        )
        return

    jobs = load_jobs()

    jobs.append({
        "title": parts[0].strip(),
        "company": parts[1].strip(),
        "salary": parts[2].strip(),
        "city": parts[3].strip(),
        "area": parts[4].strip(),
        "experience": parts[5].strip(),
        "type": parts[6].strip(),
        "skills": parts[7].strip(),
        "description": parts[8].strip(),
        "link": parts[9].strip()
    })

    save_jobs(jobs)

    await update.message.reply_text("✅ Job Added Successfully")

# -------------------
# List Jobs
# -------------------
async def listjobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    jobs = load_jobs()

    if not jobs:
        await update.message.reply_text("No jobs available.")
        return

    msg = ""

    for i, job in enumerate(jobs, start=1):
        msg += f"{i}. {job['title']} - {job['company']}\n"

    await update.message.reply_text(msg)

# -------------------
# Delete Job
# -------------------
async def deletejob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        index = int(context.args[0]) - 1

        jobs = load_jobs()

        removed = jobs.pop(index)

        save_jobs(jobs)

        await update.message.reply_text(
            f"Deleted: {removed['title']}"
        )

    except:
        await update.message.reply_text(
            "Usage:\n/deletejob 1"
        )

# -------------------
# Broadcast
# -------------------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "Broadcast feature coming soon."
    )

# -------------------
# Buttons
# -------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 Latest Jobs":
        jobs = load_jobs()

        if not jobs:
            await update.message.reply_text(
                "No jobs available."
            )
            return

        for job in jobs:
            await update.message.reply_text(
                f"🏢 Company: {job['company']}\n"
                f"💼 Job Title: {job['title']}\n"
                f"💰 Salary: {job['salary']}\n"
                f"📍 City: {job['city']}\n"
                f"📌 Area: {job['area']}\n"
                f"🕒 Experience: {job['experience']}\n"
                f"📄 Job Type: {job['type']}\n"
                f"🛠 Skills: {job['skills']}\n"
                f"📝 Description:\n{job['description']}\n"
                f"🔗 Apply:\n{job['link']}"
            )

    elif text == "🎓 Freshers Jobs":
        await update.message.reply_text(
            "Showing Freshers Jobs"
        )

    elif text == "🏠 Work From Home":
        await update.message.reply_text(
            "Showing Work From Home Jobs"
        )

    elif text == "💻 IT Jobs":
        await update.message.reply_text(
            "Showing IT Jobs"
        )

    elif text == "⭐ Premium":
        await update.message.reply_text(
            "Premium Coming Soon"
        )

    elif text == "ℹ️ Help":
        await update.message.reply_text(
            "Contact admin for support."
        )

# -------------------
# App
# -------------------
async def googlejobs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/googlejobs python developer hyderabad"
        )
        return

    query = " ".join(context.args)

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_jobs",
        "q": query,
        "api_key": SERPAPI_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        jobs = data.get("jobs_results", [])

        if not jobs:
            await update.message.reply_text(
                "No jobs found."
            )
            return

        for job in jobs[:5]:
    title = job.get("title", "Not Available")
    company = job.get("company_name", "Not Available")
    location = job.get("location", "Not Available")

    description = job.get(
        "description",
        "No description available."
    )

    salary = job.get(
        "detected_extensions",
        {}
    ).get(
        "salary",
        "Salary Not Mentioned"
    )

    posted = job.get(
        "detected_extensions",
        {}
    ).get(
        "posted_at",
        "Posting date not available"
    )

    job_type = job.get(
        "detected_extensions",
        {}
    ).get(
        "schedule_type",
        "Not Mentioned"
    )

    via = job.get(
        "via",
        "Google Jobs"
    )

    apply_options = job.get(
        "related_links",
        []
    )

    message = (
        f"🏢 Company: {company}\n"
        f"💼 Job Title: {title}\n"
        f"💰 Salary: {salary}\n"
        f"📄 Job Type: {job_type}\n"
        f"🕒 Posted: {posted}\n"
        f"📍 Location: {location}\n"
        f"🌐 Source: {via}\n\n"
        f"📝 Full Description:\n\n"
        f"{description}\n\n"
    )

    if apply_options:
        message += "🔗 Apply Links:\n"

        for link in apply_options[:10]:
            url = link.get("link")
            source = link.get("source", "Apply")

            if url:
                message += f"{source}: {url}\n"

    await update.message.reply_text(
        message[:4000]
    )
    except Exception as e:
        await update.message.reply_text(
            f"Error: {str(e)}"
        )
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("addjob", addjob))
app.add_handler(CommandHandler("listjobs", listjobs))
app.add_handler(CommandHandler("deletejob", deletejob))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("googlejobs", googlejobs))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        button_handler
    )
)

print("Bot Started...")
app.run_polling()
