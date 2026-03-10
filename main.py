from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

queues = {}


@app.on_message(filters.command("start"))
async def start(_, message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎧 Play", callback_data="play"),
                InlineKeyboardButton("📜 Queue", callback_data="queue")
            ],
            [
                InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                InlineKeyboardButton("▶ Resume", callback_data="resume")
            ],
            [
                InlineKeyboardButton("⏭ Skip", callback_data="skip")
            ]
        ]
    )

    await message.reply_text(
"""
🎧 **亗RY_Store Music Bot**

Commands:

/play nama lagu
/pause
/resume
/skip
/queue
""",
        reply_markup=buttons
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

    queues.setdefault(message.chat.id, []).append(title)

    await message.reply(f"▶ Memutar: {title}")


@app.on_message(filters.command("pause"))
async def pause(_, message):
    await call.pause_stream(message.chat.id)
    await message.reply("⏸ Musik dijeda")


@app.on_message(filters.command("resume"))
async def resume(_, message):
    await call.resume_stream(message.chat.id)
    await message.reply("▶ Musik dilanjutkan")


@app.on_message(filters.command("skip"))
async def skip(_, message):

    await call.leave_group_call(message.chat.id)

    if message.chat.id in queues:
        queues[message.chat.id] = []

    await message.reply("⏭ Lagu dilewati")


@app.on_message(filters.command("queue"))
async def queue(_, message):

    q = queues.get(message.chat.id)

    if not q:
        return await message.reply("Queue kosong")

    text = "\n".join(q)

    await message.reply(f"📜 Queue:\n{text}")


app.start()
call.start()
app.idle()
