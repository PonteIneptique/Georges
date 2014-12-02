#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import xml.etree.cElementTree as cElementTree
import copy
import regex as re


from tools.exporter import Exporter
from tools.generator import Georges

sample = True

georges = Georges("input/body.xml")
georges.convert(limit = 10, sample = sample)
georges.quoted(sample = sample)
georges.write(sample = sample)
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