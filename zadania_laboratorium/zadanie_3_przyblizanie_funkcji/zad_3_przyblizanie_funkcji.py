#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from itertools import izip


def prepare_plot():
    """Funkcja przygotowuje wykres.
    
    Zadaniem tej funkcji jest przygotowanie wykresu, czyli dodanie label oraz siatki.
    """

    # dodanie podpisu osi X
    plt.xlabel('Wartosci $x$', fontsize=23)

    # dodanie podpisu osi y
    plt.ylabel('Interpolacja wartosci $y$', fontsize=23)

    # dodanie siatki
    plt.grid(color=(0.7, 0.8, 1.0), linestyle='-')


def plot_points(nodes):
    """Funkcja rysujaca na wykresie pojedyncze punkty z listy.
    
    Parameters:
        nodes - lista punktow do narysowania
    """

    # pobranie wartosci x punktow z listy punktow
    x = [value[0] for value in nodes]
    
    # pobranie wartosci y punktow z listy punktow
    y = [value[1] for value in nodes]

    # narysowanie punktow na wykresie
    plt.plot(x, y, label='punkty', marker='o', linestyle='', markersize=8, color='blue')


def change_plot_limits():
    """Funkcja poprawia czytelnosc wykresu.
    
    Funkcja ta ustawia maksymalne i minimalne wartosci na osiach,
    w taki sposob by byl odstep 1 jednostki. 
    """
    
    # pobranie ustawien os
    axes = plt.gca()

    x = axes.get_xlim()
    y = axes.get_ylim()

    # ustawienie limitow dla os
    plt.xlim(x[0] - 1, x[1] + 1)
    plt.ylim(y[0] - 1, y[1] + 1)


def lin_intp_plot(nodes, prec):
    """Funkcja rysujaca interpolacje liniowa na wykresie.
    
    Parameters:
        nodes - lista punktow na podstawie, ktorej przebiega interpolacja
        prec  - precyzja z jaka maja byc wykonane obliczenia kolejnych
                zinterpolowanych wartosci
    
    Return:
        tupla w postaci (x, y), bedaca punktem 
    """
    def lin_intp_gen(nodes, prec):
        nodes_it = iter(nodes)

        A = nodes_it.next()
        B = nodes_it.next()

        a = (B[1] - A[1]) / (B[0] - A[0])

        for x_val in np.arange(nodes[0][0], nodes[-1][0] + prec, prec):
            if x_val > B[0]:
                A = B
                B = nodes_it.next()

                a = (B[1] - A[1]) / (B[0] - A[0])

            yield x_val, A[1] + (x_val - A[0]) * a


    # wyznaczenie wartosci x
    intp_x = [point[0] for point in lin_intp_gen(nodes, prec)]
    intp_y = [point[1] for point in lin_intp_gen(nodes, prec)]

    plt.plot(intp_x, intp_y, label='linear', linestyle='-', linewidth=1.5, color='red')


def nearest_intp_plot(nodes, prec):

    def nearest_intp_gen(nodes, prec):
        nodes_it = iter(nodes)

        A = nodes_it.next()
        B = nodes_it.next()

        xs = (A[0] + B[0]) / 2.0

        for x_val in np.arange(nodes[0][0], nodes[-1][0] + prec, prec):
            if x_val < xs:
                yield x_val, A[1]
            elif x_val == xs:
                yield x_val, A[1]
                yield x_val, B[1]
            else:
                yield x_val, B[1]

            if x_val > B[0]:
                A = B
                B = nodes_it.next()
                xs = (A[0] + B[0]) / 2.0

    intp_x = [point[0] for point in nearest_intp_gen(nodes, prec)]
    intp_y = [point[1] for point in nearest_intp_gen(nodes, prec)]

    plt.plot(intp_x, intp_y, label='nearest', linestyle='-', linewidth=1.5, color='#bfbf00')


def zero_intp_plot(nodes, prec):
    def zero_intp_gen(nodes, prec):
        nodes_it = iter(nodes)

        A = nodes_it.next()
        B = nodes_it.next()

        for x_val in np.arange(nodes[0][0], nodes[-1][0] + prec, prec):
            yield x_val, A[1]

            if x_val == B[0]:
                A = B
                yield x_val, A[1]
                B = nodes_it.next()

    intp_x = [point[0] for point in zero_intp_gen(nodes, prec)]
    intp_y = [point[1] for point in zero_intp_gen(nodes, prec)]

    plt.plot(intp_x, intp_y, label='zero', linestyle='-', linewidth=1.5, color='#00bfbf')


def lagr_intp_plot(nodes, prec):
    def lagr_intp(nodes, x):
        n = len(nodes)

        wynik = 0

        for k in xrange(n):
            tmp_x = 1
            for i in xrange(n):
                if k == i:
                    continue
                tmp_x *= (x - nodes[i][0]) / (nodes[k][0] - nodes[i][0])
            wynik += nodes[k][1] * tmp_x

        return wynik

    x = np.arange(nodes[0][0], nodes[-1][0], prec)
    intp_y = [lagr_intp(nodes, value) for value in x]
    plt.plot(x, intp_y, label='Lagrange', linestyle='-', linewidth=1.5, color='blue')



PREC = 0.001
DOMAIN = xrange(0, 10, 1)
CODOMAIN = np.sin(DOMAIN)

NODES = izip(DOMAIN, CODOMAIN)
NODES = list(NODES)


NODES.sort(key = lambda  x: x[0])

prepare_plot()
plot_points(NODES)

# lin_intp_plot(NODES, PREC)
# lagr_intp_plot(NODES, PREC)
# nearest_intp_plot(NODES, PREC)
zero_intp_plot(NODES, PREC)

plt.plot(x, intp_y, label='Lagrange', linestyle='-', linewidth=1.5, color='blue')
plt.legend(loc=3)

# change_plot_limits()
plt.show()
