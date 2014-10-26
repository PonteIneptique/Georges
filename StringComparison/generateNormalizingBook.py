#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from pprint import pprint
import pickle

werken = pickle.load( open( "werken.pickle", "rb" ) ) 

lines = []
for author in werken:
	books = werken[author]
	for book in books:
		for b in books[book]:
			l = [author, b, author, book]
			lines.append("\t".join(l))

general = lines
#Writing the automatic one
with open("../dictionary/automatic-normalizing-book.csv", "w") as f:
	f.write("\n".join(lines))
	f.close()

#Reading manual one
with open("../dictionary/manual-normalizing-book.csv") as f:
	general = general + [line.replace("\n", "") for line in f.readlines()]
	f.close()

#Generation General one
with open("../dictionary/normalizing-book.csv", "w") as f:
	f.write("\n".join(general))
	f.close()