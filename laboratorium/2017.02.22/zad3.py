# suma cyfr liczby 100!
# jak sie uda to w 1 linii
# stworzyłem potwora!
print sum(map(int, str(reduce(lambda x, y: x*y, range(2, 100)))))