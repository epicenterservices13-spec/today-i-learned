# Asymmetric Cloud Media Chunking via Colab Drive Mount

Decouple media ingestion and compute by mounting remote cloud storage directly inside Google Colab, extracting telemetry and thumbnail chunks in place, and pulling only lightweight metadata packages to edge terminals.

## Context

Handheld Android Termux and PRoot Linux environments operate under strict thermal throttling, limited storage capacity, and cellular data constraints. When working with multi-gigabyte video uploads (e.g. 10 raw 4K/HD video streams totaling 2.21 GiB), pulling full media files to a mobile node simply to run `ffprobe` or extract sample frames exhausts device flash storage and bandwidth.

Attempting to process large media files locally causes:
1. Thermal runaway and aggressive CPU throttling on mobile SoCs.
2. Android Phantom Process Killer intervention on heavy FFmpeg/Python pipelines.
3. Wasteful download/upload cycles over mobile networks.

Mounting the authoritative cloud storage remote (Google Drive) directly inside an ephemeral cloud GPU/CPU runtime (Google Colab) allows heavy media decoding and keyframe extraction to execute in Google's datacenter fabric without transmitting raw video bytes over local wireless links.

## Implementation / Code

### 1. Colab Cloud Extraction Engine (`turbo_metadata_chunker.ipynb`)

In the Colab notebook, mount Google Drive and inspect the raw video directory directly:

```python
from google.colab import drive
import os, sys, json, subprocess
from pathlib import Path

# Mount Google Drive filesystem into Colab container
drive.mount('/content/drive')

DRIVE_ROOT = Path('/content/drive/MyDrive')
INPUT_DIR = DRIVE_ROOT / '00_INBOX' / '01_RAW' / '20261028'
OUTPUT_DIR = INPUT_DIR / 'metadata'
THUMBS_DIR = OUTPUT_DIR / 'thumbnails'

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
THUMBS_DIR.mkdir(parents=True, exist_ok=True)
```

### 2. In-Cloud Telemetry and Sample Keyframe Slicing

Execute `ffprobe` and `ffmpeg` against the cloud-mounted filesystem to generate structured metadata and 3 high-resolution sample thumbnails per video:

```python
def extract_video_telemetry(filepath: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_name,codec_type,width,height:format=duration,size",
        "-of", "json", str(filepath)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(res.stdout)
    v_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    
    width = v_stream.get("width")
    height = v_stream.get("height")
    duration = float(data.get("format", {}).get("duration", 0.0))
    
    return {
        "filename": filepath.name,
        "width": width,
        "height": height,
        "aspect_ratio": "9:16 (vertical)" if width and height and (width < height) else "16:9 (horizontal)",
        "duration_sec": round(duration, 2),
        "is_short_ready": bool(width and height and (width < height) and (duration <= 60.0))
    }

def slice_thumbnails(filepath: Path, duration: float, out_dir: Path) -> list:
    timestamps = [duration * 0.15, duration * 0.50, duration * 0.85]
    saved = []
    for i, ts in enumerate(timestamps, 1):
        thumb_name = f"{filepath.stem}_thumb_{i:02d}.jpg"
        target = out_dir / thumb_name
        subprocess.run(["ffmpeg", "-y", "-ss", str(ts), "-i", str(filepath), "-vframes", "1", "-q:v", "2", str(target)])
        if target.exists():
            saved.append(thumb_name)
    return saved
```

### 3. Local Workspace Ingestion Helper (`scripts/sync_drive_metadata.sh`)

Once Colab writes the JSON packages and thumbnails to `00_INBOX/01_RAW/20261028/metadata/`, pull only the lightweight metadata chunks down to the local PRoot/Termux workspace:

```bash
#!/usr/bin/env bash
set -euo pipefail

REMOTE_PATH="turbo:00_INBOX/01_RAW/20261028/metadata/"
TARGET_DIR="./metadata/20261028"

mkdir -p "${TARGET_DIR}"

# Downloads ~1.5 MB total (JSON + JPGs) instead of 2.21 GB of raw video
rclone sync "${REMOTE_PATH}" "${TARGET_DIR}" --progress --verbose
```

## Takeaways

- **Decoupled Architecture**: High-bandwidth compute (video decoding, keyframe slicing, transcoding) belongs in cloud runtimes; low-bandwidth control logic (assembly instructions, naming schemas, publish queues) belongs on local edge terminals.
- **Zero Raw Downloads**: The local device never downloads multi-gigabyte raw assets; it consumes structured JSON packages and lightweight JPG contact sheets.
- **Ephemeral Tooling**: Host `.ipynb` files in the cloud remote directory so they are always adjacent to the dataset they operate on and can be launched directly from Google Drive.
