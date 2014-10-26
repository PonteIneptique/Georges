#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import nltk
import codecs
import difflib
import jellyfish
from fuzzywuzzy import process
import re

latinstopwords = ["de", "in"]
replacer = re.compile("|".join(latinstopwords))

def getDictionary(filename = "../output/werken.csv", splitter = "\t"):
	with codecs.open(filename ,"r") as csv:
		lines = [line.replace("\n", "") for line in csv.readlines()]
		werken = {}
		lines = [line.split(splitter) for line in lines if splitter in line]
		for line in lines: 
			author = line[0]
			if author not in werken:
				werken[author] = []
			werken[author].append(line[1])
		csv.close()
	return werken

def getClose(books, score = 70):
	#Books is a list of books title we need to merge
	#We want to return a tuples with possible matches (booktitle, listofmatches)
	results = []
	for book in books:
		index = [b for b in books if book != b]

		cleanStrings = [replacer.sub("", b) for b in books if book != b]
		cleanString = book

		matches = process.extract(cleanString, cleanStrings) #We get matches through process 
		#It returns a list of tuple(string, score)
		matches = [match[0] for match in matches if match[1] > score]
		matches = [index[cleanStrings.index(match)] for match in matches]
		results.append([book,  matches])
	return results

werken = getDictionary()

#Testing output
output = {}

for author in werken:
	output[author] = getClose(werken[author])

export = {}
for author in output:
	known = []
	export[author] = {}
	for book in output[author]:
		if book[0] not in known:
			known.append(book[0])

			export[author][book[0]] = []
			for synonym in book[1]:
				if synonym not in known:
					export[author][book[0]].append(synonym)
					known.append(synonym)

import pickle
with open("werken.pickle", "wb") as f:
	pickle.dump(export, f)
	f.close()