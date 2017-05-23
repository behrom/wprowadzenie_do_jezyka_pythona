#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Trojkat:
	"""Klasa reprezentujaca jeden trojkat."""
	def podziel(self):
		def punkt_podzialu(p1,p2):
			return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]

		q1 = punkt_podzialu(self.p1, self.p2)
		q2 = punkt_podzialu(self.p1, self.p3)
		q3 = punkt_podzialu(self.p2, self.p3)

		return [Trojkat(self.p1, q1, q2),
			 Trojkat(q1, self.p2, q3),
			 Trojkat(q2, q3, self.p3)]

	def __init__(self, punkt1, punkt2, punkt3):
		self.p1 = punkt1
		self.p2 = punkt2
		self.p3 = punkt3

	def __str__(self):
		return (r'<polygon points="{},{} {},{} {},{}"'
				' style="fill:black;"/>').format(
				  self.p1[0], self.p1[1],
				  self.p2[0], self.p2[1],
				  self.p3[0], self.p3[1])
	
def list_to_svg(trojkaty):
	res = '''<svg height="100" width="100">'''
	res += "\n".join([str(t) for t in trojkaty])
	return res + '\n</svg>'


trojkaty = [Trojkat([0.0, 0.0], [50.0, 100.0],
                    [100.0, 0.0])]

wielkosc = 4
for i in range(wielkosc):
	nowe = []
	
	for t in trojkaty:
	   nowe += t.podziel()
	   
	trojkaty = nowe
	
with open('trojkaty.svg', 'w') as file:
	file.write(list_to_svg(trojkaty))
