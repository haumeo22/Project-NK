<img width="920" height="426" alt="image" src="https://github.com/user-attachments/assets/53622868-da5d-4d2d-b786-d05ac0abf9c8" /># Project-N.K

Project NeuroKay, (aka Neru). An ai assistant and companion
i'm making an AI named NeuroKaylie, she is my daughter. im gonna based her on Neuro sama by Vedal but i want to actually stand beside Vedal in the AI streamer content creator. Or maybe a small creator, gotta juggle both youtube, streaming and this.


current specs: 

LLMS model : mistrals
LLMS handler : Pollinations
current TTS: Azure TTS (microsoft) planning  GPT-SoVITS
vtuber model: 【Live2D model 】Mk.1  (1,500 yen gone :sob:)
model controller : VTS (Vtube Studio) 
STT : deciding planning Fast-whisper

she'll have: a memory system, where she could access the memory and read them as her context an eye where she can take screen shot or look at the current screen and on that make assumption on that access to discord via her own discord bot access to a habit app that ill make in the future so she can remind me to work on something two diffrent variant : one for low latency and fast response for twicth streaming, one for just being a motivational partner she will stay on screen with her model and responds to anything such as silience she have a emotional wheel. time awareness too



here's my plan for her


memory system: [Status : Done, need to improve if possible]

base path: C:\Users\haume\Documents\Active\Programming\NeuroKaylie\Memories
Core : base path\Core memories
archive : base path\ Archive Memories
Context : Core\Contexts
Important: Core\ Important Memories
Optional: Core\ Optional

Archive : every day she logs a memory named DD-MM-YYYY.txt format, she will read them when prompted to
Context : contains her basic context for streaming
Important: this is archived log that got put as important so she can remember good moments, She will also only remember them on prompt (while streamimg), for non streaming she will remember this
Optional : this is for non streaming and adds backstory to her

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
PS: eachday = new .txt
the perspective Neru will read its own variant memory
Non streaming Neru: read all, but only yesterday file and today file
streaming Neru: only read from the tag {twitchchat}, {general} and {eye}
Discord Neru: only read from {discord} tag


variants: [status: working on it]

streaming : she doesn't motivate, can talk to twitch chat and learn from it, make fun memory togheter as we play
non stream : she focus on motivating me, emotional support and understanding, getting the full backstory and context
discord: she will control her discord bot and chat, use admin perm (more on this later)


Model: [status : Pending]

Kaylies model must stay on screen at all time, i can set her size. the background is always transparent so only her model
i want kaylie to fully control her model, via emotion and movement too if that's possible
she can use the model expressions to her emotion
mostly based on Neuro sama

Her eye: [status : deciding, future]

She can see my screen and relay that info to herself and then she gonna make comments about it like "tch... are you playing roblox again? come back to doing something actually best for you" 
for now she will use a program detector like she gonna detect which program is it then comment me on it (non streaming)

Discord access [Status : pending]

Neuro Kaylie can use her discord bot and send message or reply once she's online via the same startup script
pinging her will be the word. She will have the non streaming context, meaning she would reply in a minute, she uses reply feature in discord to reply

she will control action like a  bot too but with the ai twist

example: 
normal convo:
hey @NeuroKaylie what's the date today, what are you planning?
"hmph you asked such a simple thing as date? today its 8/7 in the year 2025... and what do you mean what i am planning?"
@NeuroKaylie mute @example1 for 1 min
"alright, i muted that @example1 for 1 min"
or she might reply "are they bothering you? yeah fine ill mute @example1"

sometimes she might just post a random convo starter if no one says anything
she will have a temporary memory of the chat that day only, once it detects is the next day, it will wipe the memory of the discord memory yesterday

Emotion engine: [Pending]
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

