---
name: dotstow
description: Manage and stow dotfiles and configs in the F-dotfiles repository using the custom dotstow tool. Use this skill whenever you are asked to create, modify, add, install, stow, list, or configure any packages, configuration files, or dotfiles in this repository.
allowed-tools: Bash(./_skills/dotstow/scripts/f-dotfiles) Bash(./_skills/dotstow/scripts/dotstow*) run_command(./_skills/dotstow/scripts/f-dotfiles) run_command(./_skills/dotstow/scripts/dotstow*) Read Write Edit Glob Grep view_file write_to_file replace_file_content multi_replace_file_content list_dir grep_search
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
   * Create `package_name/.gitignore` and/or `package_name/.stow-local-ignore` to prevent unwanted local files/caches from being symlinked or tracked.
   * Place configuration files under the appropriate directory structure.
   * **Secrets & Sensitive Data**: Never commit actual secrets, passwords, or private keys. Add them to `.gitignore` and commit a `.example` template instead.

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
   * Commit the files once so the `f-dotfiles` pre-commit hook runs and auto-generates the directory tree, OR run the helper script:
     ```bash
     ./_skills/dotstow/scripts/f-dotfiles
     ```

4. **Verify and Install**:
   * Alert the user to back up any existing files in `~` or `~/.config` that would cause conflicts.
   * Install the package by running the helper script:
     ```bash
     ./_skills/dotstow/scripts/dotstow <package_name>
     ```

## 3. Conflict Avoidance for Overlapping Configurations

When stowing configurations that might overlap (e.g., configuring git or zsh both at the base level and with host/OS specific overrides), do NOT name host-specific config files with the exact same name as base files if they reside in the same directories, as GNU Stow will fail with target link conflicts.

Instead, use inclusion mechanisms:
1. **Git configs**: Create a `config.local` file under `@config/@${HOSTNAME}/git/config.local` (or `@config/@${OS}/git/config.local`). Then, in the base `git/@config/git/config`, append:
   ```ini
   [include]
   	path = config.local
   ```
2. **Zsh configs**: Use host-specific scripts (e.g., `zsh/@config/zsh/aliases.zsh` can source a host-specific file if it exists, or the host package can stow a file named `aliases-local.zsh` that the main shell files load).


