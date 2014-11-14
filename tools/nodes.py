#!/usr/bin/python3
# -*- coding: UTF-8 -*-

def Greek(text, node, regexp = None):	# For this particular function, there is no use of regexp at this point
	lang = cElementTree.SubElement(node, "lang")
	lang.set("lang", "greek")
	lang.text = text
	return node

def PrimarySource(text, node, regexp):
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

	return node #Return the last node in usage


def Quote(text, node, regexp):
	items = [m.groupdict() for m in regexp.finditer(text)][0]

	author = items["author"]
	author = replaceAuthor(author)

	text = items["text"]

	bibl = cElementTree.SubElement(node, "quote")
	bibl.text = text

	aNode = cElementTree.SubElement(bibl, "author")
	aNode.text = author

	return node


def SecondarySource(text, node, regexp):
	items = [m.groupdict() for m in regexp.finditer(text)][0]
	SecondaryAuthor = items["SecondaryAuthor"]

	SecBiblNode = cElementTree.SubElement(node, "bibl")

	SecAuthorNode = cElementTree.SubElement(SecBiblNode, "author")
	SecAuthorNode.text = SecondaryAuthor

	node = opusFinder(items["Quoted"], SecBiblNode)

	return node #Return the last node in usage