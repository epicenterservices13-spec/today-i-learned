# Offline CPU Voice Synthesis with Pocket-TTS in PRoot ARM64

Deploying `kyutai/pocket-tts` inside a PRoot Ubuntu container on Android ARM64 for zero-latency, offline text-to-speech.

## Context

Cloud-based TTS APIs introduce rate limits, recurring costs, and latency that degrade autonomous agent loops. Running standard TTS models directly on mobile Android faces broken PyTorch dependencies in Termux. Operating inside an isolated PRoot Ubuntu environment with PyTorch CPU wheels and a gated Hugging Face token enables reliable local voice synthesis.

## Implementation / Code

```bash
# 1. Enter PRoot container and establish virtual environment
proot-distro login ubuntu -- bash -c "
  python3 -m venv ~/10_DEV/14_TOOLS/pocket-tts/venv
  source ~/10_DEV/14_TOOLS/pocket-tts/venv/bin/activate
  pip install --upgrade pip
  pip install --index-url https://download.pytorch.org/whl/cpu torch
  pip install pocket-tts
"

# 2. Authenticate gated weights (requires canReadGatedRepos permissions)
proot-distro login ubuntu -- bash -c "
  mkdir -p ~/.cache/huggingface
  echo 'hf_xxxxxxxxxxxxxxxxxxxx' > ~/.cache/huggingface/token
  chmod 600 ~/.cache/huggingface/token
"

# 3. Synthesize audio without cloud dependency
proot-distro login ubuntu -- bash -c "
  source ~/10_DEV/14_TOOLS/pocket-tts/venv/bin/activate
  pocket-tts --voice alba --text 'Sovereign systems run locally.' --output voiceover.wav
"
```

## Takeaways

- CPU-only PyTorch wheels avoid GPU driver mismatch issues in PRoot ARM64 chroots.
- Hugging Face gated tokens must reside at `~/.cache/huggingface/token` with `chmod 600`.
- Wrapping the command in a host script (`turtle-speak`) provides direct invocation from Termux.
