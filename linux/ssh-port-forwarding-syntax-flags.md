# SSH Port Forwarding Syntax & Tunneling Flags

Mastering OpenSSH forwarding flags (`-L`, `-R`, `-D`) and operational switches (`-N`, `-f`, `-p`, `-C`) to bend network traffic across isolated boundaries.

## Context

When navigating between subnets or remote environments (such as a workstation and a Termux node), standard incoming connections may be blocked or require pivoting. Understanding flag directionality and background lifecycle switches prevents broken sessions and accidental shell spawning.

## Flag Taxonomy & Syntax Reference

### 1. Directional Tunnels (`-L`, `-R`, `-D`)

| Flag | Name | Syntax | Traffic Flow & Behavior |
| :--- | :--- | :--- | :--- |
| **`-L`** | **Local Forward** | `-L [bind_ip:]local_port:dest_host:dest_port` | **Client $\rightarrow$ Server $\rightarrow$ Target**.<br>Opens `local_port` on your machine; traffic is funneled through the SSH server to `dest_host:dest_port`. |
| **`-R`** | **Remote / Reverse** | `-R [bind_ip:]remote_port:dest_host:dest_port` | **Server $\rightarrow$ Client $\rightarrow$ Target**.<br>Opens `remote_port` on the SSH server; traffic is channeled back through the client to reach `dest_host:dest_port`. |
| **`-D`** | **Dynamic SOCKS** | `-D [bind_ip:]local_port` | **Application-Level Proxy**.<br>Turns the SSH client into a local SOCKS4/SOCKS5 proxy, routing dynamic socket connections via the SSH server. |

### 2. Operational & Execution Modifiers

| Flag | Meaning | Imperial Purpose |
| :--- | :--- | :--- |
| **`-N`** | **No Command** | Prevents execution of remote commands or interactive shells. Mandatory for purely forwarding ports. |
| **`-f`** | **Background Fork** | Directs SSH to fork into background immediately before command execution (requires auth credentials / keys). |
| **`-T`** | **Disable TTY** | Suppresses pseudo-terminal allocation to save system pty/pts allocation. |
| **`-p <port>`** | **Port Select** | Specifies target SSH server port (e.g., `8022` on Android/Termux). |
| **`-C`** | **Compression** | Enables gzip compression on the data stream (useful over high-latency WAN). |
| **`-v` / `-vvv`** | **Verbose Audit** | Outputs full debug logs to diagnose failed bindings or rejected forwards. |

---

## Implementation / Code

### Local Port Forwarding (`-L`)
Access a database or web server running inside the remote host from your local workstation:

```bash
# Listen on local 8080 -> deliver to remote server's localhost:8080
ssh -N -f -p 8022 -L 8080:localhost:8080 u0_a444@192.168.0.126
```

### Remote / Reverse Port Forwarding (`-R`)
Expose a local service on your workstation back into the remote server:

```bash
# Listen on remote 9000 -> channel back to workstation localhost:3000
ssh -N -f -p 8022 -R 9000:localhost:3000 u0_a444@192.168.0.126
```

### Dynamic SOCKS5 Proxy (`-D`)
Route browser or CLI traffic dynamically through the remote network:

```bash
# Bind SOCKS5 listener on local port 1080
ssh -N -f -p 8022 -D 1080 u0_a444@192.168.0.126

# Execute requests through the established conduit
curl --socks5-hostname localhost:1080 https://api.ipify.org
```

### On-The-Fly Tunneling (SSH Escape Characters)
Inject forwards into an existing active terminal session without disconnecting:

```text
1. Press <Enter>
2. Type: ~C
3. At the ssh> prompt:
   ssh> -R 8080:localhost:8080
   ssh> -L 3000:localhost:3000
   ssh> -D 1080
   ssh> -KL 3000   (cancel forward)
```

---

## Takeaways

- **Direction Anchor**: `-L` opens the listening port on the **Local** machine; `-R` opens the listening port on the **Remote** machine.
- **Port Only Guard**: Always combine `-N` and `-f` when establishing headless background tunnels to prevent dangling interactive shells.
- **Strict Binding**: By default, forwarded ports bind to `127.0.0.1`. To bind all interfaces, prefix with `0.0.0.0:` and ensure `GatewayPorts yes` is permitted in `sshd_config`.
- **Fail Fast**: Add `-o ExitOnForwardFailure=yes` in automation scripts to ensure the SSH command exits with an error code if the port is already occupied.
