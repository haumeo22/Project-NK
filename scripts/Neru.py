import logging
import sys
import subprocess
import tkinter as tk
from tkinter import scrolledtext
import requests
import threading
import uuid
import time
import os
import re
from pathlib import Path
from datetime import datetime, timedelta

# Load environment variables
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk  # Azure TTS SDK
BASE_DIR = Path("C:/Users/haume/Documents/Active/Programming/NeuroKaylie")
dotenv_path = BASE_DIR / "scripts" / "active" / "Tokens" / "Tokens.env"
load_dotenv(dotenv_path)

# === CONFIG ===
CONTEXTS_DIR = BASE_DIR / "Memories" / "Core Memories" / "Contexts"
OPTIONAL_DIR = BASE_DIR / "Memories" / "Core Memories" / "Optional"
ARCHIVE_DIR = BASE_DIR / "Memories" / "ArchiveMemories"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
SOUNDS_FILE = CONTEXTS_DIR / "Sounds.txt"

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "HammerAI/openhermes-2.5-mistral:latest")
KAYLIE_MODE = os.getenv("KAYLIE_MODE", "stream")  # stream or full

AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_REGION = os.getenv("AZURE_REGION")
VOICE_NAME = os.getenv("VOICE_NAME", "en-AU-NatashaNeural")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

MEMORY_DAYS_TO_LOAD = int(os.getenv("MEMORY_DAYS_TO_LOAD", 1))
KAYLIE_BOOT_TIME = datetime.now()

# Validate credentials
if not AZURE_KEY or not AZURE_REGION:
    raise ValueError("Azure credentials are missing in .env")
if not DISCORD_TOKEN:
    raise ValueError("Discord token is missing in .env")

# === LOGGING SETUP ===
LOG_FILE = BASE_DIR / "neurokaylie_debug.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

# Archive logging
def write_archive(event: str):
    now = datetime.now()
    fname = ARCHIVE_DIR / f"Log {now.day}-{now.month}-{now.year}.txt"
    timestamp = now.strftime("[%H:%M:%S]")
    with open(fname, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {event}\n")

write_archive("\n[BOOT] Kaylie boot up initiated")

# Load sound overrides
def load_sound_map(path: Path):
    sound_map = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, val = line.strip().split('=', 1)
                    sound_map[key.strip()] = val.strip()
    except Exception as e:
        logging.warning(f"Couldn't load sound map: {e}")
    return sound_map

SOUND_OVERRIDES = load_sound_map(SOUNDS_FILE)

# Preprocess text for TTS
def preprocess_for_tts(text: str) -> str:
    text_tts = re.sub(r"\*(.*?)\*", r"[\1]", text)
    text_tts = re.sub(r"(?<!\.)\.\.\.(?![!?])", "<break time='400ms'/>", text_tts)
    text_tts = re.sub(r'\"\"\"', '', text_tts)
    for key, replacement in SOUND_OVERRIDES.items():
        text_tts = re.sub(rf"\b{re.escape(key)}\b", replacement, text_tts, flags=re.IGNORECASE)
        write_archive(f"[TTS] Final SSML payload:\n{ssml}")
    return text_tts

# Load memory contexts
def load_context_texts(directory: Path, limit=None):
    files = sorted([f for f in directory.glob("*.txt") if f.name.lower() != "sounds.txt"])
    if limit:
        files = files[-limit:]
    texts = []
    for f in files:
        try:
            texts.append(f.read_text(encoding="utf-8").strip())
        except:
            pass
    return texts

# Chat memory loader
def load_chat_memory():
    lines = []
    for day_delta in range(MEMORY_DAYS_TO_LOAD):
        d = datetime.now() - timedelta(days=day_delta)
        fname = ARCHIVE_DIR / f"Log {d.day}-{d.month}-{d.year}.txt"
        if fname.exists():
            lines.append(f"=== Memory from {d.day}-{d.month}-{d.year} ===")
            with open(fname, encoding="utf-8") as f:
                for line in f:
                    if "User Input:" in line or "Kaylie Output:" in line:
                        lines.append(line.strip())
    return lines[-25:] if KAYLIE_MODE == "full" else []

# Build memory prompt
def build_memory():
    now = datetime.now().strftime("%H:%M:%S")
    uptime = str(datetime.now() - KAYLIE_BOOT_TIME).split('.')[0]
    parts = [f"Current Time: {now}\nUptime: {uptime}"]
    parts += load_context_texts(CONTEXTS_DIR)
    if KAYLIE_MODE == "full":
        parts += load_context_texts(OPTIONAL_DIR)
        parts += load_chat_memory()
    else:
        parts += ["[STREAM MODE: Minimal context]"]
    memory = "\n\n".join(parts)
    logging.debug(f"Built memory tokens approx: {len(memory.split())}")
    return memory

MEMORY = build_memory()
write_archive("Memory loaded")
logging.info("=== MEMORY LOADED ===")

# Query AI
# === Pollinations API ===
import urllib.parse as ul

def ask_pollinations(user_prompt: str) -> str:
    write_archive(f"User Input: \"{user_prompt}\"")

    # 1) Build the full prompt exactly as before
    memory       = build_memory()
    system_block = f"### SYSTEM:\n{memory}\n"
    full_prompt  = f"{system_block}\n### USER:\n{user_prompt}\n\n### KAYLIE-CHAN:"

    # 2) URL‑encode it for the path
    safe_prompt  = ul.quote(full_prompt, safe="")

    url = f"https://text.pollinations.ai/{safe_prompt}"
    params = {"model": "mistral"}  # or "llama3"

    try:
        resp = requests.get(url, params=params, timeout=20)

        # HTML or other garbage? fail over.
        if resp.ok and not resp.text.lstrip().startswith("<"):
            reply = resp.text.strip().strip('"')
            write_archive(f"Kaylie Output (Pollinations): \"{reply}\"")
            return reply

        write_archive(f"Pollinations failed [{resp.status_code}]: {resp.text[:120]}")
    except Exception as e:
        write_archive(f"Pollinations error: {e}")

    return "[Pollinations error: no response]"



# === Hybrid Selector ===
def ask_kaylie(user_prompt: str) -> str:
    start_time = time.time()
    
    # Try Pollinations first
    reply = ask_pollinations(user_prompt)
    
    # If error, fallback to Ollama
    if "[Pollinations error" in reply or reply == "[No reply]":
        write_archive("Falling back to Ollama...")
        reply = ask_ollama(user_prompt)
    
    elapsed = time.time() - start_time
    write_archive(f"Kaylie total response time: {elapsed:.2f}s")
    return reply


# Play WAV audio
def play_wav_file(path: str):
    try:
        subprocess.run(["powershell", "-Command", f'(New-Object Media.SoundPlayer "{path}").PlaySync();'], check=True)
        write_archive("Received audio, playing audio")
    except Exception as e:
        write_archive(f"Audio playback failed: {e}")

import azure.cognitiveservices.speech as speechsdk
import uuid, os, traceback
from pathlib import Path

def speak_text(text: str):
    try:
        write_archive("[TTS] Starting synthesis")
        tts_text = preprocess_for_tts(text)
        write_archive(f"[TTS] Processed text: {tts_text}")

        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_KEY,
            region=AZURE_REGION
        )
        speech_config.speech_synthesis_output_format = speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        speech_config.speech_synthesis_voice_name = VOICE_NAME  # e.g., en-US-JennyNeural

        audio_folder = BASE_DIR / "scripts" / "active"
        audio_folder.mkdir(parents=True, exist_ok=True)
        filename = audio_folder / f"output_{uuid.uuid4().hex}.wav"
        audio_config = speechsdk.audio.AudioOutputConfig(filename=str(filename))

        synthesizer = speechsdk.SpeechSynthesizer(speech_config, audio_config)

        write_archive("[TTS] Synthesizer ready. Sending SSML...")
        ssml = f"""
<speak xml:lang='en-US'>
  <voice name='{VOICE_NAME}'>
    <prosody pitch='+15%' rate='0%'>{tts_text}</prosody>
  </voice>
</speak>
"""
        result = synthesizer.speak_ssml_async(ssml).get()
        write_archive("[TTS] SSML synthesis completed, checking result...")

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            if os.path.exists(filename):
                write_archive(f"[TTS ✅] Succeeded. WAV saved to: {filename}")
                play_wav_file(str(filename))
            else:
                write_archive(f"[TTS ❌] Claimed success, but file missing: {filename}")
        else:
            cd = result.cancellation_details
            write_archive(f"[TTS ❌] Canceled. Reason: {cd.reason}")
            if cd.reason == speechsdk.CancellationReason.Error:
                write_archive(f"[TTS ❌] Error details: {cd.error_details}")
                if cd.error_details and "code" in cd.error_details:
                    write_archive(f"[TTS ❌] Error code detected in details block")
            logging.error(f"[TTS ❌] {cd.reason} | {cd.error_details}")
    except Exception as e:
        logging.error("Fatal TTS exception:\n" + traceback.format_exc())
        write_archive(f"[TTS 💥] Fatal error: {e}")

# --- GUI send message ---
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return
    chat_win.insert(tk.END, f"You: {user_input}\n", "user")
    entry.delete(0, tk.END)

    def process():
        # ⬇⬇⬇  USE HYBRID BACKEND  ⬇⬇⬇
        reply = ask_kaylie(user_input)
        chat_win.insert(tk.END, f"Kaylie-chan: {reply}\n", "bot")
        speak_text(reply)

    threading.Thread(target=process, daemon=True).start()

# --- Discord integration ---
from DiscordAccess import run_discord
#      ╭────────────────────────────╮
threading.Thread(
    target=lambda: run_discord(
        DISCORD_TOKEN,
        ask_kaylie,      # ← use hybrid backend
        speak_text
    ),
    daemon=True
).start()


# Build GUI
root = tk.Tk()
root.title("NeuroKaylie - Live AI Assistant")
chat_win = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Consolas", 11))
chat_win.pack(padx=10, pady=10)
chat_win.tag_config("user", foreground="cyan")
chat_win.tag_config("bot", foreground="magenta")
entry_frame = tk.Frame(root)
entry_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
entry = tk.Entry(entry_frame, font=("Consolas", 11))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry.bind("<Return>", lambda e: send_message())
send_btn = tk.Button(entry_frame, text="Send", command=send_message)
send_btn.pack(side=tk.RIGHT)

write_archive("Kaylie online")
chat_win.insert(tk.END, "Kaylie-chan: Hmph... I'm here, don't waste my time!\n", "bot")

# Shutdown handler
def safe_shutdown():
    write_archive("[SHUTDOWN] Kaylie offline")
    root.destroy()
root.protocol("WM_DELETE_WINDOW", safe_shutdown)
root.mainloop()
