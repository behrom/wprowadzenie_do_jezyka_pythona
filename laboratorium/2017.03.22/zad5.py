#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Lista:
    def __init__(self, array):
        self.x = 0
        self.i = -2
        self.array = array

    def __iter__(self):
        return self

    def next(self):
        if (self.i == len(self.array)-2 and self.x == 0):
            self.x = 1
            self.i = -1
        elif(self.i == len(self.array)-1 and self.x == 1):
            raise StopIteration
        self.i += 2
        return self.i, self.array[self.i]

for i, l in Lista([10, 11, 12, 13, 14, 15, 16, 17, 18, 19]):
    print i, l
