# Hardware Interfacing via Termux:API

Control Android hardware components, query telemetry, and trigger system notifications directly from the Termux shell.

## Context

Android sandboxes POSIX environments, preventing shell scripts from natively interacting with platform hardware (vibrator, camera, battery, clipboard, notifications). Termux:API establishes an IPC bridge between the shell and Android system services.

## Implementation / Code

```bash
# 1. Install companion app via F-Droid / GitHub APK, then install CLI package
pkg update -y && pkg install -y termux-api

# 2. System notifications and on-screen alerts
termux-notification --title "Alert" --content "Deployment complete."
termux-toast -b black -c red "Process finished"

# 3. Battery telemetry inspection (JSON output)
termux-battery-status

# 4. Haptic vibration (500 ms)
termux-vibrate -d 500

# 5. Clipboard synchronization
echo "Transferred content" | termux-clipboard-set
termux-clipboard-get

# 6. LED Torch control
termux-torch on
termux-torch off
```

## Takeaways

- Termux:API requires both the Android APK (`Termux:API`) and the command-line package (`termux-api`) with matching signature keys.
- Output from commands like `termux-battery-status` and `termux-location` prints valid JSON, making it ideal for downstream processing with `jq`.
- Permissions (Camera, Location, Storage) must be granted to the Termux:API app inside Android App Settings.
