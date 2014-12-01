#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import xml.etree.cElementTree as cElementTree


def Greek(text, node, regexp = None, normalizer = None):	# For this particular function, there is no use of regexp at this point
	""" Put text in a subnode <lang> with attributes lang="greek" """
	lang = cElementTree.SubElement(node, "lang")
	lang.set("lang", "greek")
	lang.text = text
	return node

def PrimarySource(text, node, regexp, normalizer):
	""" Takes a match and create a subnode of node with the appropriate structure, using potentially a normalizer or a regexp"""
	items = getGroups(text, regexp["primarySource"])

	author = normalizer.replace(items["author"], "author")

	title = items["opus"]
	identifier = getListFromDictRegExp(items, "identifier", 4)

	bibl = cElementTree.SubElement(node, "bibl")
	bibl.set("type", "primary")

	aNode = cElementTree.SubElement(bibl, "author")
	lastNode = aNode

	if title:
		tNode = cElementTree.SubElement(bibl, "title")
		lastNode = tNode

	if author and title:
		author, title = normalizer.replace((author, title), "primarySource")

	aNode.text = author
	if title :
		tNode.text = title
	else:
		title = ""

	if items["editor"]:
		editorNode = cElementTree.SubElement(bibl, "editor")
		editorNode.text = items["editor"]

		lastNode = editorNode

	if identifier:
		lastNode.tail = " ".join(identifier)

	return node #Return the last node in usage


def Quote(text, node, regexp, normalizer):
	""" Take some text and a parent node, add a <quote> subnode """
	items = getGroups(text, regexp["quote"])

	author = normalizer.replace(items["author"], "author")

	text = items["text"]

	bibl = cElementTree.SubElement(node, "quote")
	bibl.text = text

	aNode = cElementTree.SubElement(bibl, "author")
	aNode.text = author

	return node


def SecondarySource(text, node, regexp, normalizer):
	""" Take some text and a parent node, add a bibl subnode for a secondary source """
	items = getGroups(text, regexp["secondarySource"])

	if items["SecondaryAuthor1"]:
		SecondaryAuthor = items["SecondaryAuthor1"]
	else:
		SecondaryAuthor = items["SecondaryAuthor2"]

	SecBiblNode = cElementTree.SubElement(node, "bibl")
	SecBiblNode.set("type", "secondary")

	SecAuthorNode = cElementTree.SubElement(SecBiblNode, "author")
	SecAuthorNode.text = SecondaryAuthor

	SecBiblNode = PrimarySource(items["Quoted"], SecBiblNode, regexp, normalizer)

	return node #Return the original

def FirstLine(text, node, regexp, normalizer):
	#<itype>a, um</itype>, = <foreign lang="greek">u)bu(skantos</foreign> Maybe some sense here
	matches = getGroups(text, regexp["firstLine"])

	#We join the itype
	itype = getListFromDictRegExp(matches, "itype", 4)

	#We then set the gen
	gen = matches["gen"]

	#We set the etym
	etym = getListFromDictRegExp(matches, "etym", 2)

	#We set the rest
	text = matches["rest"]

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

	node = cElementTree.SubElement(node, "sense")
	return (node, text)

################################################################
# General tools for NodeMaker function
################################################################

def getGroups(text, regexp):
	""" From a text and a regexp returns a dictionary """
	items = [m.groupdict() for m in regexp["grouper"].finditer(text)][0]
	return items

def getListFromDictRegExp(items, groupName, max):
	""" Return a list of match for a given ?p<matchName_X_> """
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