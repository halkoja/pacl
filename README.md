#pacl.py
View Arch linux change logs parsed from the official git repository (https://git.archlinux.org/)

#Usage
pacl [-v] [\<number of entries\>] <pkgname>

The -v flag adds update description, which often includes more details.

Also supports piping, e.g.,

pacman -Ssq htop | pacl

#Required packages & libraries
python 2, urllib and lxml.
