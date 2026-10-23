# Zero-Download Remote Auditing and Safe Deduplication with Rclone

Audit divergence and deduplicate multi-terabyte cloud remotes without downloading file payloads over mobile bandwidth.

## Context

Managing disparate cloud remotes (e.g. OneDrive, Google Drive, Wasabi S3) often results in duplicate archives and redundant trees. Downloading files locally to verify MD5/SHA256 checksums exhausts local storage and bandwidth quotas.

## Implementation / Code

```bash
# Compare file checksums and directory trees between two remotes without downloading
rclone check remote_source: remote_dest: --one-way

# Find and resolve exact duplicates directly on the remote
rclone dedupe --dedupe-mode newest remote:path/to/directory

# Audit file deletions with dry-run before touching live buckets
rclone delete remote:path/to/purge --dry-run

# Size comparison report without fetching contents
rclone size remote:path/to/bucket
```

## Takeaways

- `rclone check` verifies cryptographic hashes in-cloud using object storage metadata.
- Never execute destructive commands (`delete`, `sync`, `purge`) on remotes without first executing `--dry-run`.
- `--dedupe-mode newest` automatically resolves collisions by retaining the most recently updated object.
