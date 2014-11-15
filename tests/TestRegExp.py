#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys, os
sys.path.append("../")

from nose import with_setup

from tools.normalization import Normalizer
from tools.regexp import RegExp

normalizer = Normalizer()
regexp = RegExp(normalizer)
matrix = regexp.matrices

def test_primary_source_matcher():
	print ("Testing Primary Source Matcher")
	texts = [
		"Ter. Andr. 868",
		"Liv. 21, 5, 9."
	]
	for text in texts:
		assert matrix["primarySource"]["matcher"].match(text) != None


def test_secondary_source_matcher():
	print ("Testing Secondary Source Matcher")
	texts = [
		"Alulu zu Cic. Quint. II. 3.",
		"Wölfflin im Philol. 34, 114.",
		"s. Fabri Liv. 21, 5, 9."
	]
	for text in texts:
		assert matrix["secondarySource"]["matcher"].match(text) != None, "Regular Expression not working for {0}".format(text)

def test_greek():
	assert matrix["greek"]["matcher"].match("Ελληνική Κοινότητα Προγραμματιστών") != None