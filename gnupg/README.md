# GnuPG Configuration

This package manages GnuPG configuration files (gpg.conf, gpg-agent.conf, and scdaemon.conf).

<!--- Tree block injection -->
    └── .gnupg
        ├── gpg-agent.conf 	# configuration for gpg-agent
        ├── gpg.conf 	# GnuPG configuration options
        └── scdaemon.conf 	# configuration for smartcard daemon

## Requirements

- `gnupg`
- `pinentry` (e.g., `pinentry-gnome3` on Linux)
