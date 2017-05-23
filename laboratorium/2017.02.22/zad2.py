# Zadanie 2
#
# Napisz dwa programy (wykorzystujace petle):
# * program pobiera od uzytkownika nieujemna liczbe calkowita n i oblicza
#   sume kwadratow liczb od 0 do n, czyli wartosci:
#   0^2 + 1^2 + 2^2 + ... + n^2
#
# * program pobiera od uzytkownika dwie dodatkie liczby calkowite
#   n oraz m i wypisuje w kolejnych wierszach wszystkie dodatkie
#   wielokrotnosci n mniejsze od m


def program1():
    n = raw_input("Podaj n: ")

    # suma = 0
    #
    # for i in xrange(int(n)):
    #     suma += i ** 2
    #
    # print suma

    # da sie w jednej linijce xD
    print sum([i**2 for i in xrange(int(n))])

def program2():
    n = raw_input("Podaj n: ")
    n = int(n)

    m = raw_input("Podaj m: ")
    m = int(m)

    i = 0
    while n*i < m:
        print i, n*i
        i += 1

# program1()
program2()