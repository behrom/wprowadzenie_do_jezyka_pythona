#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DziwnaLiczba():
    def __init__(self, liczba):
        if liczba == 0:
            raise ValueError
        self.liczba = liczba

    def __add__(self, other):
        return DziwnaLiczba(self.liczba * other.liczba)

    def __mul__(self, other):
        return DziwnaLiczba(self.liczba + other.liczba)

a = DziwnaLiczba(-3) + DziwnaLiczba(3)
print a.liczba

a = DziwnaLiczba(-3) * DziwnaLiczba(3)
