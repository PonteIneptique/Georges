#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ElementTree

filename = "../dictionary/pauly_raw.xml" 

tree = ElementTree.parse(filename)
root = tree.getroot()


pauly = {}
for tr in root.findall('tr'):
  tds = tr.findall("td")
  abbreviation = tds[0]
  full = tds[1]

  abbreviation = abbreviation.findall("p")
  full = full.findall("p")

  author = abbreviation[0].find("span").text
  pauly[author] = []

  if len(abbreviation) > 1:
    abbreviation = abbreviation[1:]
    for abb in abbreviation:
      pauly[author].append(abb.find("span").text.replace("\t", ""))



import pickle
with open("pauly.pickle", "wb") as f:
  pickle.dump(pauly, f)
  f.close()

double = []
authors = []
for author in pauly:
  elements = author.split(" ")
  elements = [e for e in elements if len(e) > 1]
  authors.append(" ".join(elements))
  if len(elements) > 1:
    double.append(" ".join(elements))

with open("../dictionary/pauly-double-authors.csv", "w") as f:
  f.write("\n".join(double))
  f.close()

with open("../dictionary/authors-automatic-pauly.csv", "w") as f:
  f.write("\n".join(authors))
  f.close()