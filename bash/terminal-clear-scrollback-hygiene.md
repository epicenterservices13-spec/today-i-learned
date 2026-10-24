# Terminal Screen Erasure & Buffer Hygiene (`clear`)

**Date**: 2026-10-24  
**Category**: `bash`  
**Tags**: `terminal`, `clear`, `tmux`, `ansi`, `security`

---

## Overview

The standard `clear` command (or `Ctrl+L`) only shifts the current viewport below the previous output; scrollback buffers still retain all sensitive terminal history. True terminal hygiene requires purging the screen, scrollback buffer, and resetting damaged line disciplines.

## Core Techniques

### 1. Viewport vs Scrollback Purging

| Command | Action | Scrollback Preserved? |
| :--- | :--- | :--- |
| `clear` | Moves screen to blank viewport | Yes |
| `clear -x` | Clears without resetting scrollback capability | Yes |
| `printf '\033[2J\033[3J\033[H'` | Wipes viewport + purges scrollback buffer + homes cursor | **No (Annihilated)** |

### 2. Recovering from Garbled Output (Binary Cat)

When catting binary data corrupts terminal state:
```bash
# Reset terminfo state and terminal settings
reset

# Restore sane terminal line discipline
stty sane

# Fast terminfo reinitialization
tput reset
```

### 3. Multiplexer (Tmux) Scrollback Purge

```bash
# Clear tmux pane history buffer
tmux clear-history

# Comprehensive deep clean alias:
alias cclear='clear && printf "\033[3J" && tmux clear-history 2>/dev/null || true'
```
