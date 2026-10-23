# Direct Google Drive Metadata Inspection via Rclone Backend Query

`rclone backend query` executes raw API queries directly against Google Drive search endpoints, allowing instantaneous retrieval of file IDs, parent folder hierarchies, and MIME types without directory traversal overhead.

## Context

During cloud auditing of massive remotes (`epic:` and `epicdev:`), standard recursive listings (`rclone lsf`, `rclone lsjson`) were too slow when searching for specific file duplicates or mapping parent IDs across millions of objects. Querying Google Drive's native search API directly bypassed path resolution bottlenecks.

## Implementation / Code

```bash
# Query files by exact name across all folders on remote
rclone backend query epic: "name = 'target_payload.jpg'"

# Inspect child folders of a known parent folder ID
rclone backend query epic: "'0AAUGVdxZlWBtUk9PVA' in parents and mimeType = 'application/vnd.google-apps.folder'"

# Inspect specific file/folder metadata, capabilities, and parents by ID
rclone backend query epic: "id = '1Sna8ycctRjDlB8uBH_gQY6pZogpiUL0o'"
```

## Takeaways

- `rclone backend query` speaks directly to the remote provider's native backend API, bypassing filesystem abstractions.
- Ideal for debugging orphan folders, circular structures, or locating file instances regardless of where they sit in directory hierarchies.
- Output is emitted as structured JSON conforming to the provider's API representation.
