# Google Drive Shared Drive Permission Barriers and Authoritative Owner Routing

Deletion requests against Google Drive shared folders fail with `403 Forbidden` if the authenticated OAuth identity lacks file ownership; destructive purge operations must target the authoritative owner remote.

## Context

Attempting to delete duplicate targets from `epic:80_ARCHIVE/99_TOMB/` yielded repeated `googleapi: Error 403: The user does not have sufficient permissions for this file` errors. Although the files were accessible through `epic:`, they were owned by the account configured under `epicdev:`. Purges had to be re-routed through the authoritative owner.

## Implementation / Code

```bash
# FAILS: Deleting shared files via delegated client remote (403 Forbidden)
rclone delete epic:80_ARCHIVE/99_TOMB/ --files-from targets.txt
# Log: ERROR : Couldn't delete: googleapi: Error 403: The user does not have sufficient permissions...

# FIX: Target the authoritative owner remote where full write/delete permissions reside
# Step 1: Dry-run verification against owner remote
rclone delete epicdev:00_INBOX/RECOVERED_ORPHANS/ \
    --files-from /data/data/com.termux/files/home/50_OPS/55_LOGS/targets.txt \
    --dry-run -v

# Step 2: Live execution with execution audit logging
rclone delete epicdev:00_INBOX/RECOVERED_ORPHANS/ \
    --files-from /data/data/com.termux/files/home/50_OPS/55_LOGS/targets.txt \
    --log-file=/data/data/com.termux/files/home/50_OPS/55_LOGS/purge_execution.log
```

## Takeaways

- Read access to a Google Drive shared item does not confer deletion rights under Google API policies.
- Always determine object ownership (`rclone backend userinfo <remote>:` or `rclone about <remote>:`) before automating mass deletion pipelines.
- Stage purge lists into dedicated text manifests and execute strictly with `--files-from` to avoid accidental directory wipes.
