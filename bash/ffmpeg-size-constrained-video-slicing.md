# FFmpeg Dynamic Bitrate Math and Stream-Copy Video Slicing for Size Constraints

Calculating safe chunk durations and managing stream-copy vs re-encode fallback to guarantee video segments strictly under a target byte limit (100MB).

## Context

Cloud storage remotes, messaging platforms, and automated ingestion APIs frequently enforce rigid file upload ceilings (e.g. 100MB or 25MB). When splitting raw multi-gigabyte camera footage, naive time-based segmenting (e.g. static 30-second cuts) fails because variable bitrate (VBR) video spikes during high-motion scenes, resulting in oversized chunks that fail downstream uploads.

Additionally, operators new to film and video pipelines frequently encounter industry terminology like the **"Martini Shot"**—the final take or sequence captured before wrapping production for the day. In automated storage operations, the Martini phase represents the final wrap-up step: verifying slices, offloading the raw archival masters to cold cloud remotes, and purging scratch storage.

## Implementation / Code

### 1. The Electrical Wire Gauge Analogy: Bitrate vs File Size
Video data math follows the exact principles of electrical power consumption:
* **Resolution (1080p, 4K)** is like conduit dimensions.
* **Bitrate (kbps)** is current / amperage flowing through the conductor.
* **Duration (seconds)** is time active.
* **File Size** is total Watt-hours / energy delivered:

$$\text{Target Duration (seconds)} = \frac{\text{Target Bytes} \times 8}{\text{Bitrate (bits/sec)} \times \text{Safety Margin (1.15)}}$$

### 2. Slicing with Fast Stream Copy (`-c copy`)
If video codecs are already compatible, split at keyframe (I-frame) boundaries without re-encoding quality loss:

```bash
# Calculate safe segment time (e.g. 75 seconds for a 10 Mbps file to stay under 95MB)
SEGMENT_TIME=75

ffmpeg -hide_banner -loglevel error -y -i input_raw.mp4 \
    -c copy \
    -map 0 \
    -segment_time "$SEGMENT_TIME" \
    -f segment \
    -reset_timestamps 1 \
    "segments/part_%03d.mp4"
```

### 3. Re-encode Fallback with Hard Bitrate Cap
If keyframe spacing is sparse or stream copy produces an oversized chunk, enforce a hard bit ceiling:

```bash
# Target: 95 MB over 60 seconds -> 12,666 kbps ceiling
TARGET_BITRATE="12000k"

ffmpeg -hide_banner -loglevel error -y -i input_raw.mp4 \
    -c:v libx264 -b:v "$TARGET_BITRATE" -maxrate "$TARGET_BITRATE" -bufsize "24000k" \
    -c:a aac -b:a 128k \
    -segment_time 60 \
    -f segment \
    -reset_timestamps 1 \
    "segments/part_%03d.mp4"
```

### 4. The Martini Shot Wrap-Up
After all slices are generated and verified locally, execute the "Martini Step":

```bash
# Checksum-verified offload of original raw to cloud remote
rclone copy --checksum --check-first input_raw.mp4 turbo:20_MEDIA/26_ASSETS/raw_archive/

# Only delete local raw master once remote checksum matches
if [ $? -eq 0 ]; then
    rm -f input_raw.mp4
    echo "[MARTINI SHOT COMPLETE] Raw master offloaded. Local disk freed."
fi
```

## Takeaways

- **Safety Headroom**: For a 100MB ceiling, always target 95MB (99,614,720 bytes) to absorb container format (MP4/MKV) muxing overhead and variable audio bitrates.
- **Keyframe Alignment**: Stream copy (`-c copy`) can only cut at I-frames; if segments overshoot the time boundary by 2–3 seconds, dynamic duration sizing with a 15% safety factor prevents exceeding the byte limit.
- **Data Integrity Over Speed**: Never delete local master footage on a simple exit code 0; always pass `--checksum` to `rclone` so the remote calculates hash parity before local truncation.
