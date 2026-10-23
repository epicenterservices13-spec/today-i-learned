# Cross-Remote Content Hashing and Offline Deduplication with Python

When disparate cloud remotes do not mirror directory hierarchies, path matching fails; dumping checksum manifests via `rclone hashsum` and intersecting MD5 sets in Python identifies identical files across arbitrary folder trees.

## Context

Comparing two cloud remote trees (`epic.txt` and `epicdev.txt`) showed 0% path overlap due to differing organizational structures. Direct diffing was useless. By exporting MD5 checksums computed server-side by Google Drive and analyzing collisions in Python, 5,239 duplicate files were accurately located.

## Implementation / Code

```python
#!/usr/bin/env python3
"""Offline MD5 cross-remote collision detector."""
from collections import defaultdict
import sys

def parse_hash_dump(file_path: str) -> dict[str, list[str]]:
    hash_to_paths = defaultdict(list)
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                md5, rel_path = parts
                hash_to_paths[md5.lower()].append(rel_path)
    return hash_to_paths

# Step 1: Dump remote hashes without downloading files:
# $ rclone hashsum md5 epic: > epic.md5
# $ rclone hashsum md5 epicdev: > epicdev.md5

epic = parse_hash_dump("epic.md5")
epicdev = parse_hash_dump("epicdev.md5")

common_hashes = set(epic.keys()) & set(epicdev.keys())
print(f"Identified {len(common_hashes)} shared content hashes across distinct paths.")

# Step 2: Generate exact delete manifest for one remote
with open("epic_tomb_purge_targets.txt", "w", encoding="utf-8") as out:
    for h in common_hashes:
        for path in epic[h]:
            if "99_TOMB" in path:
                out.write(f"{path}\n")
```

## Takeaways

- Path comparison cannot detect duplicates across unaligned folder hierarchies; content hashes are the only reliable truth.
- `rclone hashsum md5 <remote>:` uses native Google Drive file checksums, incurring zero download payload costs.
- Decoupling identification into an offline manifest allows pre-purge verification and avoids live race conditions.
