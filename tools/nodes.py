#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import xml.etree.cElementTree as cElementTree

from tools.divers import getListFromDictRegExp

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

	SecAuthorNode = cElementTree.SubElement(SecBiblNode, "author")
	SecAuthorNode.text = SecondaryAuthor

	SecBiblNode = PrimarySource(items["Quoted"], SecBiblNode, regexp, normalizer)

	return node #Return the original


################################################################
# General tools for NodeMaker function
################################################################

def getGroups(text, regexp):
	""" From a text and a regexp returns a dictionary """
	items = [m.groupdict() for m in regexp["grouper"].finditer(text)][0]
	return items
