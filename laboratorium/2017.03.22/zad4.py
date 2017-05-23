#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sil_gen():
    silnia = 1
    x = 1
    while True:
        silnia *= x
        x += 1
        yield silnia

generator_liczb = sil_gen()

print sum([generator_liczb.next() for _ in xrange(5)])