from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from yt_dlp import YoutubeDL

from config import *

app = Client(
    "rymusicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call = PyTgCalls(app)


@app.on_message(filters.command("start"))
async def start(_, message):

    await message.reply_text(
"""
🎧 亗RY_Store Music Bot

Commands:
/play nama lagu
/skip
"""
)


@app.on_message(filters.command("play"))
async def play(_, message):

    query = " ".join(message.command[1:])

    if not query:
        return await message.reply("Masukkan judul lagu")

    await message.reply("🔎 mencari lagu...")

    ydl_opts = {"format": "bestaudio"}

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]

    url = info["url"]
    title = info["title"]

    await call.join_group_call(
        message.chat.id,
        AudioPiped(url)
    )

    await message.reply(f"▶ Memutar: {title}")


@app.on_message(filters.command("skip"))
async def skip(_, message):

    await call.leave_group_call(message.chat.id)

    await message.reply("⏭ Lagu dilewati")


app.start()
call.start()
app.idle()
