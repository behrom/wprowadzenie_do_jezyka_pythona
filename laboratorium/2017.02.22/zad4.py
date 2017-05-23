# oblicz roznice miedzy kwadratem sumy a roznica kwadratow
# 100 liczb natururalnych

def wynik(n):
    return sum(range(1, n+1))**2 - sum(x**2 for x in range(1, n + 1))

print wynik(100)