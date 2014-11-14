#!/usr/bin/python3
# -*- coding: UTF-8 -*-



class Steps(object):
	def __init__(self):
		self.__isA__ = "Steps"


class Step(Steps):
	def __init__(self, matrix, fn, normalizer, child = None):
		"""
		fn -> function to create node
		"""
		self.matcher = matrix["matcher"]
		self.grouper = matrix["grouper"]

		self.nodeMaker = fn
		self.normalizer = normalizer

		self.child = None
		if child:
			self.child = child

	def tail(self, node, text):
		""" Add some text at the end of the container """
		if node.tail:
			text = node.tail + text
		node.tail = text
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
				print( "Node Maker")
				node = self.nodeMaker(element, node, self.grouper, self.normalizer)
			else:
				print( "Next Step")
				node = self.next(node, element)

		return node



