# Ad-Hoc Socket Beaming of SSH Public Keys Between Mobile Nodes

Bypass the friction of manually typing base64 Ed25519 public keys on touchscreens by streaming keys directly across the local LAN with an ephemeral socket listener.

## Context

Manual entry of cryptographic keys on on-screen mobile keyboards is error-prone due to indistinguishable glyphs (`I` uppercase eye vs `l` lowercase el vs `1` number one). When establishing trust between two fresh Android/Termux nodes without shared clipboard sync or cloud intermediaries, traditional copy-paste fails.

Attempting to read base64 strings character-by-character leads to authentication rejection and lockouts.

## Implementation / Code

### Receiver Node (Phone)
Spin up an ephemeral single-connection socket listener on an unprivileged port (e.g. `7777`) that appends the incoming payload directly to `~/.ssh/authorized_keys`:

```python
import socket, os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 7777))
s.listen(1)

conn, _ = s.accept()
key = conn.recv(4096).decode('utf-8').strip()
conn.close()
s.close()

if key.startswith("ssh-"):
    with open(os.path.expanduser("~/.ssh/authorized_keys"), "a") as f:
        f.write("\n" + key + "\n")
    os.chmod(os.path.expanduser("~/.ssh/authorized_keys"), 0o600)
```

### Sender Node (Tablet)
Pipe the public key directly over TCP to the receiver's LAN IP:

```bash
cat ~/.ssh/id_ed25519.pub | nc 192.168.0.126 7777
```

Immediately test the authenticated connection:
```bash
ssh -p 8022 u0_a444@192.168.0.126
```

## Takeaways

- Eliminates manual transcription errors of base64 glyphs (`I`, `l`, `1`, `O`, `0`).
- Keeps the key transmission contained entirely within the local layer-2 Wi-Fi broadcast domain.
- Once transmitted, the trust is permanent: `ssh-guard` and `sshd` validate the key file permissions (`0600`) without future interaction.
