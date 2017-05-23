#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sum_rek(n):
    print locals()
    if(n == 1):
        return 1
    else:
        return n + sum_rek(n-1)

def sum_it(n):
    sum = 0

    for i in xrange(1, n+1):
        print locals()
        sum += i

    return sum
print globals()
print sum_rek(4)
print sum_it(4)
print globals()
# print reduce(lambda x,y: x+y, xrange(5))