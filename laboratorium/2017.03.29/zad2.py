#!/usr/bin/env python
#-*- coding: utf-8 -*-

from threading import Thread
import time

COUNT = 200000000

def countdown(n):
    while n > 0:
        n -= 1

start_time = time.time()
# jeden watek
countdown(COUNT)

print "jeden watki", time.time() - start_time

start_time = time.time()

t1 = Thread(target=countdown, args=(COUNT // 2,))
t2 = Thread(target=countdown,args=(COUNT//2,))
t1.start(); t2.start()
t1.join(); t2.join()

print "dwa watki", time.time() - start_time
print "nie chce mi sie"