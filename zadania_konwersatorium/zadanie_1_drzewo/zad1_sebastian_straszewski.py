#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division

import math
from random import randint


# nazwa pliku do ktorego zostanie zapisane drzewo
# wymagany format svg
file_name = "tree.svg"

# wymiary obrazka
max_width = 1366
max_height = 768

# modyfikacja kata jezeli < 50 to galezie nie rosna w dol
s = 60

# [grubość, kolor]
tree_texture = [70, [100, 60, 0]]

# pozycja pnia na obrazku
root_position = [max_width / 2, max_height]


class Branch:
    """Klasa reprezentujaca galaz drzewa."""

    def __init__(self, start_point, end_point, texture):
        """ Konstruktor klasy generujacej pien.

        Parameters:
            start_point - poczatek z ktorego wychodzi galaz w postaci listy
            end_point   - punkt koncowy galezi w postaci listy
            texture     - zmienna przechowujaca grubosc oraz color galezi
        """

        self.start_point = start_point
        self.end_point = end_point
        self.texture = texture

    def __str__(self):
        """ Funkcja odpowiedzialna za zamiane obiektu na string."""

        return (r'<path d="M{},{},'
                ' L{},{} Z"'
                ' style="stroke: rgb({},{},{});'
                ' stroke-width: {}"/>\n').format(
                    self.start_point[0], self.start_point[1],
                    self.end_point[0], self.end_point[1],
                    self.texture[1][0], self.texture[1][1], self.texture[1][2],
                    self.texture[0])

    def fork(self, alpha, length, texture):
        """ Funkcja tworzy rozgalezienia dla danej galezi.

        Parameters:
            alpha   - kat pod jakim maja byc rysowane nowe galezie
            length  - dlugosc galezi
            texture - zmienna przechowujaca texture galezi [grubosc, kolor]

        Returns:
            rozgalezienie w postaci listy galezi wychodzacych z tego samego punktu
        """

        alpha = math.radians(alpha)

        x = self.end_point[0] + length * math.cos(alpha)
        y = self.end_point[1] + length * math.sin(alpha)

        A = [x, y]
        B = [self.end_point[0], y]
        C = [-x + 2 * self.end_point[0], y]

        return [Branch(self.end_point, A, texture),
                Branch(self.end_point, B, texture),
                Branch(self.end_point, C, texture)]


def tree_fractal(branch_length, branch_alpha, tree_lvl):
    """ Funkcja tworzy plik z drzewem.

    Parameters:
        branch_length   - dlugosc pnia od ktorej zalezy dlugosc pozostalych galezi
        branch_length   - kat wzgledem jakiego maja byc rysowane wszystkie galezie
        tree_lvl        - ilosc poziomow drzewa

    Example:
        tree_fractal(350, -20, 6)

    """

    def lvl_change(length, texture):
        """ Funkcja aktualizujaca parametry galezi."""

        texture[0] = 2 / 3.0 * texture[0] + 1
        texture[1][1] += 20

        return (2 / 3 * length,
                texture)

    # lista zawierajaca galezie drzewa dla poprzedniego poziomu
    branches = []

    # tworzenie zerowego poziomu - pnia
    trunk = Branch(
        root_position,
        [root_position[0], root_position[1] - branch_length],
        tree_texture
    )

    # zapisanie do pliku naglowka svg oraz korzenia
    with open(file_name, 'w') as file:
        res = '<svg width="{}" height="{}">\n'\
            .format(max_width, max_height)

        res += str(trunk)

        file.write(res)

    branches.append(trunk)

    # generowanie nowych galezi drzewa
    for i in range(tree_lvl):
        # aktualizacja parametrow galezi dla nowego poziomu
        branch_length, texture = lvl_change(branch_length, tree_texture)

        new_branches = []

        for branch in branches:
            # zmiana kata dla kazdego rozgalezienia
            angle = branch_alpha + randint(-1, 1) * randint(1, s)
            new_branches += branch.fork(angle, branch_length, texture)

        branches = new_branches

        # dopisanie do pliku aktualnie wyznaczonego poziomu drzewa
        with open(file_name, 'a') as file:
            res = "".join([str(t) for t in branches])
            file.write(res)

    # dodanie taga zamykajacego plik
    with open(file_name, 'a') as file:
        file.write('</svg>\n')

tree_fractal(350, -20, 6)
