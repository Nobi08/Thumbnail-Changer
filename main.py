import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyromod import listen

# ===== CREDENTIALS =====
# You can hardcode OR use environment variables

BOT_TOKEN = "7989912852:AAGM8cbkj8whriiFuKzcpH0XHeDgBeUXgQ0
API_ID = 23309615   # must be int
API_HASH = "df851f5ea654830ce6a42c1d926b3121"

# =======================

Bot = Client(
    "Thumb-Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

START_TXT = """Hi {}, I am a video thumbnail changer bot.
Send a video or file to get started.
"""

START_BTN = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Source Code", url="https://github.com")]]
)

thumb = ""  # WARNING: single-user safe only

@Bot.on_message(filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        START_TXT.format(update.from_user.mention),
        reply_markup=START_BTN,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.private & (filters.video | filters.document))
async def thumb_change(bot, m):
    global thumb

    msg = await m.reply("Downloading file...")
    file_path = await bot.download_media(m)

    # Ask for thumbnail (FIXED: never empty)
    if thumb:
        text = "Now send the thumbnail photo or /keep to reuse old one"
    else:
        text = "Now send the thumbnail photo"

    answer = await bot.ask(m.chat.id, text)

    if answer.text and answer.text == "/keep" and thumb:
        pass
    elif answer.photo:
        if thumb and os.path.exists(thumb):
            os.remove(thumb)
        thumb = await bot.download_media(answer.photo)
    else:
        await m.reply("Invalid input. Send a photo.")
        return

    await msg.edit("Uploading...")

    if m.document:
        await bot.send_document(
            m.chat.id,
            document=file_path,
            thumb=thumb,
            caption=m.caption
        )
    else:
        await bot.send_video(
            m.chat.id,
            video=file_path,
            thumb=thumb,
            caption=m.caption
        )

    os.remove(file_path)

Bot.run()
