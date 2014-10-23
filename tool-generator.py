#!/usr/bin/python3
# -*- coding: UTF-8 -*-

abkurzung = []
with open("input/abkurzung.txt") as f:
	#In this document, we have one line = one word definition, h1 represent orth
	for line in f.readlines():
		ab = line.split(" – ")[0]
		abkurzung.append(ab)
	f.close()

with open("output/grammatik-abkurzung.csv", "r") as f:
	lines = f.readline()
	abkurzung = set(abkurzung + lines.split(";"))
	f.close()

with open("output/grammatik-abkurzung.csv", "w") as f:
	f.write(";".join([ab for ab in abkurzung if len(ab) > 0]))
	f.close()