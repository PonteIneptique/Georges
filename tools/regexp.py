#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import regex as re
from langdetect import detect_langs

class LanguageDetector(object):
	def __init__(self, lang = "de"):
		self.lang = lang
		with open(os.path.dirname(os.path.abspath(__file__)) + "/stopwords/" + lang + ".txt") as f:
			stopwords = f.read().split(",")

		self.stopwords = stopwords
		regexp = "((?:zB\.|t\.t\.|[;\(\)\–\:]+|{0})[\s]*)".format("|".join(stopwords))
		self.largeSplitter = re.compile(regexp)

	def score(self, text):
		try:
			scores = detect_langs(text)
			for score in scores:
				if score.lang == "de":
					if score.prob > 0.99:
						return 1
					else:
						return 0
			return 0
		except:
			return 0

	def match(self, text):
		splitted = self.largeSplitter.split(text)
		results = [self.score(text) for text in splitted]
		if sum(results) > 0:
			return True
		else:
			return False

	def grouper(self, text):
		splitted = self.largeSplitter.split(text)

		strings = []
		for string in splitted:
			if string in self.stopwords:
				score = 1
			else:
				score = self.score(string)
			if len(strings) == 0:
				strings.append((string, score))
			else:
				if strings[-1][1] == score:
					strings[-1] = (strings[-1][0] + string, score)
				else:
					strings.append((string, score))

		return strings

	def group(self, text):
		pass

class RegExp(object):
	"""docstring for RegExp"""
	def __init__(self, Normalizer, normalization = False):
		super(RegExp, self).__init__()

		self.normalization = normalization

		self.Normalizer = Normalizer

		self.matrices = {
			"german" : {
				"matcher" : LanguageDetector()
			},
 			"primarySource" : {
				"matcher" : self.generate("primarySource", False),
				"grouper" : self.generate("primarySource")
			},
			"secondarySource" : {
				"matcher" : self.generate("secondarySource", False),
				"grouper" : self.generate("secondarySource")
			},
			"quotes" : {
				"matcher" : self.generate("quote", False),
				"grouper" : self.generate("quote")
			},
			"senses" : {
				"grouper" : re.compile("^([1-9]{1,3}|[abcdefABCDEFαβγδ]{1}|IX|IV|V?I{0,3})$"),
				"splitter" : re.compile("[–\,]{0,1}\s([1-9]{1,3}|[abcdefABCDEFαβγδ]{1}|IX|IV|V?I{0,3})\)\s")
			},
			"greek" : {
				"matcher" :  self.generate("greek"),
				"grouper" : re.compile("(?P<match>(?:(?:[\p{Greek}µ']+)+[\s\.\,]*)+)")
			},
			"firstLine" : {
				"grouper" : self.generate("firstLine")
			}
		}

	def generate(self, category, grouper = True):
		""" Generate a regular expression object for the given category """
		mappings = {					# We set up a dictionary to do some kind of switch-alike function where it is easy to read what shoud do what
			"primarySource" 	: self.primarySource,
			"secondarySource"	: self.secondarySource,
			"quote"			: self.quotes,
			"greek" : self.greek,
			"firstLine" : self.firstLine
		}

		regexp = mappings[category]()	# We call the function through the dictionary

		if not grouper:					# If this we want a regexp which match, we want to remove any subgroups
			regexp = self.getMatcher(regexp)

		return re.compile(regexp, flags = re.UNICODE)

	def getMatcher(self, regexp):
		""" Transform a string with Regular expression matching groups to a simple global matcher string"""
		regexp = self.removeGroups(regexp)		# First we transform group names to non-capturing groups
		return "(?P<match>{0})".format(regexp)				# Then we include it in a global matcher

	def removeGroups(self, regexp):
		""" Remove groups with name in regular expression string by non-capturing group """
		return re.sub("P<[a-zA-Z0-9]+>", ":", regexp)

	def lists(self, category, depth = 0):
		data = []
		""" Returns a formated regular expression list for a given category (books, authors)"""
		data = data + [self.regularize(entry) for entry in self.Normalizer.lists[category]]
		return data

	def regularize(self, text, nonCapturing = True):
		""" Make sure than some string are regular expression compliant """ 
		text = text.replace("\n", "").replace(" ", "\s").replace(".", "\.")
		if not nonCapturing:
			return text
		return "(?:{0})".format(text)


	def book(self):
		""" Returns a regular expression for matching Primary Sources Book's title including, if self.normalization is set to False (default), a list of expected titles"""
		regexp = "(?:(?:in|ex|de|ad){1}[\s]{1}){0,1}(?:[^\W\d]{2,}\.(?:[\s])*)+)"
		if self.normalization:
			return regexp
		return "|".join(self.lists("book", 1) + [regexp])

	def author(self):
		""" Returns a regular expression string for matching author name, including, if self.normalization is set to False (default), a list of expected names"""
		regexp = "(?:(?:Ps.\s){0,1}[A-Z]{1}[a-z]+\.)"
		if self.normalization:
			return regexp
		return "|".join(self.lists("author") + [regexp])

	def primarySource(self):
		""" Returns a regular expression string for matching primary sources (Author, Book, Text Part Identifiers) """
		NumeRegExp = "(?:[p\§]{1}\.{0,1}\s){0,1}"
		BookRegExp = self.book()
		AuthRegExp = self.author()

		regexp  = "(?P<author>" + AuthRegExp + "){1}"

		regexp += "(?:\s"
		regexp += 	"(?P<opus>" + BookRegExp + "+){0,1}"
		regexp += 	"(?:\s(?P<identifier1>" + NumeRegExp + "[0-9]+\,)"
		regexp += "){0,1}"

		regexp += "(?:\s(?P<identifier2>" + NumeRegExp + "[0-9]+\,)){0,1}"
		regexp += "(?:\s(?P<identifier3>" + NumeRegExp + "[0-9]+\,)){0,1}"
		regexp += "(?:\s(?P<identifier4>" + NumeRegExp + "[0-9]+[\.:]{0,1})){1}"

		regexp += "(?:[\s])*(?:ed\.\s(?P<editor>[\w]+[\.]*)){0,1}"

		return regexp

	def secondarySource(self):
		""" Returns a regular expression string for matching Secondary Source comments """
		
		author = "[A-Z]{1}[\w]+(?:\.){0,1}"

		regexp  = "(?!"
		regexp +=	"|".join([self.regularize(string, nonCapturing = False) for string in self.Normalizer.getExclude("SecondarySource.Authors")])
		regexp += ")"
		regexp += "(?:"
		regexp += 	"(?:"
		regexp += 		"(?P<SecondaryAuthor1>" + author + ")+"
		regexp += 		"(?:\s(?:zu|in|im)\s){1}"
		regexp += 	")|(?:"
		regexp += 		"(?:s\.[\s]+)+"
		regexp += 		"(?P<SecondaryAuthor2>" + author + ")+[\s]+"
		regexp += 	")"
		regexp += ")"		
		regexp += "(?P<Quoted>(?:" + self.primarySource() + ")+(?:\s)*){1}"

		return regexp

	def quotes(self):
		""" Returns a regular expression string for matching quotes"""
		AuthRegExp = self.author()

		regexp  = "(?P<text>[a-zA-Z ]+)"
		regexp += "\,[\s]*"
		regexp += "(?P<author>"+ AuthRegExp + "){1}"

		return regexp

	def greek(self):
		regexp = "((?:(?:[\p{Greek}µ']+)+[\s\.\,]*)+)"
		return regexp

	def firstLine(self):
		#We need to get the normalizer working
		abkurzung ="|".join([self.regularize(string, nonCapturing = False) for string in self.Normalizer.getKnown("Grammar")])
		#
		regexp  = "^"
		regexp += "(?:\s{0,1}(?P<itype1>[\w]+)[,\s]){0,1}"
		regexp += "(?:\s{0,1}(?P<itype2>[\w]+)[,\s]){0,1}"
		regexp += "(?:\s{0,1}(?P<itype3>[\w]+)[,\s]){0,1}"
		regexp += "(?:\s{0,1}(?P<itype4>[\w]+)[,\s]){0,1}"
		regexp += "(?:\s(?P<gen>" + abkurzung + "+)){0,1}"
		regexp += "(?:\s*\("
		regexp +=	"(?P<etym1>[\w\s]+)"
		regexp += "\)){0,1}"
		regexp += "(?:\s*=\s*(?P<etym2>[\w\s]+)){0,1}"
		regexp += "(?P<rest>.*)"

		return regexp
		
	