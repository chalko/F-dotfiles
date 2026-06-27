# Dotstos nick's implementation of using stow to manage dot files.

<!--- Tree block injection -->
    └── bin
        └── dotstow


## How it works

```bash
dotstow PACKAGE
```

dotstow  uses sto install packages from the ~/F-dotstow direcory it has special handling for the operating system and hostname

```bash
HOSTNAME=hostname -s`
OS=`uname`
```

Packages are installed in this order

* base
* ooperating specific
* host specific
@Config is mapped to XDG_CONFIG_HOME repeating the base/os/host patter


## Instalation

Install stow

