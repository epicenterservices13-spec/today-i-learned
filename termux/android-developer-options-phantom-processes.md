# Android Developer Options and Phantom Process Mitigation

Configure Android Developer Options to unlock local ADB pairing and prevent Android from killing Termux background child processes.

## Context

Beginning in Android 12, the system kernel and OS runtime enforce a strict 32-process limit across all child processes spawned by an application (the Phantom Process Killer). Compiling code, running Python scripts, or managing background daemons triggers automatic SIGKILL terminations unless properly configured.

## Implementation / Code

```text
# Step 1: Unlock Developer Privileges
Navigate to: Settings -> About Tablet -> Tap "Build Number" 7 times consecutively.

# Step 2: Critical Settings Adjustments
- Disable Child Process Restrictions:
  Toggled ON inside Developer Options (available on Android 12L/13+).
  Stops phantomprocesskiller from terminating multi-threaded background commands.

- Wireless Debugging:
  Enables ADB daemon over Wi-Fi without a physical host computer.
```

```bash
# Step 3: Local Wireless ADB Pairing inside Termux
pkg install -y android-tools

# Pair using port and code from Wireless Debugging dialog
adb pair localhost:<port> <pairing_code>

# Connect to the active ADB service
adb connect localhost:<port>

# Alternative: Suppress phantom process limits via ADB shell (Android 12/13)
adb shell "/system/bin/device_config put activity_manager max_phantom_processes 2147483647"
adb shell "/system/bin/device_config set_sync_disabled_for_tests persistent"
```

## Takeaways

- Android 12+ kills background POSIX builds silently without throwing an error in Termux; phantom processes are the primary culprit.
- Modern Android builds (12L, 13, 14) feature "Disable child process restrictions" directly in Developer Options.
- Wireless Debugging paired locally provides direct access to ADB commands without needing a secondary machine.
