#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Kolory:
    _kols = {"Silver": "#C0C0C0", "Gray": "#808080", "Black": "#000000", "Red": "#FF0000",
             "Maroon": "#800000", "Yellow": "#FFFF00", "Olive": "#808000", "Lime": "#00FF00",
             "Green": "#008000", "Aqua": "#00FFFF", "Teal": "#008080", "Blue": "#0000FF",
             "Navy": "#000080", "Fuchsia": "#FF00FF", "Purple": "#800080"}

    def __getattr__(self, name):
        try:
            tmp = name[0:1].upper() + name[1:].lower()
            return self._kols[tmp]
        except KeyError:
            raise AttributeError

a = Kolory()

print a.kaczka