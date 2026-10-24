# Physical Keyboard Navigation in Termux and Byobu

Orchestrate Termux and Byobu multiplexer sessions rapidly using physical keyboard shortcuts on tablet devices.

## Context

When operating on an Android tablet with an external physical keyboard, virtual keyboard popups waste viewport real estate. Relying on touchscreen swipes to manage terminal sessions or split panes degrades operational velocity.

## Implementation / Code

```text
# Termux Core Native Shortcuts
Ctrl + Alt + N        : Allocate and open a new pseudo-terminal session
Ctrl + Alt + Down/Right: Switch viewport to next active session
Ctrl + Alt + Up/Left  : Switch viewport to previous active session
Ctrl + Alt + D        : Toggle navigation drawer
Ctrl + Alt + K        : Force hide or show soft keyboard

# Byobu Multiplexer Shortcuts (F-Key Driven)
F2                    : Create a new window in active session
F3 / F4               : Move focus to previous / next window
Shift + F2            : Split active pane horizontally
Ctrl + F2             : Split active pane vertically
Shift + F3 / F4       : Move focus to previous / next pane
F6                    : Detach from session cleanly
```

## Takeaways

- Physical keyboard shortcuts bypass the need for touchscreen navigation drawer gestures.
- Combining Termux native sessions (`Ctrl + Alt + N`) with Byobu/tmux multiplexing (`F2`-`F4`) yields isolated multi-tasking workspaces.
- Check hardware keyboard layout mapping in Android system settings if `Alt` acts as `Meta` or triggers system apps.
