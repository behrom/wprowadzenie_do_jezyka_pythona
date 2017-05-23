#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


class LiczbaLosowa:
    def __getattr__(self, name):
        return random.random()

    def __setattr__(self, name, value):
        raise ValueError('Rzucam mieso')



a = LiczbaLosowa()
a.x = 5;

print a.x
