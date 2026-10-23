# Cross-Provider Transfer Limits and Host Proxy Streaming in Rclone

`rclone` server-side transfers only function when both source and destination share the same underlying provider infrastructure; cross-provider migrations stream full payloads through client host memory and network.

## Context

Transferring gigabytes between differing cloud providers (e.g., Microsoft OneDrive to Google Drive) cannot execute server-side even with `--drive-server-side-across-configs`. Attempting this without understanding client streaming risks saturating mobile network connections, triggering memory pressure, and hitting Microsoft Graph API rate limits.

## Implementation / Code

```bash
# Intra-provider (Google Drive to Google Drive): Server-side execution
# Zero host bandwidth consumed; Google handles transfer internally
rclone copy epic:source epicdev:dest --drive-server-side-across-configs -P

# Cross-provider (OneDrive to Google Drive): Client streams packets
# Enforce --fast-list to avoid Microsoft Graph API request throttling
rclone sync onedrive:80_ARCHIVE epic:80_ARCHIVE \
    --fast-list \
    --transfers=4 \
    --checkers=8 \
    -P
```

## Takeaways

- Server-side copy is impossible across differing cloud storage APIs (e.g., Microsoft Graph vs Google Drive API); client acts as a network proxy.
- For high-volume cross-provider data transfers, execute within a headless cloud virtual machine (e.g., Google Colab or cloud PRoot instance) to exploit gigabit backbones and avoid mobile bandwidth consumption.
- Use `--fast-list` when querying large directory structures on OneDrive to retrieve whole folder trees in bulk memory calls rather than individual recursive HTTP requests.
