#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class normalizer(object):

	def __init__(self):
		self.dictionaries = {
			"author" : self.getDictionary("author"),
			"primarysource" : self.getDictionary("primarySource")
		}
		self.lists = {
			#Get a simple list of work names or book names and so on
		}

	def getDictionary(self, category):
		if category == "primarySource":
			return self.getPrimarySourceDictionary()
		elif category == "author":
			return self.getAuthorDictionary

	def replace(self, item, category):
		if type(item) != tuple:
			if item in self.dictionaries[category]:
				return self.dictionaries[category][item]
			return item
		else: #We assume it's a tuple
			if item[0] in self.dictionaries[category] and item[1] in self.dictionaries[category][item[0]]:
				data = self.dictionaries[category][item[0]]
				return data[0], data[1]
			else:


	def getPrimarySourceDictionary(self):
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

	def getAuthorDictionary(self):
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

	def replaceAuthor(author):
		if author in ReplacementAuthorDictionary:
			return ReplacementAuthorDictionary[author]
		return author

	def replaceAuthorBook(author, book):
		if author in ReplacementBookDictionary and book in ReplacementBookDictionary[author]:
			t = ReplacementBookDictionary[author][book]
			return t[0], t[1]
		return author, book