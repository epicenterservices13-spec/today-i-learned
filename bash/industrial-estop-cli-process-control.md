# Industrial Start-Stop and Emergency Stop (E-STOP) Architecture for CLI Process Groups

Mapping industrial 3-wire motor control and maintained emergency stop (E-STOP) mechanics to Unix process groups for accessible, fail-safe CLI daemon supervision.

## Context

In complex multi-process pipelines (e.g. background batch transcoders, video splitters, and cloud transfer daemons), standard process termination often leaves orphaned subprocesses (e.g., `ffmpeg` or `rclone` worker instances) spinning in the background, consuming CPU and I/O.

For operators requiring fast, unambiguous physical or visual accessibility, issuing fine-grained `kill <PID>` commands or finding child PIDs through `ps aux | grep` is high-friction and prone to error. Industrial motor control solves this with a **3-wire control circuit**:
1. **Start button**: Normally Open (NO) momentary switch that seals in a magnetic contactor coil.
2. **Stop / E-STOP button**: Normally Closed (NC) maintained mushroom-head switch wired in series before the coil. Striking it breaks the entire circuit instantly.

Applying this pattern to CLI supervision guarantees that a single, atomic command breaks the holding circuit and kills every worker process in the tree.

## Implementation / Code

### 1. Process Group Isolation on Start (`os.setsid`)
To prevent child processes from being detached into orphaned background tasks, spawn the root worker in its own session/process group:

```python
import os, subprocess, sys
from pathlib import Path

PID_FILE = Path.home() / ".worker.pid"

def start_station():
    # Spawns worker as leader of a new process group (PGID == PID)
    proc = subprocess.Popen(
        [sys.executable, "worker.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )
    PID_FILE.write_text(str(proc.pid))
    print(f"[START] Circuit closed. Motor running on PID {proc.pid}")
```

### 2. Maintained Master E-STOP (`os.killpg`)
Striking the E-STOP halts the entire process group with a two-stage signal:

```python
import os, signal, time
from pathlib import Path

PID_FILE = Path.home() / ".worker.pid"

def estop_station():
    if not PID_FILE.exists():
        print("[CIRCUIT OPEN] System already halted.")
        return

    pid = int(PID_FILE.read_text().strip())
    pgid = os.getpgid(pid)
    print(f"[E-STOP STRUCK] De-energizing process group {pgid}...")

    # Stage 1: Graceful SIGTERM
    try:
        os.killpg(pgid, signal.SIGTERM)
        time.sleep(1)
        # Stage 2: Hard break SIGKILL
        os.killpg(pgid, signal.SIGKILL)
    except OSError:
        pass
    finally:
        PID_FILE.unlink(missing_ok=True)
        print("[CONFIRMED] All contactors opened. Total shutdown.")
```

### 3. Bash Instant Emergency Alias
Create a tactile terminal alias that operates identically to a physical emergency button:

```bash
alias estop='turbo-ops kill && pkill -9 -f ffmpeg && pkill -9 -f rclone'
```

## Takeaways

- **Process Groups (`setsid`)**: Never launch background pipelines without `os.setsid` or `set -m` in shell scripts; otherwise, child subprocesses remain parented to the init/subreaper when the top script exits.
- **Fail-Safe Holding Circuit**: Deleting or missing the PID lockfile acts like a broken holding contact, causing running loops to abort immediately on their next cycle.
- **Visual Accessibility**: Status outputs must use binary, high-contrast states (`[RUNNING]` vs `[STOPPED / E-STOP ENGAGED]`) rather than dense multi-column tabular logs.
