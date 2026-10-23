# Terminal Multiplexer Session Persistence and Dual-Pane Monitoring on Android

Running intensive CLI commands within a detached `tmux` session prevents mobile process terminations on SSH disconnects and provides dual-pane inspection for concurrent command execution and log tailing.

## Context

When administering long-running cloud transfers or deduplication scripts on Android Termux over SSH, network interruptions or Android OS background process killer routines kill raw terminal sessions, terminating running processes. Wrapping operations in `tmux` guarantees continuous background execution and multiplexed views.

## Implementation / Code

```bash
# 1. Spawn or attach to a persistent named session
tmux new-session -A -s imperial-ops

# 2. Window splitting keybindings (Default Prefix: Ctrl+b)
# Prefix + % : Split window vertically (side-by-side)
# Prefix + " : Split window horizontally (stacked)
# Prefix + o : Cycle focus between active panes
# Prefix + [ : Enter copy/scrollback navigation mode (q to exit)

# 3. Multiplexed workflow pattern:
# Left Pane: Run live migration / deduplication
rclone sync onedrive:80_ARCHIVE epic:80_ARCHIVE -P

# Right Pane: Monitor system audit log concurrently
tail -f ~/50_OPS/55_LOGS/file_moves.csv

# 4. Detach session without killing operations
# Prefix + d

# 5. Reconnect after terminal or network drop
tmux attach -t imperial-ops
```

## Takeaways

- Never execute long-running transfers or mutations in bare mobile SSH sessions; unexpected disconnections send SIGHUP to all child processes.
- Detached `tmux` sessions remain alive under Termux background services until manually terminated.
- Multiplexing panes eliminates context switching between execution and log verification.
