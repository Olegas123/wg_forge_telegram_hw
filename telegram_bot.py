import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import validators
import re

TOKEN = '6257220025:AAHSG4lp1QXXsIXorPvO6ae04h6lZfAKw3w'

if TOKEN is None:
    print('Error: Token is not provided!!!')
    exit(1)

def response_manager(url: str) -> str:
    if not validators.url(url):
        return 'Given URL is not valid!'
    print("Downloading video: ", url)

    ydl_opts = {"outtmpl": "%(id)s.%(ext)s",
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            video_data = ydl.extract_info(url, download=False)
            video_id = video_data.get("id", "video")
            ext = video_data.get("ext", "video")
            
            ydl.download([url])
        except yt_dlp.DownloadError:
            return 'Failed to download video!'

    return f"{video_id}.{ext}"

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text

    response: str = response_manager(text)

    if not re.match(".*mp4", response):
        await update.message.reply_text(text=response)
    else:
        await update.message.reply_document(document=open(response, 'rb'))
        os.remove(response)

# Bot usage messages (/start, /help and error message if something bad happens)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! This is a simple python telegram bot " +  
                                    "that allows to download videos to telegram! " + 
                                    "If there are any questions, fell free to write /help")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("If you need to download a video from YT to telegram, " +
                                    "just copy and paste link to a chat!")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.error)
    await update.message.reply_text("Error happened!")

# Main
if __name__ == '__main__':
    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler('start', start))
    bot.add_handler(CommandHandler('help', help))

    bot.add_handler(MessageHandler(filters.TEXT, message_handler))

    bot.add_error_handler(error)

    bot.run_polling(poll_interval=5)
