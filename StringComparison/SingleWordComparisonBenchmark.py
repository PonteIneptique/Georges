#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import nltk
import codecs
import difflib
import jellyfish

with codecs.open("../output/authoren.csv" ,"r") as csv:
	authoren = [line.replace("\n", "").replace(".", "").replace(" ", "") for line in csv.readlines()]
	csv.close()



def jellyfishAlgo(author, authoren, fn, multiplicater = 1, reverse = False, maximum = 5):
	jelly = [(int (fn(author, a) * multiplicater), a) for a in authoren]
	return sorted(jelly, reverse = reverse)[0:maximum]

def jellyfishPhonetic(author, authoren, fn, stringFn = None):
	author = (author, fn(author))
	authoren = [(a, fn(a)) for a in authoren]
	if not stringFn:
		return [a[0] for a in authoren if a[1] == author[1]]

i = 0
#Test for Virgil
testauthoren = ["Virg", "Apol"]
sourceauthoren = authoren
for author in testauthoren:
	authoren = [a for a in sourceauthoren if a != author]

	print "Test for {0}".format(author)

	print "" ########################################################################

	print "difflib close match"
	print difflib.get_close_matches(author, authoren)

	print "" ########################################################################

	print "levenshtein_distance"
	levenshtein_distance = jellyfishAlgo(author, authoren, jellyfish.levenshtein_distance)
	print levenshtein_distance

	print "" ########################################################################

	print "jaro"
	jaro = jellyfishAlgo(author, authoren, jellyfish.jaro_distance, 10000, reverse = True)
	print jaro

	print "" ########################################################################

	print "jaroWinkler"
	jaro = jellyfishAlgo(author, authoren, jellyfish.jaro_winkler, 10000, reverse = True)
	print jaro

	print "" ########################################################################

	print "damerau_levenshtein_distance"
	damerau_levenshtein_distance = jellyfishAlgo(author, authoren, jellyfish.damerau_levenshtein_distance)
	print damerau_levenshtein_distance

	print "" ########################################################################

	print "hamming_distance"
	hamming_distance = jellyfishAlgo(author, authoren, jellyfish.hamming_distance)
	print hamming_distance

	print "" ########################################################################
	print "#########################################################################"
	print "PHONETIC COMPARISON"
	print "" ########################################################################

	print "Metaphone equality"
	meta = jellyfishPhonetic(author, authoren, jellyfish.metaphone)
	print meta

	print "" ########################################################################

	print "Soundex equality"
	soundex = jellyfishPhonetic(author, authoren, jellyfish.soundex)
	print soundex

	print "" #######################################################################

	print "nysiis equality"
	nysiis = jellyfishPhonetic(author, authoren, jellyfish.nysiis)
	print nysiis

	print "" #######################################################################

	print "match_rating_codex"
	match_rating_codex = jellyfishPhonetic(author, authoren, jellyfish.match_rating_codex)
	print match_rating_codex