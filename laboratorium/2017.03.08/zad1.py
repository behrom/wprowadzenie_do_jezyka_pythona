#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MojaZespolona(object):
    def __init__(self, r, i):
        self.r = r
        self.i = i

    def __add__(self, o):
        if type(o) == int:
            return MojaZespolona(self.r + o, self.i);
        return MojaZespolona(self.r + o.r, self.i + o.i)

    def __radd__(self, o):
        if type(o) == int:
            return MojaZespolona(self.r + o, self.i)
        elif type(0) == MojaZespolona:
            return MojaZespolona(self.r + o.r, self.i + o.i)

    def __str__(self):
        if self.i > 0:
            return "{} +{}.i".format(self.r, self.i)
        return "{} {}.i".format(self.r, self.i)


a = MojaZespolona(3, 2)
b = MojaZespolona(9, 2)


print a + b
print a + 3
print 3 + a
