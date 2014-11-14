#!/usr/bin/python3
# -*- coding: UTF-8 -*-



class Steps(object):
	def __init__(self):
		self.__isA__ = "Steps"


class Step(Steps):
	def __init__(self, name, matrix, fn, normalizer, child = None):
		"""
		fn -> function to create node
		"""
		self.matcher = matrix[name]["matcher"]
		self.matrix = matrix

		self.nodeMaker = fn
		self.normalizer = normalizer

		self.child = None
		if child:
			self.child = child

	def tail(self, node, text):
		""" Add some text at the end of the container """
		subelements = list(node)
		print (subelements)
		if subelements and len(subelements) > 0:
			subnode = subelements[-1]
			if subnode.tail:
				text = subnode.tail + text
			subnode.tail = text
		else:
			if node.text:
				text = node.text + text
			node.text = text
		return node

	def next(self, node, text = None):
		""" If there is a next step, this function will go there, if not, it will simply add some potential text at the end of the element"""
		if not self.child:
			if text:
				node = self.tail(node, text)
			return node
		else:
			return self.child.process(text, node)


	def process(self, text, node):
		caught = self.matcher.split(text)
		caught = [c for c in caught if c]

		for element in caught:
			if self.matcher.match(element):
				node = self.nodeMaker(element, node, self.matrix, self.normalizer)
			else:
				node = self.next(node, element)

		return node



