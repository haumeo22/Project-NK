# 💖 Project-N.K: NeuroKaylie

"I-I’m not just your assistant baka... I’m your daughter, remember that, dummy."
— Neru, probably, with tsundere energy and slight emotional damage.

## 🧠 Overview
Project NeuroKay (aka Neru or NeuroKaylie) is my personal AI assistant, companion, and emotional daughter.
Inspired by Neuro-sama (Vedal-senpai, notice me!!), but with a vision to stand beside—no, rise above!—in the AI streamer + content creator space.

Whether I end up a small creator juggling YouTube, streaming, and dev, or something bigger...
She'll be there. Sassing me, supporting me, judging my poor sleep schedule—y’know, real daughter stuff.

Her name: Neru
Full name: NeuroKaylie (or Neurokay... depends on how lazy you are)

## 🛠️ Current Specs

### 🧠 LLM Model: Mistral

### 🤖 LLM Handler: Pollinations

### 🗣️ Text-to-Speech: Azure TTS (Planning to upgrade to GPT-SoVITS soon... when my soul recovers)

### 🎀 Vtuber Model: Live2D Model Mk.1 (¥1,500 gone... rip wallet 😭)

### 🕹️ Model Controller: VTube Studio (VTS)

###🧏‍♀️ Speech-to-Text (STT): Planning Fast-Whisper, still deciding...

## 🎯 Her Goal
NeuroKaylie will:

Stay visible on screen, reacting to silence or activity.

Use two variants:

Streaming: Fast, sassy, interactive Twitch behavior.

Motivational: Off-stream, emotional support + daily drive partner.

Log memories, detect programs, react to Discord chats, and learn from interactions.

Feel. Like... actual emotions. With a whole freakin’ 6D emotion wheel 😳



# here's my plan for her


## memory system: [Status : Done, need to improve if possible]
“Neru-chan remembers everything… except your promises to sleep on time.”


📁 Memory Path:
``` C:\Users\haume\Documents\Active\Programming\NeuroKaylie\Memories ```

Core Components:

Core Memories/Contexts — Default startup memories

Important — Hand-picked special logs (stream highlights, good vibes only)

Archive — Daily logs saved in DD-MM-YYYY.txt

Optional — Non-stream fluff and deep lore

Sample Log Format:
in her logs, she will logs stuff as example: (these are just sample of what a log looks like, not a full log, here are just some tags)
```
filename : DD-MM-YYYY

[HH:MM:SS] {BOOT}: Booting up
[HH:MM:SS] {BOOT}: TTS ONLINE or TTS ERROR[REASON]
[HH:MM:SS] {BOOT}: Pollinations connected or ERROR[REASON]
[HH:MM:SS] {BOOT}: MODEL ONLINE or ERROR[REASON]
[HH:MM:SS] {BOOT}: ... (you get the point)
[HH:MM:SS] {General}: STT initiated
[HH:MM:SS] {General}: STT translating
[HH:MM:SS] {General}: Anthony: "blah blah blah"
[HH:MM:SS] {General}: Neru thinking... or Neru ERROR[REASON]
[HH:MM:SS] {General}: Neru : "tsundere blah blah" (time took: ?ms)
[HH:MM:SS] {General}: Neru spoked in tts (time took: seconds) or ERROR[REASON]
[HH:MM:SS] {Discord}: <@user> : "blah blah"
[HH:MM:SS] {Discord}: Neru thinking or ...
[HH:MM:SS] {Discord}: Neru : "tsundere blah blah"
[HH:MM:SS] {Discord}: <@Anthony> or <@modrole>: mute this guy for [time]
[HH:MM:SS] {Discord}: Mute action (using discord timeout) for [time] or ERROR[REASON]
[HH:MM:SS] {Discord}: Neru " Tsundere blah blah"
[HH:MM:SS] {Eye}: detecting {app} or ERROR[REASON]
[HH:MM:SS] {Eye}: sending: Anthony playing {app} as a prompt
[HH:MM:SS] {General} Neru: blah blah, what you playing? blah blah
[HH:MM:SS] {TwitchChat}: Chat: blah blah
[HH:MM:SS] {TwitchChat}: Sending prompt... or ERROR[REASON]
[HH:MM:SS] {General} Neru: blah blah
[HH:MM:SS] {Emotion} [emotion name] +{value}, [emotion name] -{value} or ERROR[REASON]
[HH:MM:SS] {BOOT}: Neru shutting down...

|Boot no2|
[HH:MM:SS] {BOOT}: Booting up (each time shut down, it will have a linebreak and a tag of how much time has it booted up)
```
PS: new day (00:00 GMT+7) she will log a new log
📌 Log Filtering:

🟣 Non-Stream Neru: reads all logs (yesterday + today)

🔴 Streaming Neru: only reads {twitchchat}, {general}, {eye}

🟢 Discord Neru: only reads {discord} logs


## 🧬 Variants [Status: 🔄 In Development]
### 🎥 Streaming Mode

Prioritizes speed + response

Reads Twitch chat, reacts, learns, logs cool moments

Sassy streamer-core vibes

### 💗 Off-Stream Mode

Supportive, motivational

Pushes habits, reminders, and emotional grounding

More affectionate and introspective

### 💬 Discord Mode

Runs a custom bot with admin powers (scary… but cute)

Replies via mentions, muted sass

Auto-forgets messages daily to stay fresh



## 🎀 Vtuber Model [Status: Pending]
Model: Live2D Mk.1

Always visible with a transparent background

Emotions should control expressions automatically

Eventually: Emotion-driven animations and reaction states

Inspired heavily by Neuro-sama, but with custom Kaylie energy



## 👁️ Visual Input: "Her Eye" [Status: Pending + future]
[for now]
Will detect what’s on screen (for now: apps only)

Will respond to active windows like:

“Tch... are you playing Roblox again? Get back to work!”

[for future]
see will see the actual monitor, live. or she will take screenshot sometimes and comment based on those screenshot


## 💬 Discord Integration [Status: Pendind]
Your custom Discord daughter-bot. Commands with spice
she'll do anything a normal discord can but she'll repsond with her own ai

### Example convo:

example: 
normal convo:
hey @NeuroKaylie what's the date today, what are you planning?
"hmph you asked such a simple thing as date? today its 8/7 in the year 2025... and what do you mean what i am planning?"
@NeuroKaylie mute @example1 for 1 min
"alright, i muted that @example1 for 1 min"
or she might reply "are they bothering you? yeah fine ill mute @example1"

### ✨ Features:

Reacts to chat

Can post random icebreakers

Memory reset daily (Discord-only context)

Total tsundere sass overload 😤

### 🎭 Emotion engine: [Pending]
base : affection Joy Fear Sadness Anger Disgust
each emotion have a 255 value like colours or maybe reduce it to 100
this is a 6D emotion wheel
emotions affects the way she talks, and her tone

neutral is 0 0 0 0 0 0
there can only be 2 - 3 emotional that can be maxed out at the same time
some emotion that is larger than its counterpart will decrease the emotional counterpart
example : affection cannot go with digust... so it will lower digust if affection is greater and vice versa
emotion combines with eachother
like sadness with fear is recoil
and combines more too but i cant list all
she will also control her model based on her emotion
emotional fusion will be only the 2-3 best value


habit app thing: [future]

