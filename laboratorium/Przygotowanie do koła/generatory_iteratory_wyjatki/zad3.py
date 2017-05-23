#!/usr/bin/env python
# -*- coding: utf-8 -*-

def fib_gen():
    x, y = 1, 1

    while True:
        x, y = y, x + y
        yield x

fib = fib_gen()
summ = 0

for _ in xrange(30 + 1):
    summ += fib.next()

print summ