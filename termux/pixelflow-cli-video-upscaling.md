# AI Video Upscaling with PixelFlow CLI and Real-ESRGAN in PRoot Ubuntu

Provisioning and deploying `pixelflow-cli` via `uv` in PRoot Ubuntu for 2× Real-ESRGAN frame upscaling and RIFE interpolation on Termux.

## Context

Video enhancement and super-resolution require deep neural reconstruction (Real-ESRGAN) coordinated with FFmpeg for audio/video stream demuxing, frame extraction, and re-encoding. 

Running AI upscaling pipelines directly on Android/Termux faces library dependencies and wheel availability issues. Hosting the pipeline inside a PRoot Ubuntu container (`proot-distro login ubuntu`) provides a full glibc runtime where `uv` manages the `pixelflow-cli` tool environment and ncnn Vulkan backends.

## Implementation / Code

### 1. Provision PixelFlow in PRoot Ubuntu Container
```bash
# Enter Ubuntu PRoot and install via uv tool
proot-distro login ubuntu -- bash -c "export PATH=\$PATH:/root/.local/bin; uv tool install pixelflow-cli"

# Provision FFmpeg, Real-ESRGAN, and RIFE models (411MB bundle)
proot-distro login ubuntu -- bash -c "export PATH=\$PATH:/root/.local/bin; pixelflow init"
```

### 2. Path Resolution & Health Verification (`doctor`)
PixelFlow extracts the ncnn executables into nested directories. Symlink them into the application binary directory so the resolver registers them:
```bash
proot-distro login ubuntu -- bash -c "
  ln -sf /root/.local/share/pixelflow/bin/realesrgan/realesrgan-ncnn-vulkan /root/.local/share/pixelflow/bin/realesrgan-ncnn-vulkan
  ln -sf /root/.local/share/pixelflow/bin/rife/rife-ncnn-vulkan-20221029-ubuntu/rife-ncnn-vulkan /root/.local/share/pixelflow/bin/rife-ncnn-vulkan
  pixelflow doctor
"
```

Verified Doctor Output:
```text
FFmpeg          OK  /root/.local/share/pixelflow/bin/ffmpeg
FFprobe         OK  /data/data/com.termux/files/usr/bin/ffprobe
Real-ESRGAN     OK  /root/.local/share/pixelflow/bin/realesrgan-ncnn-vulkan
RIFE            OK  /root/.local/share/pixelflow/bin/rife-ncnn-vulkan
Backend         OK  ncnn
Platform        OK  Linux arm64
Temp directory  OK  /root/.local/share/pixelflow/cache
```

### 3. Upscale Video with Conservative Factor (2×)
```bash
proot-distro login ubuntu -- bash -c "
  pixelflow upscale-video turtle.mp4 -o turtle_upscaled.mp4 --scale 2
"
```

### 4. Host Wrapper for Native Invocation from Termux Host
Expose `pixelflow` directly to `$PATH` (`~/.local/bin/pixelflow`):
```bash
cat << 'EOF' > ~/.local/bin/pixelflow
#!/usr/bin/env bash
exec proot-distro login ubuntu -- bash -c "export PATH=\$PATH:/root/.local/bin; pixelflow \"\$@\""
EOF
chmod +x ~/.local/bin/pixelflow
```

## Takeaways

- **Organic Detail Protection**: Limit initial video upscaling to **2×** rather than 4×. Real-ESRGAN generates plausible texture approximations; aggressive 4× passes invent synthetic artifacts on turtle shells, reptilian scales, and fluid water surfaces.
- **Pipeline Segregation**: Use FFmpeg first for lossless audio demuxing and geometric rotational alignment before feeding clean frame sequences to the upscaler.
