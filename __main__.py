#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import xml.etree.cElementTree as cElementTree
import copy
import regex as re


from tools.exporter import Exporter
from tools.normalization import Normalizer
from tools.regexp import RegExp
from tools.steps import Step

from tools.nodes import Greek as GreekNodification
from tools.nodes import PrimarySource as PrimarySourceNodification
from tools.nodes import SecondarySource as SecondarySourceNodification
from tools.nodes import Quote as QuoteNodification

from tools.divers import polishSenses
from tools.divers import divideText
from tools.divers import polishH1
from tools.divers import firstLine
from tools.divers import getLevel
from tools.divers import prettify

normalizer = Normalizer()
regexp = RegExp(normalizer)


Greek = Step (
		"greek",
		regexp.matrices,
		GreekNodification,
		normalizer
	)

PrimarySource = Step(
		"primarySource",
		regexp.matrices,
		PrimarySourceNodification,
		normalizer,
		Greek
	)

SecondarySource = Step(
		name = "secondarySource",
		matrix = regexp.matrices,
		fn = SecondarySourceNodification,
		normalizer = normalizer,
		child = PrimarySource
	)

#We set up a link to what we think should be first step, to avoid changing it directly in the code later
FirstStep = SecondarySource

#Configuration
entryFreeId = 1
limit = 10 #For the sample
break_on_sample = True
ignoreReplacer = False #Ignore the merger for Werken

root = cElementTree.Element("text")
body = cElementTree.SubElement(root, "body")

div = {}
head = {}
with open("input/body.xml") as f:

	char = None
	#In this document, we have one line = one word definition, h1 represent orth
	for line in f.readlines():
		#We split the line around the <h1> tag
		h1, senses_text = divideText(line, entryFreeId)
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
		entryFree.set("n", str(entryFreeId))

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
		senses_text_split = regexp.matrices["senses"]["splitter"].split(senses_text)
		senses_text_split = [s for s in senses_text_split if s != None]

		if len(senses_text_split) == 1:

			#We check for itype, etym, gen...
			text = firstLine(senses_text, entryFree)


			#When a sense has no number before it
			senses.append(cElementTree.SubElement(entryFree, "sense"))
			node = senses[len(senses) - 1 ]
			node = FirstStep.process(text, node)
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
				matching = regexp.matrices["senses"]["grouper"].match(text)

				#If this doesn't match, we have a sense's text
				#If this match, we have a numeric identifier : we set id to it
				if not matching:
					#id was set on previous iteration, we set n attribute to it
					if id:
						senses.append(cElementTree.SubElement(entryFree, "sense"))
						node = senses[len(senses) - 1 ]
						node.set("n", id)
						node.set("level", str(levelN))
						node = FirstStep.process(text, node)
					else: #We dont have text
						text = firstLine(text, entryFree)
						senses.append(cElementTree.SubElement(entryFree, "sense"))
						node = senses[len(senses) - 1 ]
						node = FirstStep.process(text, node)
				else:
					id = text
					levelN, levelDictionary = getLevel(id, levelDictionary)

		if entryFreeId == limit:
			with open("output/sample.xml", "w") as f:
				f.write(prettify(copy.deepcopy(root)))
				f.close()
			if break_on_sample:
				break
		entryFreeId += 1 

if not break_on_sample:
	with open("output/output.xml", "w") as f:
		f.write(cElementTree.tostring(root, 'unicode'))
		f.close()


	#Exporter Part
	AuthorBookPrimarySource = Exporter(".//bibl[@type='primary']", "./output/CSVs/author-with-title-primary-source.csv")
	AuthorPrimarySourceResults = Exporter(".//bibl[@type='primary']/author", "./output/CSVs/author-primary-source.csv")
	AuthorSecondarySourceResults = Exporter(".//bibl[@type='secondary']/author", "./output/CSVs/author-secondary-source.csv")
else:
	AuthorBookPrimarySource = Exporter(".//bibl[@type='primary']", "./output/CSVs/author-with-title-primary-source-sample.csv")
	AuthorPrimarySourceResults = Exporter(".//bibl[@type='primary']/author", "./output/CSVs/author-primary-source-sample.csv")
	AuthorSecondarySourceResults = Exporter(".//bibl[@type='secondary']/author", "./output/CSVs/author-secondary-sample-source.csv")

AuthorBookPrimarySource.search(body, True)
AuthorBookPrimarySource.write()

AuthorPrimarySourceResults.search(body)
AuthorPrimarySourceResults.write()

AuthorSecondarySourceResults.search(body)
AuthorSecondarySourceResults.write()