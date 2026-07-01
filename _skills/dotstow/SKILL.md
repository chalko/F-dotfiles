---
name: dotstow
description: Manage and stow dotfiles and configs in the F-dotfiles repository using the custom dotstow tool.
allowed-tools: Bash(./scripts/f-dotfiles) Bash(./scripts/dotstow*) run_command(./scripts/f-dotfiles) run_command(./scripts/dotstow*) Read Write Edit Glob Grep view_file write_to_file replace_file_content multi_replace_file_content list_dir grep_search
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
     ./scripts/f-dotfiles
     ```

4. **Verify and Install**:
   * Alert the user to back up any existing files in `~` or `~/.config` that would cause conflicts.
   * Install the package by running the helper script:
     ```bash
     ./scripts/dotstow <package_name>
     ```

