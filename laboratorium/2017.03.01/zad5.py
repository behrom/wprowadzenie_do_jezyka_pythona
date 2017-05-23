#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Zadanie 5
def factory(n):
    def do():
        print range(n)

    return do

a = factory(5)

a()