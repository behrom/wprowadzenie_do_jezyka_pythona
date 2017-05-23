#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from math import sqrt

class MojaZespolona:
    def __init__(self, r, i):
        self.r = r
        self.i = i

    def __add__(self, o):
        if type(o) == int:
            return MojaZespolona(self.r + o, self.i);
        return MojaZespolona(self.r + o.r, self.i + o.i)

    def __radd__(self, o):
        if type(o) == int:
            return MojaZespolona(self.r + o, self.i);
        return MojaZespolona(self.r + o.r, self.i + o.i)

    def __str__(self):
        if self.i > 0:
            return "{} +{}.i".format(self.r, self.i)
        return "{} {}.i".format(self.r, self.i)

    def mod(self):
        r = self.r**2
        i = self.i**2

        return sqrt(r + i)


a = MojaZespolona(3, 2)
b = MojaZespolona(9, 2)

# print a + b
# print a + 3
# print 3 + a

def moj_generator(a, n):
    for i in xrange(1, n+1):
        yield MojaZespolona(a, i), MojaZespolona(a, i).mod()

for zesp, mod in moj_generator(2, 4):
    print str(zesp), "\t", mod