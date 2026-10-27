# Today I Learned

> A collection of concise, battle-tested write-ups on commands, systems architecture, and engineering discipline.

**Total TILs documented:** `30`

---

## Categories

- [Architecture & Taxonomy](#arch) (`4`)
- [Bash & Shell Scripting](#bash) (`4`)
- [Git Discipline & Version Control](#git) (`2`)
- [Linux Administration & Storage](#linux) (`9`)
- [Python & Data Processing](#python) (`1`)
- [Termux & Android POSIX](#termux) (`10`)

---

<a id="arch"></a>
### Architecture & Taxonomy

- [Antigravity Agent Discovery and Custom Rule Precedence](arch/antigravity-agent-discovery-and-rule-hierarchy.md)
- [Zero Root Clutter via Johnny Decimal Governance](arch/johnny-decimal-root-governance.md)
- [Universal Johnny Decimal Taxonomy Across PRoot Containers](arch/proot-distro-taxonomy-synchronization.md)
- [TIL vs. Learning Journal Cognitive Taxonomy](arch/til-vs-learning-journal-taxonomy.md)

<a id="bash"></a>
### Bash & Shell Scripting

- [4K HEVC Video Scaling with Lanczos and Unsharp Filtering](bash/ffmpeg-lanczos-hevc-video-upscaling.md)
- [Fail-Fast Shell Scripts with set -euo pipefail](bash/safe-shell-pipelines.md)
- [Standard Stream Redirection and /dev/null Descriptor Mechanics](bash/stream-redirection-dev-null.md)
- [Terminal Screen Erasure & Buffer Hygiene (`clear`)](bash/terminal-clear-scrollback-hygiene.md)

<a id="git"></a>
### Git Discipline & Version Control

- [Single-File Atomic Commits in Git](git/atomic-commits-per-file.md)
- [GitHub CLI Multi-Account Token Management](git/gh-cli-multi-account-tokens.md)

<a id="linux"></a>
### Linux Administration & Storage

- [Atomic Audit Trail Logging for Filesystem Mutations](linux/atomic-audit-trail-logging.md)
- [Asymmetric Remote Compute via Google Colab Model Context Protocol](linux/colab-mcp-asymmetric-cloud-offload.md)
- [Direct Google Drive Metadata Inspection via Rclone Backend Query](linux/rclone-backend-query-api.md)
- [Zero-Download Remote Auditing and Safe Deduplication with Rclone](linux/rclone-cloud-remote-auditing.md)
- [Cross-Provider Transfer Limits and Host Proxy Streaming in Rclone](linux/rclone-cross-provider-transfer-limits.md)
- [Google Drive Shared Drive Permission Barriers and Authoritative Owner Routing](linux/rclone-permission-ownership-barriers.md)
- [Diagnosing SSH Reverse Tunnel Connection Resets (kex_exchange_identification)](linux/reverse-tunnel-connection-reset.md)
- [Rsync vs MV for Mass Transfers and Safe Migration](linux/rsync-vs-mv-large-transfers.md)
- [SSH Port Forwarding Syntax & Tunneling Flags](linux/ssh-port-forwarding-syntax-flags.md)

<a id="python"></a>
### Python & Data Processing

- [Cross-Remote Content Hashing and Offline Deduplication with Python](python/cross-remote-md5-deduplication.md)

<a id="termux"></a>
### Termux & Android POSIX

- [Android Developer Options and Phantom Process Mitigation](termux/android-developer-options-phantom-processes.md)
- [Android Root Privileges, Kernel Sovereignty, and Threat Vectors](termux/android-root-privileges-and-threat-vectors.md)
- [Portable Shebangs in Android Termux ARM64 Environments](termux/arm64-portable-shebangs.md)
- [Deploying OpenAI Codex CLI in PRoot Ubuntu Containers on Android](termux/codex-cli-in-proot-ubuntu.md)
- [Offline CPU Voice Synthesis with Pocket-TTS in PRoot ARM64](termux/offline-pocket-tts-synthesis.md)
- [AI Video Upscaling with PixelFlow CLI and Real-ESRGAN in PRoot Ubuntu](termux/pixelflow-cli-video-upscaling.md)
- [Hardware Interfacing via Termux:API](termux/termux-api-hardware-control.md)
- [Termux Extra Keys Layout Restoration and Instant Reload](termux/termux-extra-keys-configuration.md)
- [Physical Keyboard Navigation in Termux and Byobu](termux/termux-physical-keyboard-and-byobu-shortcuts.md)
- [Terminal Multiplexer Session Persistence and Dual-Pane Monitoring on Android](termux/tmux-session-persistence-splits.md)

---

## Adding a TIL

1. Copy [`template.md`](template.md) into the appropriate category folder:
   ```bash
   cp template.md bash/my-topic.md
   ```
2. Populate your notes following the structured sections.
3. Rebuild the index:
   ```bash
   python3 scripts/build_index.py
   ```
4. Enforce atomic commits:
   ```bash
   git add bash/my-topic.md && git commit -m "bash/my-topic.md: add notes on my topic"
   git add README.md && git commit -m "README.md: update index"
   ```

## License

MIT License. See [LICENSE](LICENSE).
