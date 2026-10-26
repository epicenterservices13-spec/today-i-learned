# 4K HEVC Video Scaling with Lanczos and Unsharp Filtering

Executing high-quality video scaling on low-power ARM64 CPUs using FFmpeg Lanczos resampling and sharpening filters.

## Context

Neural super-resolution models (Real-ESRGAN) require substantial GPU compute and run slowly on low-power devices. For batch video preparation and baseline upscaling, mathematical filtering (Lanczos) combined with unsharp masking produces clean high-definition output without overwhelming the mobile CPU or requiring cloud offload.

## Implementation / Code

```bash
# 4K UHD 10-bit HEVC Upscale with Lanczos algorithm
ffmpeg -i input.mp4 \
  -vf "scale=3840:2160:flags=lanczos,unsharp=5:5:0.8:5:5:0.0" \
  -c:v libx265 -crf 18 -preset medium -pix_fmt yuv420p10le \
  -c:a copy output_4k.mp4

# High-Quality 1080p Profile with Bicubic fallback
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080:flags=lanczos" \
  -c:v libx264 -crf 20 -preset fast \
  -c:a aac -b:a 192k output_1080p.mp4
```

## Takeaways

- `flags=lanczos` preserves edge clarity significantly better than default bilinear interpolation.
- The `unsharp` filter counteracts blurring introduced during resolution expansion.
- `yuv420p10le` mitigates color banding in high-resolution gradients.
