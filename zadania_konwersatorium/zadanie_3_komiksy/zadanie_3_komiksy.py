#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
# wymagamy biblioteki w wersji min 3.0
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

import os.path
import urllib2
from bs4 import BeautifulSoup

# śćieżka do folderu cache przechowującego pobrane komiksy
CACHE = "cache/"

def get_comic(comic="random", next_comic=""):
    """Funkcja pobierajaca komiks z XKCD.

    :param comic: parametr opisujacy czy ma byc pobrany komiks najnowszy "new", losowy "random",
                czy o zadanym numerze
    :param next_comic: parametr opisujacy czy ma zostac pobrany nastepny obrazek, czy poprzedni
    :return: tupla zawierajaca numer i tytul komiksu, lub komunikat "ERROR 404" gdy nie udalo sie pobrac
            komiksu o zadanym numerze
    """

    # jeżeli parametr comic jest równy "random" to losujemy komiks
    # jeżeli parametr comic jest równy "new" to pobieramy najnowszy komiks
    # parametr comic jest liczba to pobierany jest komiks o zadanym numerze
    if comic == "random":
        response = urllib2.urlopen("https://c.xkcd.com/random/comic/")
    elif comic == "new":
        response = urllib2.urlopen("https://xkcd.com/")
    else:
        try:
            comic_id = int(comic)
        except ValueError:
            raise ValueError('comic must be number, "random" or "new"')

        # sprawdzenie czy ma być pobrany komiks poprzedzajacy zadany indeks
        # czy następny, jeżeli next_comic nie zostanie ustalone pobierany
        # jest komiks o wskazanym numerze
        if next_comic == True:
            comic_id += 1
        elif next_comic == False:
            comic_id -= 1

        # próba pobrania komiksu o zadanym numerze, jeżeli podamy błędny numer
        # zwrócony zostaje komunikat o błędzie 404
        try:
            response = urllib2.urlopen("https://xkcd.com/{0}/".format(comic_id))
        except urllib2.HTTPError, e:
            if e.code == 404:
                return "Error 404"

    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    middle = soup.find(id="middleContainer")

    # pobranie tytulu komiksu
    for data in soup.find(id="ctitle"):
        title = data

    # pobranie id komiksu w przypadku gdy nie zostalo podane w argumencie
    if comic == "random" or comic == "new":
        for data in middle.find_all("a", accesskey="p"):
            comic_id = data["href"][1:-1]
            comic_id = str(int(comic_id) + 1)
            break

    # pobranie linku do komiksu
    for data in middle.find_all("img", alt=True):
        src = data["src"]
        img_type = "." + src.split("/")[-1].split(".")[1]
        break

    # przeszukuje folder cache w poszukiwaniu komiksu o zadanym id
    # jezeli znajduje sie w nim to zwracam wynik
    # w przeciwnym razie pobieram nowy komiks
    if os.path.exists(CACHE + "{0}{1}".format(comic_id, img_type)):
        print "Obrazek znajduje sie juz w cache."
        return comic_id, img_type, title

    # pobranie komiksu i zapisanie w cache
    print "Pobieram obrazek: {0}".format(comic_id)

    f = open(CACHE+"{0}{1}".format(comic_id, img_type), "wb")
    f.write(urllib2.urlopen("http:" + src).read())
    f.close()

    return comic_id, img_type, title


class App(Gtk.Window):
    """Klasa implementujaca okno glowne aplikacji."""

    def __init__(self):
        # sprawdzenie czy istnieje folder cache i ewentualne jego utworzenie
        if not os.path.exists(CACHE):
            os.mkdir(CACHE)

        Gtk.Window.__init__(self)
        # ustawienie tytulu okna oraz rozmiaru
        self.set_title("Comics from XKCD")

        # ustawienie stałego rozmiaru okna
        self.set_default_size(600, 600)
        self.set_resizable(False)

        # obsługa wcisnięcia przycisku "krzyżyka" zamykającego aplikację
        self.connect("delete-event", Gtk.main_quit)

        # zmienna przechowująca wartość o jaką ma zostać przeskalowany komiks
        # domyślnie jest równa 1 - komiks jest w oryginalnym rozmiarze
        self.rescale = 1

        # zmienna przechowująca nazwę pliku do komikus
        self.img_file = ""

        # ustawienie menu programu
        lbl_box = Gtk.HBox()
        self.id_label = Gtk.Label("ID: ")

        # w tym komponencie wyświetlany jest numer aktualnie przeglądanego komiksu
        # jego zmiana powoduje wczytanie komiksu o zadanym numerze
        self.id = Gtk.Entry()

        # ustawienie stałej wielkości komponentu na 7 znakóœ
        self.id.set_max_width_chars(7)
        self.id.set_width_chars(7)
        self.id.connect("activate", self.set_comic, "this")

        # Label przechowujący tytuł komiksu
        self.title = Gtk.Label()

        lbl_box.pack_start(self.id_label, False, True, 0)
        lbl_box.pack_start(self.id, False, True, 0)
        lbl_box.pack_start(self.title, True, True, 0)

        # ustawienie przycisków sterujących programem
        btn_box = Gtk.HBox()
        # przycisk obsługujący wczytanie poprzedniego komiksu
        self.prev_comic_btn = Gtk.Button.new_with_label("Poprzedni")
        self.prev_comic_btn.connect("clicked", self.set_comic, "prev")

        # przycisk obsługujący wczytanie najnowszego komiksu
        self.new_comic_btn = Gtk.Button.new_with_label("Najnowszy")
        self.new_comic_btn.connect("clicked", self.set_comic, "new")

        # przycisk obsługujący wczytanie losowego komiksu
        self.random_comic_btn = Gtk.Button.new_with_label("Losowy")
        self.random_comic_btn.connect("clicked", self.set_comic, "random")

        # przycisk obsługujący wczytanie następnego komiksu
        self.next_comic_btn = Gtk.Button.new_with_label("Następny")
        self.next_comic_btn.connect("clicked", self.set_comic, "next")

        # przycisk pozwalający powiększyć komiks
        self.plus_btn = Gtk.Button.new_with_label("+")
        self.plus_btn.connect("clicked", self.scale, "plus")

        # przycisk pozwalający pomniejszyć komiks
        self.minus_btn = Gtk.Button.new_with_label("-")
        self.minus_btn.connect("clicked", self.scale, "minus")

        btn_box.pack_start(self.minus_btn, True, False, 0)
        btn_box.pack_start(self.plus_btn, True, False, 0)
        btn_box.pack_start(self.prev_comic_btn, True, False, 0)
        btn_box.pack_start(self.new_comic_btn, True, False, 0)
        btn_box.pack_start(self.random_comic_btn, True, False, 0)
        btn_box.pack_start(self.next_comic_btn, True, False, 0)

        # komponent przechowujący wyświetlany komiks
        self.comic_img = Gtk.Image()
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_min_content_width(600)
        self.scrolled_window.set_max_content_width(600)

        self.scrolled_window.set_min_content_height(600)
        self.scrolled_window.set_max_content_height(600)

        window_box = Gtk.VBox()
        window_box.pack_start(btn_box, False, False, 0)
        window_box.pack_start(lbl_box, False, False, 0)
        window_box.pack_start(self.scrolled_window, False, False, 0)

        self.add(window_box)
        self.show_all()

    def load_comic(self, file):
        """Metoda wczytująca komiks z pliku.
        
        :param: file - ścieżka do komiksu, który ma zostać wczytany
        """
        # wczytanie komiksu
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(CACHE + "{}".format(file))

        # przeskalowanie obrazka
        width = pixbuf.get_width() * self.rescale
        height = pixbuf.get_height() * self.rescale
        pixbuf = GdkPixbuf.Pixbuf.scale_simple(pixbuf, width, height, GdkPixbuf.InterpType.BILINEAR)

        # wyświetlenie obrazka
        self.comic_img.set_from_pixbuf(pixbuf)

        if self.scrolled_window.get_child():
            self.scrolled_window.remove(self.scrolled_window.get_child())

        self.scrolled_window.add(self.comic_img)

    def scale(self, _, scale_type):
        """Metoda zmieniająca parametr o ile ma zostać przeskalowany obrazek.
        
        :param scale_type - parametr określający czy ma być powiększony czy pomniejszony obrazek.
        """
        if scale_type == "plus":
            if self.rescale < 2:
                self.rescale += 1 / 5
        else:
            if self.rescale > 2 / 5:
                self.rescale -= 1 / 5

        # wczytanie przeskalowanego obrazka
        if not self.id.get_text() == "":
            self.load_comic(self.img_file)

    def set_comic(self, _, state):
        """Metoda odpowiedzialna za pobranie i wyświetlenie komiksu.
        
        :param _ - przycisk który wywolal metode, nie wykorzystywany wewnatrz niej
        :param state - parametr dzięki któremu ustawiamy czy ma zostać wyświetlony poprzedni,
                    losowy czy nastepny komiks. 
                    "this" - wyswietlenie aktualnego komiksu
                    "new" - wyswietlenie najnowszego komiksu
                    "random" - wyswietlenie losowego komiksu
                    "next" - wyswietlenie nastepnego komiksu
                    "prev" - wyswietlenie poprzedniego komiksu
        """
        # zresetowanie parametru o jaki ma zostac zeskalowany komiks
        self.rescale = 1

        # zmienna przechowujaca wynik dzialania funkcji get_comic
        result = ""

        # wywolanie funkcji pobierajacej komiks w zaleznosci od
        # podanego parametru this
        if state == "this" and not self.id.get_text() == "":
            result = get_comic(int(self.id.get_text()))
        elif state == "prev" and not self.id.get_text() == "":
            result = get_comic(int(self.id.get_text()), False)
        elif state == "new":
            result = get_comic("new")
        elif state == "random":
            result = get_comic()
        elif state == "next" and not self.id.get_text() == "":
            result = get_comic(int(self.id.get_text()), True)

        # w zaleznosci od wyniku funkcji pobierajacej komiks:
        # wyswietlenie bledu
        # wyswietlenie pobranego komiksu
        if result == "":
            return
        elif result == "Error 404":
            # utworzenie okna popup z informacja o blednym id komiksu
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Podałeś błędny numer komiksu lub nie masz połączenie z siecią.")
            dialog.run()

            dialog.destroy()
        else:
            id, img_type, title = result

            self.id.set_text("{}".format(id))

            self.title.set_markup("<b>{}</b>".format(title))
            self.img_file = "{}{}".format(id, img_type)
            self.load_comic(self.img_file)

            self.show_all()

if __name__ == "__main__":
    a = App()
    Gtk.main()