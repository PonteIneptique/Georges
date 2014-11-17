#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Exporter(object):
	def __init__(self, xmlpath, filename):
		self.xmlpath = xmlpath
		self.filename = filename

	def search(self, xml, children = False):
		""" 

		options
		children : if set to True, will take the result set and append the xml in some kind of dictionary, expecting no duplicates
		"""
		nodes = xml.findall(self.xmlpath)
		if children:
			mother = ["\t".join([node.text for node in list(element)]) for element in nodes]
			lines = list(set(mother))
			lines.sort()
		else:
			author = [node.text for node in nodes]
			author = list(set(author))
			author.sort()

			lines = [[name] for name in author]

			lines = ["\t".join(line) for line in lines]
			
		self.lines = lines
		return lines

	def write(self):
		with open(self.filename, "w") as f:
			f.write("\n".join(self.lines))
			f.close()
			return True
		return False