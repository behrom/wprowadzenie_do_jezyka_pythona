#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

# TO DO:
# poprawa komentarzy
# wyslac

from __future__ import division

# postanowilem wczytac dane z plikow do slownika
# dzieki czemu bylo mi latwiej manipulowac danymi
# rozwiazanie to jednak nie pozwala na przetwarzanie
# nieograniczonej liczby studentow lub nieograniczonej
# liczby wypozyczonych ksiazek przez studenta
# powodem jest ograniczony rozmiar pamieci operacyjnej

# slownik przechowuje dane o osobach
# kluczem jest pesel poniewaz pesel jest wartoscia unikatowa
# a wartosciami sa dane bedace lista, ktora zawiera:
#   pozycja 0: imie
#   pozycja 1: nazwisko
#   pozycja 2: nr pokoju w akademiku lub -1 jezeli brak
#   pozycja 3: liste ksiazek
dane = {}

# wczytanie danych z pliku studentci.txt
# do slownika
with open('studenci.txt', 'r') as plik:
    # pominiecie naglowka
    plik.readline()

    # wczytanie danych z pliku i zapisanie ich do slownika
    for linia in plik:
        lin = linia.rstrip("\n").split("\t")

        # zapis imienia i nazwiska do slownika
        # pod klucz - pesel
        dane[lin[0]] = [lin[2], lin[1]]

# wczytanie danych z pliku studentci.txt
with open('meldunek.txt', 'r') as plik:
    # pominiecie naglowka
    plik.readline()

    # wczytanie danych z pliku i zapisanie ich do slownika
    for linia in plik:
        lin = linia.rstrip("\n").split("\t")

        # odczyt ze slownika imienia i nazwiska
        tmp = dane.get(lin[0])

        # dodanie numeru pokoju
        tmp.append(lin[1])

        # zapisanie do slownika zaktualizowanych danych
        dane[lin[0]] = tmp

# poniewaz nie wszystkie osoby mieszkaja w akademiku
# a wiem, ze w slowniku co najmniej znajduje sie imie i nazwisko
# dodaje do slownika w polu "pokoj" (3 indeks na liscie wartosci slownika)
#  wartosc -1
for item in dane.items():
    if len(item[1]) < 3:
        tmp = dane.get(item[0])
        tmp.append(-1)

        dane[item[0]] = tmp

# wczytanie danych z pliku wypozyczenia.txt
with open('wypozyczenia.txt', 'r') as plik:
    # pominiecie naglowka
    plik.readline()

    # wstawienie pustej listy do danych
    for item in dane.items():
        # dodanie pustej listy na koncu danych
        item[1].append([])

        # aktualizacja slownika
        dane[item[0]] = item[1]

    # wczytanie danych z pliku i zapisanie ich do slownika
    for linia in plik:
        lin = linia.rstrip("\n").split("\t")

        # odczyt ze slownika imienia i nazwiska
        tmp = dane.get(lin[1])

        # dopisanie tytulu ksiazki do listy ksiazek w slowniku
        tmp[3].append(lin[2])

        dane[lin[1]] = tmp


def ppkt_1(dane):
    """Funkcja odpowiadajaca na pytanie z podpunktu 1."""

    print "Odpowiedz na podpunkt 1:"

    # lista w postaci
    # pesel - ilosc wypozyczonych ksiazek
    odpowiedz = [-1, -1]

    # iteruje po wszystkich osobach
    # i zapisuje dane osoby ktora wypozyczyla
    # najwiecej ksiazek
    for pesel, dane_osoby in dane.items():
        if odpowiedz[1] < len(dane_osoby[3]):
            odpowiedz = [pesel,
                         len(dane_osoby[3])]

    print "\tNajwiecej ksiazek wypozyczyl(a): {} {}\n".format(
        dane.get(odpowiedz[0])[0],
        dane.get(odpowiedz[0])[1]
    )

    print "\tTytuly jakie wypozyczyl(a) to:"

    for tytul in dane.get(odpowiedz[0])[3]:
        print "\t\t", tytul


def ppkt_2(dane):
    """Funkcja odpowiadajaca na pytanie z podpunktu 2."""

    print "\nOdpowiedz do podpunktu 2:"

    # slownik przechowujacy:
    # klucz     - numer pokoju
    # wartosc   - liczba osob na pokoju
    pokoj = {}

    for pesel, dane_osoby in dane.items():
        # zapamietuje wczesniejsza liczbe osob na pokoju
        ile_osob = pokoj.get(dane_osoby[2], 0)

        # zwiekszam liczbe osob na pokoju o 1 nowo zaneziona
        ile_osob += 1

        # zapamietuje nowa liczbe osob na pokoju
        pokoj[dane_osoby[2]] = ile_osob

    # usuwam ze slownika osoby ktore nie mieszakaja w akademiku
    del pokoj[-1]

    # wyliczam srednia liczbe osob na pokoju ze wzoru
    # suma liczby osob na pokoju / liczbe pokoi
    # i wyswietlam odpowiedz
    print "\tSrednia liczba osob "\
        "zameldowanych w jednym pokoju wynosi: {:.4f}".format(
            sum(pokoj.values()) / len(pokoj))


def ppkt_3(dane):
    """Funkcja odpowiadajaca na pytanie z podpunktu 3."""

    print "\nOdpowiedz do podpunktu 3:"
    # zmienna przechowujaca ilosc mezczyzn
    mezczyzn = 0

    # zmienna przechowujaca ilosc kobiet
    kobiet = 0

    # dla kazdego peselu - klucza ze slownika
    # sprawdzam czy przedostatnia cyfra jest parzysta
    # i odpowiednio zwiekszam zmienne
    for pesel in dane.keys():
        if int(pesel[9]) % 2:
            mezczyzn += 1
        else:
            kobiet += 1

    # wyswietlam wyniki
    print "\tLiczba kobiet wsrod studentow wynosi:\t", kobiet
    print "\tLiczba mezczyzn wsrod studentow wynosi:\t", mezczyzn


def ppkt_4(dane):
    """Funkcja odpowiadajaca na pytanie z podpunktu 4."""

    print "\nOdpowiedz do podpunktu 4:"

    # lista zwierajaca imiona i nazwiska osob
    # nie mieszakajacych na pokoju
    osoby_z_poza_akademika = []

    # dla kazdej osoby sprawdzam numer pokoju
    # w ktorym mieszka wynosi -1
    # jezeli tak to wiem, ze ta osoba nie mieszka w akademiku
    # wiec zapisuje do listy jej imie i nazwisko
    for dane_osoby in dane.values():
        if dane_osoby[2] == -1:
            osoby_z_poza_akademika.append([dane_osoby[1],
                                           dane_osoby[0]])

    # posortowanie listy osob z poza akademika
    # wzgledem nazwiska (indeks 0)
    osoby_z_poza_akademika.sort(key=lambda x: x[0])

    # wyswietlenie odpowiedzi
    print "\tOsoby z poza akademika:"

    for osoba in osoby_z_poza_akademika:
        print "\t\t{} {}".format(osoba[0],
                                 osoba[1])


def ppkt_5(dane):
    """Funkcja odpowiadajaca na pytanie z podpunktu 5."""

    print "\nOdpowiedz do podpunktu 5:"

    # slownik ktory przechowuje:
    # klucz     - numer pokoju
    # wartosci  - lista ksiazek jaka jest wypozyczona przez
    #             wszystkich studentow na pokoju
    pokoj = {}

    for osoba in dane.values():
        # zapamietuje aktualna liste ksiazek wypozyczonych
        # przez studentow z danego pokoju
        tmp = pokoj.get(osoba[2], [])

        # dodaje do listy ksiazek
        # ksiazki aktualnie przetwarzanego studenta
        for os in osoba[3]:
            tmp.append(os)

        # usuwam z listy powtorzenia
        # zgodnie z wprowadzonym ograniczeniem
        # 1 egzemplarza ksiazki na pokoj
        tmp = list(set(tmp))

        # zapamietuje liste ksiazek wypozyczonych na pokoj
        pokoj[osoba[2]] = tmp

    # wyswietlam odpowiedz do podpunktu
    print "\tGdyby obowiazywalo ograniczenie 1 egzemplarza ksiazki na pokoj"
    print "\tto wypozyczonych ksiazek byloby: ", sum(len(ks) for ks in pokoj.values())


# wyswietlenie odpowiedzi do podpunktow z zadania
ppkt_1(dane)
ppkt_2(dane)
ppkt_3(dane)
ppkt_4(dane)
ppkt_5(dane)
