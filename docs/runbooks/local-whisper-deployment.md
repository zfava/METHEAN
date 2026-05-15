# Local Whisper Deployment

A small FastAPI wrapper around ``faster-whisper`` that exposes the
same request/response shape the OpenAI Whisper provider uses, so the
METHEAN backend can swap providers without code changes.

This document is design-only for v2; the actual service has not been
deployed against the production homestead cluster yet.

## Hardware

- Mac mini M5 Pro, 48 GB RAM minimum recommended.
- Model: ``large-v3-turbo`` (faster-whisper).
- Expected P95: ~2.5s for a 5-second utterance under load.

## Software

```bash
# On the Mac mini:
pyenv install 3.11.9
pyenv local 3.11.9
python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install faster-whisper fastapi uvicorn python-multipart
```

## Service wrapper

```python
# /Users/methean/whisper-service/main.py
from fastapi import FastAPI, File, UploadFile, Form
from faster_whisper import WhisperModel
import tempfile, os

app = FastAPI()
model = WhisperModel("large-v3-turbo", device="auto", compute_type="auto")

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...), language: str = Form("en")):
    # The temp file is local; the upstream METHEAN backend already
    # validated that the kid agreed via parent policy. Audio is
    # deleted immediately after transcription returns.
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as fh:
        fh.write(await audio.read())
        path = fh.name
    try:
        segments, info = model.transcribe(path, language=language, beam_size=5)
        text = "".join(s.text for s in segments).strip()
        return {
            "text": text,
            "duration": info.duration,
            "confidence": float(info.language_probability or 0.0),
            "language": info.language or language,
        }
    finally:
        os.unlink(path)

@app.get("/health")
async def health():
    return {"ok": True}
```

## launchd unit (macOS)

```xml
<!-- ~/Library/LaunchAgents/com.methean.whisper.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
  <key>Label</key><string>com.methean.whisper</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/methean/whisper-service/.venv/bin/uvicorn</string>
    <string>main:app</string>
    <string>--host</string><string>0.0.0.0</string>
    <string>--port</string><string>9000</string>
  </array>
  <key>WorkingDirectory</key>
  <string>/Users/methean/whisper-service</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key>
  <string>/Users/methean/whisper-service/stdout.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/methean/whisper-service/stderr.log</string>
</dict>
</plist>
```

Load with ``launchctl load -w
~/Library/LaunchAgents/com.methean.whisper.plist``.

## Health check

```bash
curl http://mac-mini-1.local:9000/health
# {"ok": true}
```

The METHEAN backend's ``LocalWhisperProvider`` does the same probe
in ``app.services.whisper.factory._local_alive`` before routing a
household to the local service.

## Model update

```bash
# Pre-cache the next model version before swapping
python -c "from faster_whisper import WhisperModel; WhisperModel('large-v3-turbo')"

# Edit main.py to use the new model name, launchctl unload + load.
```

## Privacy

The wrapper writes a temp file briefly during transcription; the
``finally`` block always unlinks it. No transcripts are logged.

To run the service entirely in-RAM (skip the temp file), use
``faster-whisper``'s in-memory bytes loading path with a custom
``Decoder``; left as a follow-up since the simpler temp-file path
satisfies the kid-privacy boundary (the file lives on the homestead
LAN, never leaves it).
