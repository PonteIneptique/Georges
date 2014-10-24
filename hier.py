#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

tests = [
	["I" , "a", "b", "1", "2", "3", "II", "a", "1" , "b", "c"],
	["A" , "1", "a", "b", "2", "3", "4", "a", "b" , "B", "1", "A"]
]

def defineLevelRegExp(text):
	availableRegExp = ["[a-z]+", "[IVX]+", "[0-9]+", "[ABCDEFGH]+"]
	for regexp in availableRegExp:
		r = re.compile(regexp)
		if r.match(text):
			return regexp
	return "FAULTY"


def getLevel(text, dictionary):
	regexp = defineLevelRegExp(text)
	if regexp not in dictionary:
		dictionary[regexp] = len(dictionary) + 1

	return dictionary[regexp], dictionary

for levels in tests:
	levelRegExp = {}
	for level in levels:
		text, levelRegExp = getLevel(level, levelRegExp)
	print levelRegExp