from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
import json
import os

DATA_FILE = "videos.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        video_db = json.load(f)
else:
    video_db = []

async def check_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        uid = update.message.video.file_unique_id

        if uid in video_db:
            await update.message.delete()
        else:
            video_db.append(uid)
            with open(DATA_FILE, "w") as f:
                json.dump(video_db, f)

TOKEN = os.getenv("BOT_TOKEN")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.VIDEO, check_video))

print("Bot berjalan...")
app.run_polling()
