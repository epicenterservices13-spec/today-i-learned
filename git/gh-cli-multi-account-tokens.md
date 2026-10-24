# GitHub CLI Multi-Account Token Management

Forge Personal Access Tokens (PATs) and switch active CLI identities across multiple GitHub accounts without credential collisions.

## Context

Operating across multiple GitHub accounts (e.g. personal vs organization) creates authentication collisions. GitHub does not allow re-viewing generated tokens, requiring deterministic generation, active session switching, and vault storage.

## Implementation / Code

```bash
# 1. Forge PAT at https://github.com/settings/tokens/new
# Scopes: repo, workflow, read:org, gist

# 2. Authenticate new account via browser/device code
gh auth login --hostname github.com -p https -w

# 3. Check authenticated accounts and toggle active session
gh auth status
gh auth switch --user <account_username>

# 4. Secure token in Imperial Vault
echo "GITHUB_TOKEN_<ACCOUNT>=ghp_..." >> ~/90_VAULT/92_CREDENTIALS/.env
chmod 600 ~/90_VAULT/92_CREDENTIALS/.env
```

## Takeaways

- Generated tokens are displayed once by GitHub; if misplaced, generate a replacement immediately.
- `gh auth switch` updates the active user context in `~/.config/gh/hosts.yml` without re-authenticating.
- Always isolate secrets in `~/90_VAULT/92_CREDENTIALS/` with `chmod 600` permissions.
