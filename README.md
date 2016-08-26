pacl.py: View Arch linux change logs parsed from the official git repository (https://git.archlinux.org/)

Usage: pacl [-v] [\<number of entries\>] <pkgname>

Supports piping, e.g.,
pacman -Ssq htop | pacl

Requires python 2, urllib and lxml.
