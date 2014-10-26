#!/usr/bin/python3
# -*- coding: UTF-8 -*-

with open('./output/TEI.xml', 'w') as outfile:
	with open("./input/output-manual-header.xml") as infile:
		outfile.write(infile.read())
		infile.close()
	with open("./output/output.xml") as infile:
		outfile.write(infile.read().replace('<?xml version="1.0" ?>', ""))
		infile.close()
	outfile.write("\n</TEI.2>")
	outfile.close()