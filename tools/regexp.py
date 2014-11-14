#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import regex as re

class RegExp(object):
	"""docstring for RegExp"""
	def __init__(self, Normalizer, normalization = False):
		super(RegExp, self).__init__()

		self.normalization = normalization

		self.Normalizer = Normalizer
		
		self.matrices = {
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
				"grouper" : re.compile("^([1-9]{1,3}|[abcdefABCDEF]{1}|IX|IV|V?I{0,3})$")
			},
			"greek" : {
				"finder" : re.compile("((?:(?:[\p{Greek}µ']+)+[\s\.\,]*)+)"),
				"grouper" : re.compile("(?P<match>(?:(?:[\p{Greek}µ']+)+[\s\.\,]*)+)")
			}
		}

	def generate(self, category, grouper = True):
		""" Generate a regular expression object for the given category """
		mappings = {					# We set up a dictionary to do some kind of switch-alike function where it is easy to read what shoud do what
			"primarySource" 	: self.primarySource,
			"secondarySource"	: self.secondarySource,
			"quote"			: self.quotes
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
		if depth == 0:
			data = data + [self.regularize(entry) for entry in self.Normalizer.lists[category]]
		else:
			data = data + [self.regularize(entry[depth]) for entry in self.Normalizer.lists[category]]
		return data

	def regularize(self, text):
		""" Make sure than some string are regular expression compliant """ 
		text = text.replace("\n", "").replace(" ", "\s").replace(".", "\.")
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
		regexp += "(?:\s(?P<opus>" + BookRegExp + "+){0,1}(?:\s(?P<identifier1>" + NumeRegExp + "[0-9]+\,)){0,1}"
		regexp += "(?:\s(?P<identifier2>" + NumeRegExp + "[0-9]+\,)){0,1}"
		regexp += "(?:\s(?P<identifier3>" + NumeRegExp + "[0-9]+\,)){0,1}"
		regexp += "(?:\s(?P<identifier4>" + NumeRegExp + "[0-9]+[\.:]{0,1})){1}"

		return regexp

	def secondarySource(self):
		""" Returns a regular expression string for matching Secondary Source comments """
		
		regexp  = "(?P<SecondaryAuthor>[A-Z]{1}[a-z]+)"
		regexp += "(?:\szu\s){1}"
		regexp += "(?P<Quoted>(?:" + self.primarySource() + ")+(?:\s)*){1}"

		return regexp

	def quotes(self):
		""" Returns a regular expression string for matching quotes"""
		AuthRegExp = self.author()

		regexp  = "(?P<text>[a-zA-Z ]+)"
		regexp += "\,[\s]*"
		regexp += "(?P<author>"+ AuthRegExp + "){1}"

		return regexp