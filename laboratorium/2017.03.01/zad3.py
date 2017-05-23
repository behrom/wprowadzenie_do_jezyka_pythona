#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Zadanie 3
def FF(n):
    print "globals:\n", globals()
    print "locals:\n", locals()
    if (n == 0):
        return 2
    return (n + 1) * FF(n - 1)


def GG(n):
    print "globals:\n", globals()
    print "locals:\n", locals()

    if n == 0:
        return 3
    elif n == 1:
        return 5
    elif n == 2:
            return 7
    else:
        return GG(n - 3) + GG(n - 1) * GG(n - 2) + GG(n - 1)

GG(5)
