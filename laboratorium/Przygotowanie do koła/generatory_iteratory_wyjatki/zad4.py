#!/usr/bin/env python
# -*- coding: utf-8 -*-

def silnia_gen():
    silnia = 1
    i = 1

    while True:
        yield silnia
        silnia *= i
        i += 1


silnia = silnia_gen()

summ = 0

for _ in xrange(9+1):
    summ += silnia.next()

print summ