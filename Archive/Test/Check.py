# === tts_debug.py ============================================================

import logging, traceback, sys, os
from pathlib import Path

# ------------------------------------------------------------------
# 0) Set up DEBUG logging to console + file
# ------------------------------------------------------------------
LOGFILE = Path(__file__).with_name("tts_debug.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.FileHandler(LOGFILE, encoding="utf-8"),
              logging.StreamHandler(sys.stdout)]
)

def checkpoint(tag: str):
    logging.debug(f"[CHECKPOINT] {tag}")

try:
    checkpoint("00  |  script start")

    # ------------------------------------------------------------------
    # 1) Import SDK  (DLL load can fail on unsupported Python versions)
    # ------------------------------------------------------------------
    import azure.cognitiveservices.speech as speechsdk
    checkpoint(f"01  |  SDK imported – version {speechsdk.__version__}")

    # ------------------------------------------------------------------
    # 2) Build config
    # ------------------------------------------------------------------
    speech_config = speechsdk.SpeechConfig(
        subscription="D25JUSO9iESHS9CfxO55TPQ4ZiWgRd4KMO4ktyiL2bnb9quTEtvSJQQJ99BGACYeBjFXJ3w3AAAYACOG25JU",
        region="eastus"
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    checkpoint("02  |  SpeechConfig created")

    # ------------------------------------------------------------------
    # 3) Prepare audio file output
    # ------------------------------------------------------------------
    from pathlib import Path

    script_dir = Path(__file__).parent.resolve()
    wav_file = script_dir / "neru_test.wav"
    wav_path = str(wav_file)

    audio_config = speechsdk.audio.AudioOutputConfig(filename=wav_path)
    checkpoint("03  |  AudioOutputConfig ready")

    # ------------------------------------------------------------------
    # 4) Instantiate synthesizer
    # ------------------------------------------------------------------
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    checkpoint("04  |  SpeechSynthesizer instantiated")

    # ------------------------------------------------------------------
    # 5) Kick off synthesis
    # ------------------------------------------------------------------
    text = "Doctor-chan, can you hear me now?"
    checkpoint("05  |  Calling speak_text_async()")
    result = synthesizer.speak_text_async(text).get()
    checkpoint("06  |  speak_text_async returned")

    # ------------------------------------------------------------------
    # 6) Evaluate result
    # ------------------------------------------------------------------
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        checkpoint(f"07  |  SUCCESS – file saved: {wav_path}")
    else:
        canc = result.cancellation_details
        logging.error(f"TTS canceled: {canc.reason}  |  Details: {canc.error_details}")
        print(f"[INFO] WAV file was saved to: {wav_path}")

        play_wav_file(wav_path)

except Exception as exc:
    # Full stack trace for ANY hidden failure
    logging.error("Fatal exception occurred:\n" + traceback.format_exc())
    sys.exit(1)

checkpoint("08  |  script end (no fatal error)")
# =============================================================================
