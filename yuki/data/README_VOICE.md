# Yuki Voice Reference Audio

## Missing File: `yuki_voice.wav`

This directory should contain a reference audio file for LuxTTS voice cloning.

### Requirements:

- **Filename**: `yuki_voice.wav`
- **Format**: WAV (uncompressed)
- **Sample Rate**: 48kHz (recommended) or 44.1kHz
- **Channels**: Mono or Stereo (both work)
- **Duration**: 3-10 seconds minimum
- **Voice**: Male voice (as specified by user)
- **Quality**: Clear audio, minimal background noise

### How to Create the Reference Audio:

#### Option 1: Use Free TTS Services
1. Visit a free TTS website (e.g., https://ttsmaker.com/, https://voicegenerator.io/)
2. Select a male voice you like
3. Generate a 5-10 second sample saying something neutral (e.g., "Hello, how can I help you today?")
4. Download as MP3/WAV
5. Convert to WAV 48kHz if needed (using Audacity or FFmpeg)
6. Rename to `yuki_voice.wav` and place in this directory

#### Option 2: Record Your Own Voice
1. Open Windows Voice Recorder or Audacity
2. Record a 5-10 second clip in a quiet environment
3. Speak clearly and naturally
4. Export as WAV (48kHz if possible)
5. Save as `yuki_voice.wav` in this directory

#### Option 3: Use FFmpeg to Convert Existing Audio
```bash
# Convert any audio file to WAV 48kHz mono
ffmpeg -i input.mp3 -ar 48000 -ac 1 yuki_voice.wav

# Or from YouTube/online video
yt-dlp -x --audio-format wav "VIDEO_URL"
ffmpeg -i downloaded.wav -ar 48000 -ac 1 -t 10 yuki_voice.wav
```

### What Happens If File is Missing?

If `yuki_voice.wav` is not found, Yuki will:
1. Log a warning message
2. Run in **text-only mode** (no voice synthesis)
3. Display responses only in the status window
4. Continue functioning normally for all other features

### Testing Your Reference Audio:

After adding the file, restart Yuki and check the logs:
- Look for: `✓ LuxTTS initialized successfully`
- If you see: `Reference audio not found`, check the file path and format

### File Path:

The file should be located at:
```
YukiAI/yuki/data/yuki_voice.wav
```

Full path on Windows:
```
C:\Workspace\YukinoAI\yuki\data\yuki_voice.wav
```

### Tips for Best Voice Quality:

1. **Clear speech**: No mumbling or unclear pronunciation
2. **Consistent tone**: Don't shout or whisper
3. **No background noise**: Record in a quiet room
4. **Good microphone**: Use a decent mic if recording yourself
5. **Natural pacing**: Not too fast or too slow

### Example Text for Recording:

> "Hello, this is a test of the voice synthesis system. I'm speaking clearly and naturally to provide a good reference sample for voice cloning."

This text is about 10 seconds long and provides good phonetic variety.

---

**Once you've added the file, you're ready to run Yuki with voice synthesis!** 🎤
