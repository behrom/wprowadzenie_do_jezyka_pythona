#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from itertools import izip


def linear_intp(nodes):
    """Funkcja, ktora dla zadanej listy punktow zwraca funkcje liczaca interpolacje liniowa.
    
    Parameters:
        nodes - lista punktow, dla których wiadome jest, ze naleza do badanej funkcji
                w postaci listy dwuelementowych tupl np. [(1, 2), (3, 8)]
    
    Return:
        funkcja liczaca interpolacje liniowa dla zadanej tablicy argumentow (numpy.ndarray)
    """

    def linear(x):
        """Funkcja wyznaczajaca wartosci interpolacji liniowej.
        
        Parameters:
            x - tablica argumentow (numpy.ndarray), dla ktorych ma zostac policzona interpolacja
        
        Return:
            tablica wartosci (numpy.ndarray), zawierajaca wyliczone wartosci interpolacji    
        """

        # tworze pusta liste do ktorej beda dodawane wyliczone wartosci interpolacji
        intp_y = []

        for i in xrange(len(x)):
            # wyznaczam w jakim przedziale znajduje sie x
            # to znaczy po miedzy jakimi punktami z listy punktow znajduje sie
            # x, dla ktorego liczona jest wartosc
            idx = sum(map(lambda t: t <= x[i], zip(*nodes)[0])) - 1

            # wyliczam wartosci interpolacji liniowej przy wspolczynnik kierunkowego funkcji
            a = (nodes[idx + 1][1] - nodes[idx][1]) / (nodes[idx + 1][0] - nodes[idx][0])
            intp_y.append(a * (x[i] - nodes[idx][0]) + nodes[idx][1])

        # zwracam tablice wartosci (numpy.ndarray) po interpolacji
        return np.array(intp_y)

    # zwracam funkcje, liczaca dla zadanej tablicy argumentow, tablice wartosci po interpolacji
    return linear


def nearest_intp(nodes):
    """Funkcja, ktora dla zadanej listy punktow zwraca funkcje liczaca interpolacje "nearest".

    Parameters:
        nodes - lista punktow, dla których wiadome jest, ze naleza do badanej funkcji
                w postaci listy dwuelementowych tupl  np. [(1, 2), (3, 8)]

    Return:
        funkcja liczaca interpolacje "nearest" dla zadanej tablicy argumentow (numpy.ndarray)
    """

    def nearest(x):
        """Funkcja wyznaczajaca wartosci interpolacji "nearest".

        Parameters:
            x - tablica argumentow (numpy.ndarray), dla ktorych ma zostac policzona interpolacja

        Return:
            tablica wartosci (numpy.ndarray), zawierajaca wyliczone wartosci interpolacji    
        """

        # tworze pusta liste do ktorej beda dodawane wyliczone wartosci interpolacji
        intp_y = []

        for i in xrange(len(x)):
            # wyznaczam w jakim przedziale znajduje sie x
            # to znaczy po miedzy jakimi punktami z listy punktow znajduje sie
            # x, dla ktorego liczona jest wartosc
            idx = sum(map(lambda t: t <= x[i], zip(*nodes)[0])) - 1

            # wyznaczam argument dla ktorego ma nastapic zmiana wartosci
            # srodek pomiedzy punktami z listy
            xs = (nodes[idx][0] + nodes[idx + 1][0]) / 2.0

            # zapisanie odpowiednich wartosci do tablicy wartosci
            if x[i] <= xs:
                intp_y.append(nodes[idx][1])
            else:
                intp_y.append(nodes[idx + 1][1])

        # zwracam tablice wartosci (numpy.ndarray) po interpolacji
        return np.array(intp_y)

    # zwracam funkcje, liczaca dla zadanej tablicy argumentow, tablice wartosci po interpolacji
    return nearest


def zero_intp(nodes):
    """Funkcja, ktora dla zadanej listy punktow zwraca funkcje liczaca interpolacje "zero".

    Parameters:
        nodes - lista punktow, dla których wiadome jest, ze naleza do badanej funkcji
                w postaci listy dwuelementowych tupl  np. [(1, 2), (3, 8)]

    Return:
        funkcja liczaca interpolacje "zero" dla zadanej tablicy argumentow (numpy.ndarray)
    """

    def zero(x):
        """Funkcja wyznaczajaca wartosci interpolacji "zero".

            Parameters:
                x - tablica argumentow (numpy.ndarray), dla ktorych ma zostac policzona interpolacja

            Return:
                tablica wartosci (numpy.ndarray), zawierajaca wyliczone wartosci interpolacji    
            """
        # tworze pusta liste do ktorej beda dodawane wyliczone wartosci interpolacji
        intp_y = []

        for i in xrange(len(x)):
            # wyznaczam w jakim przedziale znajduje sie x
            # to znaczy po miedzy jakimi punktami z listy punktow znajduje sie
            # x, dla ktorego liczona jest wartosc
            idx = sum(map(lambda t: t <= x[i], zip(*nodes)[0])) - 1

            # dodaje do tablicy wyznaczone wartosci interpolacji
            intp_y.append(nodes[idx][1])

        # zwracam tablice wartosci (numpy.ndarray) po interpolacji
        return np.array(intp_y)

    # zwracam funkcje, liczaca dla zadanej tablicy argumentow, tablice wartosci po interpolacji
    return zero


def lagrange_intp(nodes):
    """Funkcja, ktora dla zadanej listy punktow zwraca funkcje liczaca interpolacje Lagrange'a.

    Parameters:
        nodes - lista punktow, dla których wiadome jest, ze naleza do badanej funkcji
                w postaci listy dwuelementowych tupl  np. [(1, 2), (3, 8)]

    Return:
        funkcja liczaca interpolacje Lagrange'a dla zadanej tablicy argumentow (numpy.ndarray)
    """

    def lagrange(x):
        """Funkcja wyznaczajaca wartosci interpolacji Lagrange'a.

        Parameters:
            x - tablica argumentow (numpy.ndarray), dla ktorych ma zostac policzona interpolacja

        Return:
            tablica wartosci (numpy.ndarray), zawierajaca wyliczone wartosci interpolacji    
        """
        # tworze pusta liste do ktorej beda dodawane wyliczone wartosci interpolacji
        intp_y = []

        # po wszystkich x dla których ma byc wyliczona wartosc
        for i in xrange(len(x)):
            # zmienna przechowujaca wynik mnozenia
            # (x-xi)(xk-xi) po wszystkich 0 < i < n, i != k, , gdzie n - liczba interpolowanych punktow
            tmp_x = 1.0
            # zmienna przechowujaca sume mnozen
            # tmp_x * yk dla wszystkich 0 < k < n, gdzie n - liczba interpolowanych punktow
            tmp_y = 0

            # implementacja wyliczenia zinterpolowanych wartosci funkcji na podstawie wzoru podanego
            # w specyfikacji
            for j in xrange(len(zip(*NODES)[0])):
                tmp_x = 1.0

                for k in xrange(len(zip(*NODES)[0])):
                    if j == k:
                        continue

                    tmp_x *= (x[i] - nodes[k][0]) / (nodes[j][0] - nodes[k][0])

                tmp_y += nodes[j][1] * tmp_x

            # dodanie wyliczonej wartosci do listy
            intp_y.append(tmp_y)

        # zwracam tablice wartosci (numpy.ndarray) po interpolacji
        return np.array(intp_y)

    # zwracam funkcje, liczaca dla zadanej tablicy argumentow, tablice wartosci po interpolacji
    return lagrange

# tworze generator punktow, dla których wiadome jest, ze naleza do funkcji
# w tym przypadku funkcji sinus, ktorej dziedzina sa wartosci od 0 do 10
NODES = izip(np.arange(0, 10), np.sin(np.arange(0, 10)))

# tworze liste tych punktow
NODES = list(NODES)

# tworze tablice (numpy.ndarray) argumentow, dla ktorych beda wyliczane
# wartosci interpolacji
x = np.arange(0, 9, 0.01)

# dodaje podpis osi X do wykresu
plt.xlabel('Wartosci $x$', fontsize=23)

# dodaje podpis osi y do wykresu
plt.ylabel('Interpolacja wartosci $y$', fontsize=23)

# dodanie siatki do wykresu funkcji
plt.grid(color=(0.7, 0.8, 1.0), linestyle='-')

# rysuje punkty, dla ktorych znana jest wartosc funkcji na wykresie
plt.plot(zip(*NODES)[0], zip(*NODES)[1], label='punkty', marker='o', linestyle='', markersize=8, color='blue')

# rysuje jak wyglada interpolacja liniowa,
# dla wczesniej zdefiniowanej tablicy argumentow
# oraz wartosci funkcji wygenerowanych przy uzyciu zaimplementowanej wyzej funkcji
plt.plot(x, linear_intp(NODES)(x), label='linear', linestyle='-', linewidth=1.5, color='red')

# rysuje jak wyglada interpolacja Lagrange'a,
# dla wczesniej zdefiniowanej tablicy argumentow
# oraz wartosci funkcji wygenerowanych przy uzyciu zaimplementowanej wyzej funkcji
plt.plot(x, lagrange_intp(NODES)(x), label='Lagrange', linestyle='-', linewidth=1.5, color='blue')

# rysuje jak wyglada interpolacja "nearest",
# dla wczesniej zdefiniowanej tablicy argumentow
# oraz wartosci funkcji wygenerowanych przy uzyciu zaimplementowanej wyzej funkcji
plt.plot(x, nearest_intp(NODES)(x), label='nearest', linestyle='-', linewidth=1.5, color='#bfbf00')

# rysuje jak wyglada interpolacja "zero",
# dla wczesniej zdefiniowanej tablicy argumentow
# oraz wartosci funkcji wygenerowanych przy uzyciu zaimplementowanej wyzej funkcji
plt.plot(x, zero_intp(NODES)(x), label='zero', linestyle='-', linewidth=1.5, color='#00bfbf')

# umieszczam legende w lewym dolnym rogu wykresu
plt.legend(loc=3)

# pokazuje wykres na ekranie
plt.show()

