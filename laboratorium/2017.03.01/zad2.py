#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Zadanie 2
def silnia_it(n):
    return reduce(lambda x,y: x*y, range(1, n+1))

print silnia_it(5)

def silnia_rek(n):
    if(n == 1):
        return 1
    return n*silnia_rek(n-1)

print silnia_rek(5)