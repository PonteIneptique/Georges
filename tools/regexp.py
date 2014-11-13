n#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import regex as re

class RegExp(object):
 	"""docstring for RegExp"""
 	def __init__(self, dictionary):
 		super(RegExp, self).__init__()

 		self.dictionary = dictionary
 		
 		self.matrices = {
 			"primarysource" : {
				"matcher" : re.compile("(?P<match>{0})".format(self.generate("opus", True))),
				"grouper" : re.compile(self.generate("opus"))
			},
			"secondarysource" : {
				"matcher" : re.compile("(?P<match>(?:[A-Z]{1}[a-z]+)(?:\szu\s){1}(?:" + opusRegExp(True) + ")+)", flags= re.UNICODE),
				"grouper" : re.compile("(?P<SecondaryAuthor>[A-Z]{1}[a-z]+)(?:\szu\s){1}(?P<Quoted>(?:" + re.sub("\?P<[a-zA-Z0-9]+>", "", opusRegExp()) + ")+(?:\s)*){1}", flags= re.UNICODE)
			},
			"quotes" : {
				"matcher" : re.compile("(?P<match>{0})".format(QuotationRegExp(True))),
				"grouper" : re.compile(QuotationRegExp())
			}
			"list" : {
				"grouper" : re.compile("^([1-9]{1,3}|[abcdefABCDEF]{1}|IX|IV|V?I{0,3})$")
			},
			"greek" : {
				"grouper" : re.compile("((?:(?:[\p{Greek}µ']+)+[\s\.\,]*)+)")
			}
		}

	def generate(self, category, ignoreGroups):

	def getAuthor(self, formatting):
		if formatting == "regexp":
			return self.authorList()
		else:
			return self.authorDictionary()

	def list(self, category, depth = 0):
		if depth == 0:
			data = [self.regularize(entry) for entry in self.dictionary.lists[category]]
		else:
			data = [self.regularize(entry[depth]) for entry in self.dictionary.lists[category]]
		return 

	def regularize(self, text):
		text = text.replace("\n", "").replace(" ", "\s").replace(".", "\.")
		return "(?:{0})".format(text)

	def authorList(self):
		output = []
		with open("./dictionary/authors.csv") as f:
			output = ["(?:{0})".format(line.replace("\n", "").replace(" ", "\s").replace(".", "\.")) for line in f.readlines()]
			f.close()

		return "|".join(output)
		
"""
	def getBooksRegexp():
		lines = []
		with open("./dictionary/books.csv") as f:
			lines = ["(?:{0})".format(line.replace("\n", "").replace(" ", "\s").replace(".", "\.").split("\t")[1]) for line in f.readlines()]
			f.close()

		output = lines + ["(?:(?:in|ex|de|ad){1}[\s]{1}){0,1}(?:[^\W\d]{2,}\.(?:[\s])*)+)"]
		return "|".join(output)
"""

	def primarySource(opusfinder = False):
		paragraphCharacters = "(?:[p\§]{1}\.{0,1}\s){0,1}"
		authorRegExp = self.getAuthors("regexp")
		regexp = "(?P<author>" + authorRegExp + "){1}(?:\s(?P<opus>" + BooksRegExp + "+){0,1}(?:\s(?P<identifier1>" + paragraphCharacters + "[0-9]+\,)){0,1}(?:\s(?P<identifier2>" + paragraphCharacters +  "[0-9]+\,)){0,1}(?:\s(?P<identifier3>" + paragraphCharacters + "[0-9]+\,)){0,1}(?:\s(?P<identifier4>" + paragraphCharacters + "[0-9]+[\.:]{0,1})){1}"
		if opusfinder:
			#sub
			return re.sub("P<[a-zA-Z0-9]+>", ":", regexp)
		else:
			return regexp

	def quotes(finder = False):
		# "(?:[:;\s\)\,]+)" + 
		regexp = "(?P<text>[a-zA-Z ]+)\,[\s]*(?P<author>"+ AuthorSimpleRegexp + "){1}"
		if finder:
			return re.sub("P<[a-zA-Z0-9]+>", ":", regexp)
		return regexp