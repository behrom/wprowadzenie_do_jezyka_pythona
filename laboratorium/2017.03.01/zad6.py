#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Zadanie 6
def vars(n):
    for i in range(n):
        globals()['v' + str(i)] = i**2

vars(5)

print globals()