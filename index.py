#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import codecs
import xml.etree.cElementTree as cElementTree
import xml.etree.ElementTree as ElementTree
import regex as re
from xml.dom import minidom
import copy

#Registering werk and autoren abkurzungen
authoren = []
werken = []
TextIdentifiers = []


#Configuration
i = 0
limit = 100 #For the sample
break_on_sample = True
ignoreReplacer = False #Ignore the merger for Werken

#########################################################
#
#
#	Normalizing functions
#
#########################################################

def booksdictionary():
	dic = {}
	with open("dictionary/normalizing-book.csv") as f:
		lines = [line.replace("\n", "") for line in f.readlines()]
		f.close()

	for line in lines:
		l = line.split("\t")
		author1 = l[0]
		book1 = l[1]
		author2 = l[2]
		book2 = l[3]
		if author1 not in dic:
			dic[author1] = {}
		dic[author1][book1] = (author2, book2)
	return dic

def authordictionary():
	dic = {}
	with open("dictionary/author-synonyms.csv") as f:
		lines = [line.replace("\n", "") for line in f.readlines()]
		f.close()

	for line in lines:
		l = line.split("\t")
		author1 = l[0]
		author2 = l[1]
		if author1 not in dic:
			dic[author1] = {}
		dic[author1] = author2
	return dic


def getAuthorRegExp(simple = False):
	output = []
	with open("./dictionary/authors.csv") as f:
		output = ["(?:{0})".format(line.replace("\n", "").replace(" ", "\s").replace(".", "\.")) for line in f.readlines()]
		f.close()

	if not simple:
		output = output# + ["(?:(?:[A-Z]{1}[a-z]+)(?:\szu\s)(?:Ps.\s){0,1}[A-Z]{1}[a-z]+\.)"]

	return "|".join(output)

def getBooksRegexp():
	lines = []
	with open("./dictionary/books.csv") as f:
		lines = ["(?:{0})".format(line.replace("\n", "").replace(" ", "\s").replace(".", "\.").split("\t")[1]) for line in f.readlines()]
		f.close()

	output = lines + ["(?:(?:in|ex|de|ad){1}[\s]{1}){0,1}(?:[^\W\d]{2,}\.(?:[\s])*)+)"]
	return "|".join(output)


#########################################################
#
#
#	Normalizing Variables
#
#########################################################

ReplacementBookDictionary = booksdictionary()
ReplacementAuthorDictionary = authordictionary()
AuthorRegExp = getAuthorRegExp()
BooksRegExp = getBooksRegexp()
AuthorSimpleRegexp = getAuthorRegExp(True)

#########################################################
#
#
#	Reg EXP Generator
#
#
#########################################################

def opusRegExp(opusfinder = False):
	paragraphCharacters = "(?:[p\§]{1}\.{0,1}\s){0,1}"
	authorRegExp = AuthorRegExp
	regexp = "(?P<author>" + authorRegExp + "){1}(?:\s(?P<opus>" + BooksRegExp + "+){0,1}(?:\s(?P<identifier1>" + paragraphCharacters + "[0-9]+\,)){0,1}(?:\s(?P<identifier2>" + paragraphCharacters +  "[0-9]+\,)){0,1}(?:\s(?P<identifier3>" + paragraphCharacters + "[0-9]+\,)){0,1}(?:\s(?P<identifier4>" + paragraphCharacters + "[0-9]+[\.:]{0,1})){1}"
	if opusfinder:
		#sub
		return re.sub("P<[a-zA-Z0-9]+>", ":", regexp)
	else:
		return regexp

def QuotationRegExp(finder = False):
	# "(?:[:;\s\)\,]+)" + 
	regexp = "(?P<text>[a-zA-Z ]+)\,[\s]*(?P<author>"+ AuthorSimpleRegexp + "){1}"
	if finder:
		return re.sub("P<[a-zA-Z0-9]+>", ":", regexp)
	return regexp

##########################################################
#
#
#	RegExp Compiled
#
#
##########################################################
OpusRegExp = {
		"Finder" : re.compile("(?P<match>{0})".format(opusRegExp(True))),
		"Groups" : re.compile(opusRegExp())
	}

SecondarySource = {
	"Finder" : re.compile("(?P<match>(?:[A-Z]{1}[a-z]+)(?:\szu\s)(?:Ps.\s){0,1}[A-Z]{1}[a-z]+\.)"),
	"Groups" : re.compile("(?P<SecondaryAuthor>[A-Z]{1}[a-z]+)(?:\szu\s)(?P<PrimaryAuthor>(?:Ps.\s){0,1}[A-Z]{1}[a-z]+\.)")
}

ol_match = re.compile("^([1-9]{1,3}|[abcdefABCDEF]{1}|IX|IV|V?I{0,3})$")
GreekChar = re.compile("((?:(?:[\p{Greek}µ']+)+[\s\.\,]*)+)")

Quotation = {
	"Finder" : re.compile("(?P<match>{0})".format(QuotationRegExp(True))),
	"Groups" : re.compile(QuotationRegExp())
}


def replaceAuthor(author):
	if author in ReplacementAuthorDictionary:
		return ReplacementAuthorDictionary[author]
	return author

def replaceAuthorBook(author, book):
	if author in ReplacementBookDictionary and book in ReplacementBookDictionary[author]:
		t = ReplacementBookDictionary[author][book]
		return t[0], t[1]
	return author, book

def prettify(elem):
	"""Return a pretty-printed XML string for the Element.
	"""
	rough_string = cElementTree.tostring(elem, 'unicode')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="\t")

def polishH1(text):
	if text[-1:] == ",":
		text = text[0:-1]
	return text

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

def GrammatikAbkurzung():
	abkurzung = []
	with open("output/grammatik-abkurzung.csv", "r") as f:

		lines = f.readline()
		abkurzung = lines.split(";")
		f.close()
	return abkurzung

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

def greek(text, node):
	lang = cElementTree.SubElement(node, "lang")
	lang.set("lang", "greek")
	lang.text = text
	return lang

def greekFinder(text, node):
	splitter = GreekChar
	caught = splitter.split(text)

	initialText = None
	lastNode = None
	for element in caught:
		if element:
			if not initialText:
				if splitter.match(element):
					#We must create a node with opus informations
					lastNode = greek(element, node)
					initialText = True
				else:
					node.text = element
					initialText = True
			else:
				if splitter.match(element):
					lastNode = greek(element, node)
				else:
					lastNode.tail = element
	return lastNode

def opus(text, node):
	#<bibl><author>Sen.</author> <title>Q. N.</title> 4, 2, 7</bibl>
	regexp = OpusRegExp["Groups"]
	items = [m.groupdict() for m in regexp.finditer(text)][0]

	author = items["author"]
	author = replaceAuthor(author)

	title = items["opus"]
	identifier = getListFromDictRegExp(items, "identifier", 4)

	bibl = cElementTree.SubElement(node, "bibl")

	aNode = cElementTree.SubElement(bibl, "author")
	lastNode = aNode

	authoren.append(author)

	if title:
		tNode = cElementTree.SubElement(bibl, "title")
		lastNode = tNode

	if author and title:
		if not ignoreReplacer:
			author, title = replaceAuthorBook(author, title)
		werken.append("{0}\t{1}".format(author, title))

	aNode.text = author
	if title :
		tNode.text = title
	else:
		title = ""

	if identifier:
		lastNode.tail = " ".join(identifier)
		TextIdentifiers.append("{0}\t{1}\t{2}".format(author, title, identifier))

	return bibl #Return the last node in usage

def quotationMarker(text, node):
	regexp = Quotation["Groups"]
	items = [m.groupdict() for m in regexp.finditer(text)][0]

	author = items["author"]
	author = replaceAuthor(author)

	text = items["text"]

	bibl = cElementTree.SubElement(node, "quote")
	bibl.text = text

	aNode = cElementTree.SubElement(bibl, "author")
	aNode.text = author


	return bibl

def quotationFinder(text, node):
	splitter = Quotation["Finder"]
	caught = splitter.split(text)
	initialText = None
	lastNode = node

	for element in caught:
		if element:
			if not initialText:
				if splitter.match(element):
					#We must create a node with opus informations
					lastNode = quotationMarker(element, node)
					initialText = True
				else:
					lastNode = opusFinder(element, node)
					initialText = True
			else:
				if splitter.match(element):
					lastNode = quotationMarker(element, node)
				else:
					lastNode = opusFinder(element, node)

def opusFinder(text, node):
	splitter = OpusRegExp["Finder"]

	caught = splitter.split(text)

	initialText = None
	lastNode = node
	for element in caught:
		if element:
			if not initialText:
				if splitter.match(element):
					#We must create a node with opus informations
					lastNode = opus(element, node)
					initialText = True
				else:
					lastNode = greekFinder(element, node)
					initialText = True
			else:
				if splitter.match(element):
					lastNode = opus(element, node)
				else:
					lastNode = greekFinder(element, node)


def secondarySource(text, node):
	regexp = SecondarySource["Groups"]

	items = [m.groupdict() for m in regexp.finditer(text)][0]

	PrimaryAuthor = items["PrimaryAuthor"]
	PrimaryAuthor = replaceAuthor(PrimaryAuthor)

	SecondaryAuthor = items["SecondaryAuthor"]

	SecBiblNode = cElementTree.SubElement(node, "bibl")

	SecAuthorNode = cElementTree.SubElement(SecBiblNode, "author")
	SecAuthorNode.text = SecondaryAuthor

	#The should be a loop there at some point
	PrimBiblNode = cElementTree.SubElement(SecBiblNode, "bibl")
	PrimaryAuthorNode = cElementTree.SubElement(PrimBiblNode, "author")
	PrimaryAuthorNode.text = PrimaryAuthor

	return SecBiblNode #Return the last node in usage


def SecondarySourceFinder(text, node):
	splitter = SecondarySource["Finder"]

	caught = splitter.split(text)

	initialText = None
	lastNode = node
	for element in caught:
		if element:
			if not initialText:
				if splitter.match(element):
					#We must create a node with opus informations
					lastNode = secondarySource(element, node)
					initialText = True
				else:
					lastNode = opusFinder(element, node)
					initialText = True
			else:
				if splitter.match(element):
					lastNode = secondarySource(element, node)
				else:
					lastNode = opusFinder(element, node)

	return lastNode

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
	availableRegExp = ["[a-z]+", "[IVX]+", "[0-9]+", "[ABCDEFGH]+", "[αβ]+"]
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


"""
	TEI Structure
	<text>
		<body>
			<pb n="1"/>
			<cb n="A"/>
			<div0 type="alphabetic letter" n="A">
				<head lang="la">A</head>
"""
root = cElementTree.Element("text")
body = cElementTree.SubElement(root, "body")

div = {}
head = {}
with open("input/body.xml") as f:

	char = None
	#In this document, we have one line = one word definition, h1 represent orth
	for line in f.readlines():

		#We split the line around the <h1> tag
		h1, senses_text = divideText(line, i)
		h1 = polishH1(h1)
		senses_text = polishSenses(senses_text)

		if h1[0] != char:
			char = h1
			div[char] = cElementTree.SubElement(body, "div0")
			div[char].set("type", "alphabetic letter")
			div[char].set("n", char.upper())

			head[char] = cElementTree.SubElement(div[char], "head")
			head[char].set("lang", "la")


		#We create a node for this element
		entryFree = cElementTree.SubElement(div[char], "entryFree")
		entryFree.set("n", str(i))

		#We set a orth node according to the content in h1
		orth = cElementTree.SubElement(entryFree, "orth")
		orth.set("key", h1)
		orth.text = h1

		#Now we get to the senses : 
		# - we set up a list where we'll store our new nodes
		# - we split up our senses part so we can find each level of definition
		# - we set up an index counter
		# - we reset id to None. id is the key for the numeric identifier of the sense
		senses = []
		senses_text_split = re.split('[–\,]{0,1}\s([1-9]{1,3}|[abcdefABCDEFαβ]{1}|IX|IV|V?I{0,3})\)\s', senses_text)

		if len(senses_text_split) == 1:

			#We check for itype, etym, gen...
			text = firstLine(senses_text, entryFree)


			#When a sense has no number before it
			senses.append(cElementTree.SubElement(entryFree, "sense"))
			SecondarySourceFinder(text, senses[len(senses) - 1 ])
		else:
			index_sense = 1
			id = None
			levelN = 1

			levelDictionary = {}

			#We make a loop around our data
			for index_sense in range(1, len(senses_text_split)):


				#The text correspond to our element in senses_text_split with index (index_sense - 1)
				text = senses_text_split[index_sense - 1]
				#We match it against our simple numeric matcher
				matching = ol_match.match(text)

				#If this doesn't match, we have a sense's text
				#If this match, we have a numeric identifier : we set id to it
				if not matching:
					#id was set on previous iteration, we set n attribute to it
					if id:
						senses.append(cElementTree.SubElement(entryFree, "sense"))
						senses[len(senses) - 1 ].set("n", id)
						senses[len(senses) - 1 ].set("level", str(levelN))
						opusFinder(text, senses[len(senses) - 1 ])
					else: #We dont have text
						text = firstLine(text, entryFree)
						senses.append(cElementTree.SubElement(entryFree, "sense"))
						opusFinder(text, senses[len(senses) - 1 ])
				else:
					id = text
					levelN, levelDictionary = getLevel(id, levelDictionary)

		if i == limit:
			with open("output/sample.xml", "w") as f:
				f.write(prettify(copy.deepcopy(root)))
				f.close()
			if break_on_sample:
				break
		i += 1 

if not break_on_sample:
	with open("output/output.xml", "w") as f:
		f.write(cElementTree.tostring(root, 'unicode'))
		f.close()

with open("output/authoren.csv", "w") as f:
	authoren = list(set(authoren))
	authoren.sort()
	f.write("\n".join(authoren))
	f.close()

with open("output/werken.csv", "w") as f:
	werken = list(set(werken))
	werken.sort()
	f.write("\n".join(werken))
	f.close()

with open("output/texts.csv", "w") as f:
	TextIdentifiers = list(set(TextIdentifiers))
	TextIdentifiers.sort()
	f.write("\n".join(TextIdentifiers))
	f.close()
