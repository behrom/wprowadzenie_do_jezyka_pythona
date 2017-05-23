#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MyList():
    def __init__(self, lista):
        self.lista = lista
        self.i = 0

    def __iter__(self):
        return self

    def next(self):
        if self.i == len(self.lista)-2 and self.i % 2 == 0:
            self.i = 1
        elif self.i == len(self.lista)-1 and self.i % 2 == 1:
            raise StopIteration

        self.i += 2

        return self.i, self.lista[self.i]


for i, d in MyList([10, 11, 12, 13, 14, 15, 16, 17, 18, 19]):
    print i, "\t", d