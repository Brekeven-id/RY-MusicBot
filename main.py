import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from yt_dlp import YoutubeDL

from config import *
import queue

app = Client(
    "RYMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start(client, message):

    msg = await message.reply("⚡ Booting RY System...\n[□□□□□□□□] 0%")

    await asyncio.sleep(1)
    await msg.edit("⚡ Loading Music Engine...\n[■■□□□□□□] 20%")

    await asyncio.sleep(1)
    await msg.edit("⚡ Connecting Voice Server...\n[■■■■□□□□] 40%")

    await asyncio.sleep(1)
    await msg.edit("⚡ Checking Modules...\n[■■■■■■□□] 60%")

    await asyncio.sleep(1)
    await msg.edit("⚡ Starting Music Bot...\n[■■■■■■■■] 100%")

    await asyncio.sleep(1)

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎧 Play Music", callback_data="play"),
                InlineKeyboardButton("📜 Commands", callback_data="help")
            ]
        ]
    )

    await msg.delete()

    await message.reply_photo(
        photo="logo.png",
        caption="""
🎧 **亗RY_Store Music Bot**

Play music in voice chat

Commands

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

    await message.reply("🔎 Searching...")

    ydl_opts = {"format": "bestaudio"}

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]

    url = info["url"]
    title = info["title"]

    queue.add(message.chat.id, title)

    await call.join_group_call(
        message.chat.id,
        AudioPiped(url)
    )

    await message.reply(f"▶ Playing {title}")


@app.on_message(filters.command("pause"))
async def pause(_, message):

    await call.pause_stream(message.chat.id)

    await message.reply("⏸ Music Paused")


@app.on_message(filters.command("resume"))
async def resume(_, message):

    await call.resume_stream(message.chat.id)

    await message.reply("▶ Music Resumed")


@app.on_message(filters.command("skip"))
async def skip(_, message):

    await call.leave_group_call(message.chat.id)

    queue.clear(message.chat.id)

    await message.reply("⏭ Song Skipped")


@app.on_message(filters.command("queue"))
async def q(_, message):

    songs = queue.get(message.chat.id)

    if not songs:
        return await message.reply("Queue kosong")

    text = "\n".join(songs)

    await message.reply(f"📜 Queue:\n{text}")


app.start()
call.start()
app.idle()
