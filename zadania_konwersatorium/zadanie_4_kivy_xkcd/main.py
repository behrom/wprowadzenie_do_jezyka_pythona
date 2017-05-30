import os.path
import urllib2
from bs4 import BeautifulSoup
from functools import partial

import kivy
kivy.require('1.1.6')
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button


# Aplikacja dziala bardzo dobrze pod systemem Linux,
# niestety nie udalo mi sie przetestowac dzialania aplikacji pod systemem Android
# powodem byl problem z dolaczeniem biblioteki BeautifulSoup
# ale uwazam, ze aplikacja dzialalaby bardzo dobrze gdyby udalo mi sie
# zaimportowac biblioteke BeautifulSoup

# sciezka do folderu cache przechowujacego pobrane komiksy
CACHE = "cache/"


def get_comic(comic="random", next_comic=""):
    """Funkcja pobierajaca komiks z XKCD.

    :param comic: parametr opisujacy czy ma byc pobrany komiks najnowszy "new", losowy "random",
                czy o zadanym numerze
    :param next_comic: parametr opisujacy czy ma zostac pobrany nastepny obrazek, czy poprzedni
    :return: tupla zawierajaca numer i tytul komiksu, lub komunikat "ERROR 404" gdy nie udalo sie pobrac
            komiksu o zadanym numerze
    """

    # jezeli parametr comic jest rowny "random" to losujemy komiks
    # jezeli parametr comic jest rowny "new" to pobieramy najnowszy komiks
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

        # sprawdzenie czy ma byc pobrany komiks poprzedzajacy zadany indeks
        # czy nastepny, jezeli next_comic nie zostanie ustalone pobierany
        # jest komiks o wskazanym numerze
        if next_comic is True:
            comic_id += 1
        elif next_comic is False:
            comic_id -= 1

        # proba pobrania komiksu o zadanym numerze, jezeli podamy bledny numer
        # zwrocony zostaje komunikat o bledzie 404
        try:
            print "https://xkcd.com/{0}/z".format(comic_id)
            response = urllib2.urlopen(
                "https://xkcd.com/{0}/".format(comic_id))
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

    # sprawdzenie czy istnieje folder cache i ewentualne jego utworzenie
    if not os.path.exists(CACHE):
        os.mkdir(CACHE)

    # przeszukuje folder cache w poszukiwaniu komiksu o zadanym id
    # jezeli znajduje sie w nim to zwracam wynik
    # w przeciwnym razie pobieram nowy komiks
    if os.path.exists(CACHE + "{0}{1}".format(comic_id, img_type)):
        print "Obrazek znajduje sie juz w cache."
        return comic_id, img_type, title

    # pobranie komiksu i zapisanie w cache
    print "Pobieram obrazek: {0}".format(comic_id)

    f = open(CACHE + "{0}{1}".format(comic_id, img_type), "wb")
    f.write(urllib2.urlopen("http:" + src).read())
    f.close()

    return comic_id, img_type, title


class WindowXKCD(FloatLayout):
    """Klasa definiujaca okno aplikacji wyswietlajacej komiksy z XKCD."""

    def __init__(self, **kwargs):
        """Konstruktor klasy inicjalizuje przyciski oraz labele."""
        super(WindowXKCD, self).__init__(**kwargs)

        # label wyswietlajaca tekst "ID:"
        id_lbl = Label(text="ID:")

        # pole tekstowe, w ktorym wyswietlany jest numer (ID) aktualnie przegladanego komiksu
        # po wprowadzeniu do niego numeru wczytany zostaje komiks o zadanym ID
        self.id_txt_in = TextInput(
            multiline=False, on_text_validate=partial(self.set_comic, "this"))

        # przycisk po wcisniecium ktorego nastepuje pobranie najnowszego
        # komiksu
        new_btn = Button(text='Najnowszy', size_hint=(1, 0.9),
                         on_press=partial(self.set_comic, "new"))

        # przycisk po wcisniecium, ktorego nastepuje pobranie losowego komiksu
        random_btn = Button(text='Losowy', size_hint=(
            1, 0.9), on_press=partial(self.set_comic, "random"))

        # przycisk po wcisniecium, ktorego nastepuje pobranie poprzedniego
        # komiksu
        prev_btn = Button(text='Poprzedni', size_hint=(
            1, 0.9), on_press=partial(self.set_comic, "prev"))

        # przycisk po wcisniecium, ktorego nastepuje pobranie nastepnego
        # komiksu
        next_btn = Button(text='Nastepny', size_hint=(
            1, 0.9), on_press=partial(self.set_comic, "next"))

        # BoxLayout, przechowujacy menu aplikacji
        btn_box = BoxLayout(orientation='horizontal', size_hint=(0.6, 0.05))

        # dodanie elementow do layouty
        btn_box.add_widget(id_lbl)
        btn_box.add_widget(self.id_txt_in)
        btn_box.add_widget(prev_btn)
        btn_box.add_widget(new_btn)
        btn_box.add_widget(random_btn)
        btn_box.add_widget(next_btn)

        # dzieki temu layoutowi moge rozmiescic caly pasek z przyciskami w dowolnym
        # miejscu okna
        top_menu_anch = AnchorLayout(anchor_x='center', anchor_y='top')
        top_menu_anch.add_widget(btn_box)
        self.add_widget(top_menu_anch)

        # BoxLayout przechowujacy wyswietlany obrazek
        self.img_box = BoxLayout(orientation='vertical', size_hint=(1, 0.9))

        self.add_widget(self.img_box)

    def set_comic(self, *args):
        """Metoda odpowiedzialna jest za wczytanie i wyswietlenie zadanego komiksu."""

        # usuniecie z okna aktualnie wyswietlanego komiksu
        self.img_box.clear_widgets()

        # zmienna przechowujaca wynik dzialania funkcji get_comic
        result = ""
        result = ""
        # wywolanie funkcji pobierajacej komiks w zaleznosci od
        # podanego parametru this
        if args[0] == "this" and not self.id_txt_in.text == "":
            print int(self.id_txt_in.text)
            result = get_comic(self.id_txt_in.text)
            print result
        elif args[0] == "prev" and not self.id_txt_in.text == "":
            result = get_comic(self.id_txt_in.text, False)
        elif args[0] == "new":
            result = get_comic("new")
        elif args[0] == "random":
            result = get_comic()
        elif args[0] == "next" and not self.id_txt_in.text == "":
            result = get_comic(self.id_txt_in.text, True)

        # w zaleznosci od wyniku funkcji pobierajacej komiks:
        # wyswietlenie bledu
        # wyswietlenie pobranego komiksu
        if result == "":
            return
        elif result == "Error 404":
            self.img_box.add_widget(Label(
                text="[b]ERROR 404: Podales bledny numer komiksu lub nie masz polaczenie z siecia.[/b]", markup=True, size_hint=(1, 0.1)))
        else:
            # zmiana id wyswietlanego komiksu
            self.id_txt_in.clear_widgets()
            self.id_txt_in.text = str(result[0])

            # wyswietlenie tytulu komiksu
            self.img_box.add_widget(
                Label(text="[b]" + result[2] + "[/b]", markup=True, size_hint=(1, 0.1)))
            # wyswietlenie wczytanego komiksu
            self.img_box.add_widget(AsyncImage(
                source=CACHE + "{}{}".format(result[0], result[1])))


class MyJB(App):
    """Klasa obslugujaca aplikacje."""

    def build(self):
        """Metoda wywolywana za kazdym razem gdy okno zostaje tworzone."""
        parent = WindowXKCD()
        return parent


if __name__ in ('__main__', '__android__'):
    MyJB().run()
