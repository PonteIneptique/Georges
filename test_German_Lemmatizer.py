#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from langdetect import detect_langs

texts = [
	"vor Zahlen, Jahresbezeichnung, lascivus est superbus",
	"vor Zahlen, Jahresbezeichnung (= Annus) auf Grabschriften usw.",
	"aber auch der Verwünschung, Komik., Verg., Poët. eleg., Ov. u.a. Dichter. ",
	"exercitus hostium duo, unus ab urbe, alter a Gallia obstant"
]

text = ".".join(texts)

for text in texts:
	print (text)

	print (detect_langs(text))