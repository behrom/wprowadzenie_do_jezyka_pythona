#!/usr/bin/env python
# -*- coding: utf-8 -*

def fib_generator():
    x, y = 0, 1
    while True:
        yield x
        x, y = y, x + y

generator_liczb = fib_generator()

print sum([generator_liczb.next() for _ in xrange(30)])

