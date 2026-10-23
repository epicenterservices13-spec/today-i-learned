# Termux Extra Keys Layout Restoration and Instant Reload

Restore essential navigation keys (ESC, TAB, CTRL, ALT, cursor keys) on Android mobile touch keyboards without interrupting running processes.

## Context

Android virtual keyboards lack essential POSIX terminal keys. If the Termux properties configuration is missing or corrupted, terminal control characters cannot be typed easily. Restarting the app kills active sessions and subshells.

## Implementation / Code

```bash
# Define standard extra-keys layout in ~/.termux/termux.properties
mkdir -p ~/.termux

cat << 'EOF' > ~/.termux/termux.properties
extra-keys = [ \
  ['ESC', 'TAB', 'CTRL', 'ALT', 'UP', 'DOWN'], \
  ['/', '-', 'HOME', 'END', 'PGUP', 'PGDN'] \
]
EOF

# Reload configurations immediately into the running Android interface:
termux-reload-settings
```

## Takeaways

- `termux-reload-settings` re-reads `~/.termux/termux.properties` in real time without killing running jobs or tmux panes.
- Keep canonical configuration backed up in `55_INFRA/dotfiles/` to prevent loss across device resets.
