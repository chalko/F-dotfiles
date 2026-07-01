---
name: dotstow
description: Manage and stow dotfiles and configs in the F-dotfiles repository using the custom dotstow tool.
---

# dotstow Skill Instructions

Use this skill when you are asked to create, modify, stow, or debug configurations and packages in this repository.

## 1. Directory Structure Conventions

Always structure packages to align with `dotstow` and GNU Stow expectations:
* **Base Package Files**: Root of the package directory (symlinked to `~`).
* **OS-Specific Overrides**: Under `@${OS}` (e.g., `@Linux`, `@Darwin`).
* **Host-Specific Overrides**: Under `@${HOSTNAME}`.
* **XDG Config Home**: Under `@config` (symlinked to `~/.config`).
  * OS-specific: `@config/@${OS}`
  * Host-specific: `@config/@${HOSTNAME}`

## 2. Step-by-Step Workflow for Adding a Package

1. **Create Directory Structure**:
   * Create `package_name/`.
   * Create `package_name/.gitignore` and exclude keys/databases/caches.
   * Place base config files under the appropriate structure (e.g., `package_name/.gnupg/` or `package_name/@config/`).
   
2. **Add Header Self-Documentation**:
   * For every text configuration file, add an inline comment within the first 10 lines:
     ```
     # <filename>: <short description>
     ```
   
3. **Generate README**:
   * Create `package_name/README.md` containing:
     ```markdown
     # Package Name
     
     <!--- Tree block injection -->
     ```
   * Commit the files once so the `f-dotfiles` pre-commit hook runs and auto-generates the directory tree, OR run `python3 f-dotfiles.py` manually.

4. **Verify and Install**:
   * Alert the user to back up any existing files in `~` or `~/.config` that would cause conflicts.
   * Install the package by running:
     ```bash
     ./dotstow/bin/dotstow <package_name>
     ```
