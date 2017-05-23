#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import math
import random

# wymiary obrazka
max_width = 1366
max_height = 768

# wysokosc drzewa
tree_level = 9

# kolor pnia
trunk_color = [100, 60, 0]

# grubosc galezi
branch_size = 44

# dlugosc galezi
branch_length = 290

# kat nachylenia galezi
branch_angle = -33

# stopien zmiany kata nachylenia galezi
s = 30


class Trunk:
    """ Klasa generujaca pien. """

    def __init__(self, root, length, size, color):
        """ Konstruktor klasy generujacej pien.

        Args:
            root    - poczatek z ktorego wychodzi pien w postaci dwuelementowej tupli (x, y)
            length  - wysokosc pnia
            size    - grubosc pnia
            color   - kolor pnia w postaci trojelementowej tupli (R, G, B)
        """
        self.root = root
        self.length = length
        self.size = size
        self.color = color

    def __str__(self):
        """ Funkcja odpowiedzialna za wyswietlanie danych o pniu w postaci svg. """

        tag_format = (
            r'<path '
            r'd="M{root[0]},{root[1]}, L{root[0]},{fork_distance} Z" '
            r'style="stroke: rgb({color[0]},{color[1]},{color[2]}); '
            r'stroke-width: {size}"/>\n'
        )
        tag_fields = {
            'root': self.root,
            'fork_distance': self.root[1] - self.length,
            'color': self.color,
            'size': self.size
        }
        return tag_format.format(**tag_fields)


class Branches:
    """ Klasa generuje 3 galezie (1 rozgalezienie) wychodzace z tego samego punktu.

    Example:
        b = Branches( (1, -1), 5, 6, -2, (123, 23, 0)  )

        utworzone zostanie rozgalezienie w punkcie 1, -1, o galeziach
        dlugosci 5 i grubosci 6 pod katem -2 w kolorze (123, 23, 0)
    """

    def __init__(self, root, length, size, alpha, color):
        """ Konstruktor klasy.

        Odpowiedzialny jest za pobranie danych i wyznaczenie wierzcholkow galezi w rozgalezieniu

        Args:
            root    - poczatek z ktorego wychodza galezie w postaci dwuelementowej tupli (x, y)
            length  - dlugosc galezi
            size    - grubosc galezi
            alpha   - kat w stopniach pod ktorym znajduja sie galezie
            color   - kolor galezi w postaci trojelementowej tupli (R, G, B)
        """
        self.root = root
        self.length = length
        self.size = size
        self.alpha = alpha
        self.color = color

        # wylizcenie wspolrzednych wierzcholka A galezi
        tmp_x = self.root[0] + self.length * math.cos(math.radians(self.alpha))
        tmp_y = self.root[1] + self.length * math.sin(math.radians(self.alpha))

        self.A = (tmp_x, tmp_y)

        # wylizcenie wspolrzednych wierzcholka B galezi
        self.B = (self.root[0], tmp_y)

        # wylizcenie wspolrzednych wierzcholka C galezi
        tmp_x = -tmp_x + 2 * self.root[0]
        self.C = (tmp_x, tmp_y)

    def __str__(self):
        """ Funkcja odpowiedzialna za wypisanie rozgalezienia w postaci svg. """

        # dodanie do zmiennej tekstowej galezi z korzenia do punktu A w postaci svg
        # w celu pozniejszego wypisania calego rozgalezienia
        res = (r'<path d="M{},{}, L{},{} Z"'
               ' style="stroke: rgb({},{},{}); stroke-width: {}"/>\n').format(
                self.root[0], self.root[1],
                self.A[0], self.A[1],
                self.color[0], self.color[1], self.color[2],
                self.size)

        # dodanie do zmiennej tekstowej galezi z korzenia do punktu b w postaci svg
        # w celu pozniejszego wypisania calego rozgalezienia
        res += (r'<path d="M{},{}, L{},{} Z"'
               ' style="stroke: rgb({},{},{}); stroke-width: {}"/>\n').format(
                self.root[0], self.root[1],
                self.B[0], self.B[1],
                self.color[0], self.color[1], self.color[2],
                self.size)

        # dodanie do zmiennej tekstowej galezi z korzenia do punktu b w postaci svg
        # w celu pozniejszego wypisania calego rozgalezienia
        res += (r'<path d="M{},{}, L{},{} Z"'
               ' style="stroke: rgb({},{},{}); stroke-width: {}"/>\n').format(
                self.root[0], self.root[1],
                self.C[0], self.C[1],
                self.color[0], self.color[1], self.color[2],
                self.size)

        # zwrocenie zmiennej tekstowej
        return res


def tree(branch_length, alpha, levels):
    """ Funkcja tworzaca fraktal - drzewo.

    Args:
        branch_length   - dlugosc galezi
        alpha           - kat pod jakim maja byc rysowane galezie
        levels          - wysokosc drzewa
    """

    def add_to_file(tree_list):
        """ Funkcja sluzy do zapisu listy galezi w pliku.

        jako parametrz przyjmuje liste z galeziami
        """
        res = ""
        res += "\n".join([str(t) for t in tree_list])

        with open('tree.svg', 'a') as file:
            file.write(res)

    # wyjscie bez rysowania dla drzewa o wysokosci 0
    if levels == 0:
        return

    # zmienna przechowujaca pozycje drzewa
    trunk_root = (max_width / 2, max_height)

    # zmienna przechowujaca kolor dla poszczegolnych galezi
    # ulega zmianie w zaleznosci od poziomu drzewa
    trunk_color = globals()["trunk_color"]

    # zmienna przechowujaca grubosc galezi
    # ulega zmianie w zaleznosci od pozomu drzewa
    branch_size = globals()["branch_size"]

    # lista przechowujaca wczesniej wyliczone rozgalezienia
    prev_lvl_list = []

    # dodanie pnia drzewa do listy galezi
    prev_lvl_list.append(Trunk(trunk_root, branch_length, branch_size, trunk_color))

    # zapis do pliku
    add_to_file(prev_lvl_list)

    # wyjscie z funkcji z narysowanym tylko pniem dla poziomu 1 drzewa
    if levels == 1:
        return

    # lista przechowujaca aktualnie wyliczane rozgalezienia
    lvl_list = []

    # zmiana koloru dla rozgalezienia
    if trunk_color[1] < 249:
        trunk_color[1] += 6

    # narysowanie 2 poziomu drzewa w zaleznosci od pnia drzewa
    lvl_list.append(Branches((trunk_root[0], trunk_root[1] - branch_length),
                             (2 / 3) * branch_length, (2 / 3) * branch_size + 1, alpha, trunk_color))

    # zapis do pliku
    add_to_file(lvl_list)

    # zapamietanie wyznaczonych rozgalezien
    prev_lvl_list = lvl_list

    # wyzerowanie listy z aktualnie wyliczanymi rozgalezieniami
    lvl_list = []

    if levels == 2:
        return

    # petla generujaca kolejne poziomy drzewa
    for i in range(2, levels):
        # modyfikacja dlugosci galezi
        branch_length *= (2 / 3)

        # modyfikacja grubosci galezi
        branch_size = (2 / 3) * branch_size + 1

        # modyfikacja koloru jesli jest to mozliwe
        if trunk_color[1] < 249:
            trunk_color[1] += 6

        # petla wyznaczajaca kolejne rozgalezienia drzewa na bazie
        # juz istniejacych
        for b in prev_lvl_list:
            # wyliczenie pod jakim katem maja byc rysowane nowe galezie
            angle = alpha + random.randint(-1, 1) * random.randint(1, s)

            # wyznaczenie nowej trojki galezi
            lvl_list.append(Branches(b.A, branch_length, branch_size, angle, trunk_color))

            # wyliczenie pod jakim katem maja byc rysowane nowe galezie
            angle = alpha + random.randint(-1, 1) * random.randint(1, s)

            # wyznaczenie nowej trojki galezi
            lvl_list.append(Branches(b.B, branch_length, branch_size, angle, trunk_color))

            # wyliczenie pod jakim katem maja byc rysowane nowe galezie
            angle = alpha + random.randint(-1, 1) * random.randint(1, s)

            # wyznaczenie nowej trojki galezi
            lvl_list.append(Branches(b.C, branch_length, branch_size, angle, trunk_color))

        # zapisanie do pliku
        add_to_file(lvl_list)

        # zapamietanie wyznaczonych rozgalezien
        prev_lvl_list = lvl_list

        # wyzerowanie listy z aktualnie wyliczanymi rozgalezieniami
        lvl_list = []

# zapis naglowka pliku svg
with open('tree.svg', 'w') as file:
    file.write(('''<svg width="{}" height="{}">\n''').format(max_width, max_height))

# wyznaczenie drzewa
tree(branch_length, branch_angle, tree_level)

# zakonczenie pliku
with open('tree.svg', 'a') as file:
    file.write('</svg>')
