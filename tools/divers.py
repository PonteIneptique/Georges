import xml.etree.cElementTree as cElementTree
from xml.dom import minidom

import regex as re


def prettify(elem):
	""" Return a pretty-printed XML string for the Element. """
	rough_string = cElementTree.tostring(elem, 'unicode')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="\t")

def polishH1(text):
	if text[-1:] == ",":
		text = text[0:-1]
	return text

def polishSenses(text):
	text = re.sub("<[\/]{0,1}[A-Za-z0-9]+>", "", text)
	text = re.sub("[\s]{2,}", " ", text)
	return text

def divideText(text, index):
	text = polishSenses(text)
	regexp = re.compile("^([\w]+)(?:[,\.]{0,1})(.*)$", flags= re.UNICODE)
	match = regexp.match(text)
	try:
		return match.group(1), match.group(2)
	except:
		raise ValueError("No H1 for line {0}".format(index))


def defineLevelRegExp(text):
	availableRegExp = ["[a-z]+", "[IVX]+", "[0-9]+", "[ABCDEFGH]+", "[αβγδ]+"]
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
