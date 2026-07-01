# F-dotfiles Agent Rules

This file outlines the rules, guidelines, and behavioral constraints for AI agents working in the **F-dotfiles** repository.

## Repository Overview

`F-dotfiles` is an opinionated, topical dotfiles organization scheme based on GNU `stow`. It organizes dotfiles into application-specific package directories at the repository root (e.g., `zsh/`, `git/`, `linux/`).

## Architectural Rules

### 1. Package Directory Structure & Stow Conventions
Every package folder (e.g., `git`, `zsh`) follows a specific layout. Files in these folders are symlinked to the user's home directory.
* **Base Package Files**: Place common configuration files directly in the package directory.
* **OS-Specific Overrides**: Place OS-specific overrides in a subdirectory named `@${OS}` (e.g., `@Linux`, `@Darwin`).
* **Host-Specific Overrides**: Place host-specific overrides in a subdirectory named `@${HOSTNAME}` (e.g., `@my-laptop`).
* **XDG Config Home (`~/.config`)**: Place files destined for `XDG_CONFIG_HOME` under `@config`.
  * OS-specific configs in `XDG_CONFIG_HOME` go under `@config/@${OS}`.
  * Host-specific configs in `XDG_CONFIG_HOME` go under `@config/@${HOSTNAME}`.

---

### 2. Package Documentation (`f-dotfiles.py`)
F-dotfiles uses a custom Python script [f-dotfiles.py](file:///home/nick/.gemini/antigravity/worktrees/F-dotfiles/create-agents-documentation/f-dotfiles.py) (run via pre-commit hooks or manually) to automatically document packages.
* **Sentinel Comment**: Every package's `README.md` must contain the comment `<!--- Tree block injection -->`. The script injects the auto-generated directory tree view right after this comment.
* **Inline File Descriptions**: For any configuration file or script in a package, add a description comment in the first 10 lines in the format:
  ```
  # <filename>: <description>
  ```
  For example, in `aliases.zsh`: `# aliases.zsh: shell aliases`. The script extracts these comments to enrich the generated tree listing.
* **Regeneration**: Do not manually modify the tree listing block in package `READMEs`. Run `python3 f-dotfiles.py` to regenerate the documentation automatically.

---

### 3. Secret and Sensitive Files
* **Never commit actual secrets, passwords, or private keys**.
* Add any files containing sensitive information to the package-specific `.gitignore`.
* Commit a template file with the same name but with a `.example` suffix (e.g., `credentials.example`) containing dummy values to serve as a guide for users.

---

### 4. Git and Ignore Rules
* Keep directories clean. Use `.gitignore` or `.stow-local-ignore` files within package directories to prevent unwanted files (e.g., local state, caches) from being symlinked or tracked.
