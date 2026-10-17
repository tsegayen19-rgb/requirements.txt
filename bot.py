import os
from pyrogram import Client, filters
import yt_dlp

# Reading credentials from environment variables (GitHub Secrets)
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("media_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hello! 👋 Send me a valid link, and I will download the video/audio for you.")

@app.on_message(filters.text & ~filters.command("start"))
def download_media(client, message):
    url = message.text
    status_msg = message.reply_text("Processing... Please wait ⏳")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            status_msg.edit_text("Downloading... 📥")
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        status_msg.edit_text("Uploading to Telegram... 🚀")
        message.reply_video(video=file_name, caption=f"🎬 {info.get('title', 'Video')}\n\nDownloaded via Bot")

        os.remove(file_name)
        status_msg.delete()

    except Exception as e:
        status_msg.edit_text("Sorry, failed to download. Please make sure the link is correct. ❌")
        print(f"Error: {e}")

print("Bot is running...")
app.run()
      
