#-*- coding: utf-8 -*-
import gi
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import random  # losowanie min

n = 2


class Plansza(Gtk.Grid):

    def __init__(self, okno, rozmiar):
        Gtk.Grid.__init__(self)

        self.bezpieczne_pola = rozmiar*rozmiar - rozmiar

        self.okno = okno
        self.rozmiar = rozmiar

        self.generuj_plansze()
        self.ustaw_miny()

    def generuj_plansze(self):
        self.pola = []

        for i in range(self.rozmiar):
            self.pola.append([])

            for j in range(self.rozmiar):
                b = Gtk.Button.new_with_label("")
                self.pola[i].append(b)
                self.attach(b, i, j, 1, 1)
                b.connect("clicked", self.stan_pola, i, j)

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)

    def ustaw_miny(self):
        self.miny = set()

        for i in range(self.rozmiar):
            pozycja = (random.randint(0, self.rozmiar-1),
                       random.randint(0, self.rozmiar-1))

            self.miny.add(pozycja)

    def reset(self):
        self.bezpieczne_pola = self.rozmiar * self.rozmiar - self.rozmiar
        self.okno.set_title("Saper")

        self.ustaw_miny()

        for i in xrange(self.rozmiar):
            for j in range (self.rozmiar):
                self.pola[i][j].set_sensitive(True)
                self.pola[i][j].get_child().set_markup("")

    def ustaw_tekst(self, button, kolor, tekst):
        styl = '<span foreground="{}"><b>{}</b></span>'.format(kolor, tekst)
        button.get_child().set_markup(styl)
        button.set_sensitive(False)

    def ile_min_w_poblizu(self, x, y):
        if (x, y) in self.miny:
            return -1

        suma = 0

        for i in xrange(x - 1, x + 2):
            for j in xrange(y - 1, y + 2):
                if i < 0 or j < 0:
                    continue
                if (i, j) in self.miny:
                    suma += 1

        return suma

    def stan_pola(self, button, x, y):
        kolory = {"default": "brown",
                  -1: "red",
                  0: "black",
                  1: "orange",
                  2: "orangered",
                  3: "tomato"}

        ilosc_min = self.ile_min_w_poblizu(x, y)

        if ilosc_min == -1:
            self.ustaw_tekst(button, kolory[ilosc_min], "M")
        elif ilosc_min > 3:
            self.ustaw_tekst(button, kolory["default"], ilosc_min)
        else:
            self.ustaw_tekst(button, kolory[ilosc_min], ilosc_min)

        self.bezpieczne_pola -= 1
        print self.bezpieczne_pola

    def odslon(self):
        for i in range(self.rozmiar):
            for j in range (self.rozmiar):
                if self.pola[i][j].get_sensitive():
                    self.stan_pola(self.pola[i][j], i, j)

    def przegrana(self):
        self.okno.set_title("PRZEGRAŁEŚ!")
        self.odslon()

    def wygrana(self):
        self.okno.set_title("WYGRAŁEŚ!")
        self.odslon()
        dialog = Gtk.MessageDialog(self.okno, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK)


class App(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Saper")
        self.set_default_size(200,200)

        self.connect("delete-event", Gtk.main_quit)

        box = Gtk.VBox()

        self.nowa = Gtk.Button.new_with_label("Nowa gra")
        self.nowa.connect("clicked", self.nowa_gra)

        box.pack_end(self.nowa, True, True, 0)

        self.plansza = Plansza(self, n)

        box.pack_end(self.plansza, True, True, 0)

        self.add(box)

        self.show_all()

    def nowa_gra(self, btn):
        self.plansza.reset()

if __name__ == "__main__":
    a = App()
    Gtk.main()
