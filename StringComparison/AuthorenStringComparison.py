#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import nltk
import codecs
import difflib
import jellyfish

with codecs.open("../output/authoren.csv" ,"r") as csv:
	authoren = [line.replace("\n", "").replace(".", "").replace(" ", "") for line in csv.readlines()]
	csv.close()


def jellyfishPhonetic(author, authoren, fn, stringFn = None):
	author = (author, fn(author))
	authoren = [(a, fn(a)) for a in authoren if a != author[0]]
	if not stringFn:
		return [a[0] for a in authoren if a[1] == author[1]]


def jellyfishAlgo(author, authoren, fn, multiplicater = 1, reverse = False, maximum = 2, limit = False):
	jelly = [(int (fn(author, a) * multiplicater), a) for a in authoren if a != author]
	jelly = sorted(jelly, reverse = reverse)[0:maximum]
	if limit:
		return [a[1] for a in jelly if a[0] > limit]
	return [a[1] for a in jelly]

def close(a, b):
	return list(set(a) & set(b))

sourceauthoren = authoren#[0:100]
for author in sourceauthoren:
	matches = jellyfishPhonetic(author, authoren, jellyfish.match_rating_codex)
	nysiis = jellyfishPhonetic(author, authoren, jellyfish.soundex)

	matches = close(matches, nysiis)

	jaro = jellyfishAlgo(author, authoren, jellyfish.jaro_distance, 10000, reverse = True, maximum = 3, limit = 8300)
	matches = close(matches, jaro)


	if(len(matches) > 0):
		print ([author, matches])

