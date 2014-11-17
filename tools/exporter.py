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
			#The whild road
			print(True)
		else:
			author = [node.text for node in nodes]
			author = list(set(author))
			author.sort()
			lines = [[name] for name in author]

		self.lines = lines
		return lines

	def write(self):
		with open(self.filename, "w") as f:
			f.write("\n".join(["\t".join(line) for line in self.lines]))
			f.close()
			return True
		return False