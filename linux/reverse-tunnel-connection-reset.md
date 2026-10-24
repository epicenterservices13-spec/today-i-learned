# Diagnosing SSH Reverse Tunnel Connection Resets (kex_exchange_identification)

Differentiating between an active SSH reverse tunnel socket and an unattached client target when diagnosing `kex_exchange_identification: read: Connection reset by peer`.

## Context

When establishing reverse tunnels (`ssh -R <remote_port>:localhost:<target_port>`), the listening socket opens on the SSH server immediately. However, client connections to `127.0.0.1:<remote_port>` fail with an instant handshake termination:

```text
debug1: Connecting to 127.0.0.1 [127.0.0.1] port 2222.
debug1: Connection established.
debug1: Local version string SSH-2.0-OpenSSH_10.6
kex_exchange_identification: read: Connection reset by peer
Connection reset by 127.0.0.1 port 2222
```

This occurs because OpenSSH allocates the remote tunnel port on the server upon negotiation, but only attempts to dial `localhost:<target_port>` on the client machine when traffic actually arrives. If no daemon is listening on `<target_port>` on the client (e.g., failed `systemctl` in a container, missing host keys, or non-root permission denied binding port 22), the client resets the TCP channel.

## Implementation / Code

### 1. Identify the False Positive on Server
The remote port responds to `nc` probe even when the client target service is dead:

```bash
# This reports OPEN because the tunnel ingress is listening:
nc -zvw 1 127.0.0.1 2222
# Output: Ncat: Connected to 127.0.0.1:2222.
```

### 2. Diagnose Channel Reset with Verbose Tracing
Run client SSH connection with `-v` to confirm failure at key exchange (`kex_exchange_identification`):

```bash
ssh -v -p 2222 127.0.0.1
```

### 3. Verify Target Service on Client Node
On the machine initiating the reverse tunnel, verify that the daemon is actually bound locally:

```bash
# Check if target port (e.g. 22 or 2022) is listening locally
ss -tulpn | grep -E "22|2022" || netstat -tlpn | grep -E "22|2022"

# In containers (PRoot, chroot, Docker) without systemd init:
# 1. Generate missing host keys
sudo ssh-keygen -A 2>/dev/null || true

# 2. Avoid privileged port 22 conflicts; bind unprivileged port 2022
/usr/sbin/sshd -p 2022

# 3. Establish reverse tunnel pointing to active port 2022
ssh -p 8022 -N -f -R 2222:localhost:2022 user@remote-host
```

## Takeaways

- **Delayed Target Resolution**: An open `-R` port on the server does NOT guarantee the target service on the client is reachable. OpenSSH dials the target lazily upon incoming connection.
- **Rootless Port Binding**: In non-root environments (Termux, PRoot, unprivileged Linux namespaces), daemons cannot bind ports below 1024 (e.g. port 22). Always route through high unprivileged ports (e.g. 2022, 8022).
- **Init Failures in Containers**: `systemctl` / `service` fails silently in PRoot without PID 1 init. Directly invoke binaries (e.g. `/usr/sbin/sshd`) or verify with `ps aux`.
