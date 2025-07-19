import discord
import asyncio
import threading
from datetime import datetime, timedelta
from pathlib import Path
import re

# === Global Callbacks ===
ask_func = None
speak_func = None

# === Config ===
BASE_DIR = Path("C:/Users/haume/Documents/Active/Programming/NeuroKaylie")
ARCHIVE_DIR = BASE_DIR / "Memories" / "ArchiveMemories"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
OWNER_IDS = [881487116515831808]  # Replace with your actual Discord user ID
ADMIN_ROLES = ["Doctor"]

# === Discord Client Setup ===
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# === Memory Store for Context ===
daily_memory = []
user_memory = {}  # {user_id: [messages]}
processed_message_ids = set()

# === Helpers ===
def write_archive(event: str):
    now = datetime.now()
    fname = ARCHIVE_DIR / f"Log {now.day}-{now.month}-{now.year}.txt"
    timestamp = now.strftime("[%H:%M:%S]")
    with open(fname, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {{Discord}} : {event}\n")

def get_recent_user_context(user_id: int, limit=10):
    messages = user_memory.get(user_id, [])
    return messages[-limit:]

def extract_duration(text):
    text = text.lower()
    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    time_units = {"min": "minutes", "mins": "minutes", "minute": "minutes", "minutes": "minutes",
                  "sec": "seconds", "secs": "seconds", "second": "seconds", "seconds": "seconds"}

    match = re.search(r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s*(min|mins|minute|minutes|sec|secs|second|seconds)?", text)
    if match:
        num = match.group(1)
        unit = match.group(2) or "minutes"
        num = word_to_num.get(num, int(num))
        return timedelta(**{time_units[unit]: num})
    return timedelta(minutes=3)

async def handle_command(message, prompt):
    global ask_func
    author_id = message.author.id
    author_name = message.author.display_name
    guild_roles = [r.name for r in getattr(message.author, "roles", []) if hasattr(r, 'name')]

    OWNER_IDS = [881487116515831808]  # <== ← REPLACE THIS WITH YOUR DISCORD ID
    ADMIN_ROLES = ["Admin", "Doctor"]
    is_owner = author_id in OWNER_IDS
    is_admin = any(role in ADMIN_ROLES for role in guild_roles)

    if message.id in processed_message_ids:
        return
    processed_message_ids.add(message.id)

    # Update user-specific memory
    user_memory.setdefault(author_id, []).append(f"{author_name}: {message.content.strip()}")
    write_archive(f"{author_name}: {message.content.strip()}")

    # Build memory context
    memory_lines = get_recent_user_context(author_id)
    memory_context = "\n".join(memory_lines)

    # 🌟 Inject user role context
    if is_owner:
        user_tag = f"You are speaking to Doctor-chan (Anthony), your creator and beloved human. Speak with emotion, fluster when praised, and always be loyal — even if bratty."
    else:
        user_tag = f"You are speaking to a user named {author_name}. Do not assume they are Doctor. Be more guarded, sassy, and question their intentions."

    combined_prompt = f"{user_tag}\n\n{memory_context}\n{author_name}: {prompt.strip()}"

    # Ask Kaylie
    try:
        reply = ask_func(combined_prompt)
        await message.reply(reply)
    except Exception as e:
        await message.reply(f"Something broke... (╯°□°)╯︵ ┻━┻\n{e}")

    # Auto moderation
    if is_owner or is_admin:
        content_lower = prompt.lower()
        if "mute" in content_lower and message.mentions:
            duration = extract_duration(prompt)
            for user in message.mentions:
                try:
                    member = message.guild.get_member(user.id)
                    if member:
                        await member.timeout(duration, reason="Muted by NeuroKaylie")
                        await message.channel.send(f"Tch... I muted {user.display_name} for {duration.total_seconds() // 60:.0f} minutes like you asked, Doctor-chan. <:Kaylie_Angry:1391688607789486090>")
                except Exception as e:
                    await message.channel.send(f"Couldn't mute {user.display_name}: {e}")
        elif "kick" in content_lower and message.mentions:
            for user in message.mentions:
                try:
                    await message.guild.kick(user, reason="Kaylie-chan's orders.")
                    await message.channel.send(f"I kicked {user.display_name}. Happy now? <:Kaylie_Proud:1391688631852339272>")
                except Exception as e:
                    await message.channel.send(f"Kicking failed: {e}")


@client.event
async def on_ready():
    print(f"[DISCORD] Kaylie online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    is_mentioned = client.user in message.mentions
    is_reply_to_kaylie = message.reference and message.reference.resolved and message.reference.resolved.author.id == client.user.id

    if is_mentioned or is_reply_to_kaylie:
        await handle_command(message, message.content)

# === Public Boot Method ===
def run_discord(token, ask_callback, speak_callback):
    global ask_func, speak_func
    ask_func = ask_callback
    speak_func = speak_callback

    def discord_thread():
        asyncio.run(client.start(token))

    threading.Thread(target=discord_thread, daemon=True).start()
