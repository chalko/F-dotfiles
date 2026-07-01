# Dotstow: Nick's implementation of using stow to manage dot files.

<!--- Tree block injection -->
    └── bin
        └── dotstow


## How it works

```bash
dotstow PACKAGE
```

dotstow uses stow to install packages from the ~/F-dotfiles directory. It has special handling for the operating system and hostname.

```bash
HOSTNAME=hostname -s`
OS=`uname`
```

Packages are installed in this order

* base
* operating system specific
* host specific

`@config` is mapped to `XDG_CONFIG_HOME`, repeating the base/os/host pattern.


## Installation

Install stow

