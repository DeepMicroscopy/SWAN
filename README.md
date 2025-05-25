# SWAN

## Verifying commits

```sh
# configure allowed signers
git config gpg.ssh.allowedSignersFile known_signers

# view signatures for commits
git log --show-signature
```