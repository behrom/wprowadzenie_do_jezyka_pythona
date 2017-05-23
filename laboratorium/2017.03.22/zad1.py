#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math


class MojaZespolona:
    def __init__(self, r, i):
        self.r = r
        self.i = i

    def __add__(self, o):
        if( type(o) == int ):
            return MojaZespolona(self.r + o, self.i);
        return MojaZespolona(self.r + o.r, self.i + o.i)

    def __radd__(self, o):
        if( type(o) == int ):
            return MojaZespolona(self.r + o, self.i);
        return MojaZespolona(self.r + o.r, self.i + o.i)

    def __str__(self):
        if( self.i > 0 ):
            return "{} + {}.i".format(self.r, self.i)
        return "{} {}.i".format(self.r, self.i)

    def mod(self):
        r = self.r**2
        i = self.i**2

        return math.sqrt(r + i)

def generator(a, n):
    for i in xrange(n):
        liczba = MojaZespolona(a, i)
        yield str(liczba), liczba.mod()

for ob in generator(2, 4):
    print ob