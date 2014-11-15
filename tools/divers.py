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

def GrammatikAbkurzung():
	abkurzung = []
	with open("output/grammatik-abkurzung.csv", "r") as f:

		lines = f.readline()
		abkurzung = lines.split(";")
		f.close()
	return abkurzung


def getListFromDictRegExp(items, groupName, max):
	i = 1
	ret = []
	while i <= max:
		key = "{0}{1}".format(groupName, i)
		if items[key]:
			ret.append(items[key])
		i += 1

	if len(ret) == 0:
		return None
	return ret

def firstLine(text, node):
	#<itype>a, um</itype>, = <foreign lang="greek">u)bu(skantos</foreign> Maybe some sense here
	abkurzung = "|".join(GrammatikAbkurzung()).replace(".", "\\.")
	regexp = "^(?:\s{0,1}(?P<itype1>[\w]+)[,\s]){0,1}(?:\s{0,1}(?P<itype2>[\w]+)[,\s]){0,1}(?:\s{0,1}(?P<itype3>[\w]+)[,\s]){0,1}(?:\s{0,1}(?P<itype4>[\w]+)[,\s]){0,1}(?:\s(?P<gen>" + abkurzung + "+)){0,1}(?:\s*\((?P<etym1>[\w\s]+)\)){0,1}(?:\s*=\s*(?P<etym2>[\w\s]+)){0,1}(?P<rest>.*)"
	regexp = re.compile(regexp, flags = re.UNICODE)
	matches = [m.groupdict() for m in regexp.finditer(text)][0]

	#We join the itype
	itype = getListFromDictRegExp(matches, "itype", 4)

	#We then set the gen
	gen = matches["gen"]

	#We set the etym
	etym = getListFromDictRegExp(matches, "etym", 2)

	#We set the rest
	rest = matches["rest"]

	#Now we create the nodes

	if itype:
		iTypeNode = cElementTree.SubElement(node, "itype")
		iTypeNode.text = ", ".join(itype)

	if gen:
		iTypeNode = cElementTree.SubElement(node, "gen")
		iTypeNode.text = gen

	if etym:
		for e in etym:
			eNode = cElementTree.SubElement(node, "etym")
			eNode.text = e
	return rest


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
