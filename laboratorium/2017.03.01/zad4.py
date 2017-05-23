#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Zadanie 4
def ksiegowosc(stan_konta, kwota):
    def wplata():
        print "wplata: ", locals()
        return stan_konta + kwota

    def wyplata():
        print "wyplata: ", locals()
        return stan_konta - kwota

    print "ksiegowosc: ", locals()
    return (wplata(), wyplata())

print ksiegowosc(100, 20)