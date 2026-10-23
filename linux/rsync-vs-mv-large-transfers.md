# Rsync vs MV for Mass Transfers and Safe Migration

Use `rsync -aP --remove-source-files` instead of `mv` when transferring large batches across mount points to gain resume capability, verification, and prevent corruption upon interruption.

## Context

Running `mv` on massive directory trees (thousands or millions of files) across different partitions, cloud mounts, or network shares is an all-or-nothing risk. If interrupted midway (network drop, killed process, out-of-space), `mv` leaves partially transferred files with no record of completion, zero progress visibility, and no mechanism to resume without starting over.

## Implementation / Code

```bash
# Safe, verifiable migration with progress reporting and checkpoint resume
rsync -aP --remove-source-files /source/path/ /destination/path/

# Flags breakdown:
# -a: Archive mode (recurse, preserve permissions, timestamps, owner, symlinks)
# -P: Combines --progress (real-time transfer metrics) and --partial (keep partially transferred files to resume)
# --remove-source-files: Deletes each source file ONLY after the remote copy is successfully written and verified

# Always execute a dry-run test first:
rsync -aPn --remove-source-files /source/path/ /destination/path/
```

## Takeaways

- `mv` within the same filesystem is an instant metadata pointer update (inode rename); across mount points, `mv` becomes an unmonitored copy-then-delete operation.
- `rsync --remove-source-files` guarantees atomic safety: corrupted or interrupted files remain intact at the source until verified at the destination.
- Use `--dry-run` (`-n`) before executing transfers against critical directories.
