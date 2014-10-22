#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import codecs
import xml.etree.cElementTree as cElementTree
import xml.etree.ElementTree as ElementTree
import re

def getH1(doc):
	div1 = doc.findall(".//H1") + doc.findall(".//h1")
	try:
		doc.remove(div1[0])
		text = div1[0].text
		if text[-1:] == ",":
			text = text[0:-1]
		return text, doc
	except Exception as E:
		print("No H1 \n\t" + E)

def getNotH1(doc):
	try:
		return ElementTree.tostring(doc, encoding="unicode", method="text")
	except Exception as E:
		print("No H1 \n\t" + E)

#Match number
ol_match = re.compile("^([1-9]{1,3}|[abcdefABCDEF]{1}|IX|IV|V?I{0,3})$")

i = 0
limit = 100
#Corrected = 400
with open("Georges_1913_no_header.xml") as f:

	georges = cElementTree.Element("div")
	#In this document, we have one line = one word definition, h1 represent orth
	for line in f.readlines():
		#We create a node for this element
		entryFree = cElementTree.SubElement(georges, "entryFree")

		#We get the word into xml format to parse it...
		line = "<div>{0}</div>".format(line)

		try:
			doc = cElementTree.fromstring(line)
		except Exception as E:
			print(E)

		if doc:
			h1, doc = getH1(doc)
			orth = cElementTree.SubElement(entryFree, "orth")
			orth.set("key", h1)
			orth.text = h1

			senses_text = getNotH1(doc)
			senses = []
			senses_text_split = re.split('[–]{0,1}\s([1-9]{1,3}|[abcdefABCDEF]{1}|IX|IV|V?I{0,3})\)\s', senses_text)
			index_sense = 1

			id = None
			while index_sense <= len(senses_text_split):
				text = senses_text_split[index_sense - 1] #Text gotten from re.splut
				matching = ol_match.match(text)
				print (matching)
				print (text)
				if not matching:
					if id:
						senses.append(cElementTree.SubElement(entryFree, "sense"))
						senses[len(senses) - 1 ].text = text
						senses[len(senses) - 1 ].set("n", id)
					else:
						#When a sense has no number before it
						senses.append(cElementTree.SubElement(entryFree, "sense"))
						senses[len(senses) - 1 ].text = text
				else:
					id = text

				index_sense += 1
			
		"""
		<H1>A. 1. A, a,</H1>
		<I>der erste Buchstabe des lateinischen Alphabets. – Als Abkürzung:</I>
		1) = der Vorname Aulus.  
		<p>
		2) = Antiquo <I>(ich verwerfe den neuen Vorschlag), auf den Stimmtafeln in röm. Volksversammlungen.</I> – 
		3) = Absolvo <I>(ich spreche frei), auf den Stimmtafeln der Richter; dah.</I> 
		A gen. littera salutaris<I> bei</I> Cic. Mil. 15. – 
		4) <I>vor Zahlen, Jahresbezeichnung</I> (= Annus) <I>auf Grabschriften usw.: u. so </I><B>A. U. C.</B> = anno urbis conditae – <I>aber </I><B>a. u. c.</B> = ab urbe condita. – <I>u. </I><B>a. d. </B>= ante diem <I>als Datum.</I> – 
		5) = Augustus, <I>häufig in Inschriften; </I><B>A. A.</B> = Augusti duo;<B> A. A. A.</B> = Augusti tres. – <I>aber </I><B>A. A. A. F. F. </B><I>nach</I> III viri = auro, argento, aeri flando, feriundo. – 
		6) = Auditor, <I>im Gegensatz zu</I> M(agister) <I>in</I> Cic. Tusc. disp. 
		</p>

		OR 
		<H1>abāctio,</H1> 
		ōnis, f. (abigo) = εξέλασις, <I>das </I><B><I>Wegtreiben,</I></B> Hier. in Ierem. 1, 5, 15. Gloss. II, 302, 50. 
		"""

		"""
		<entryFree id="n10" type="hapax" key="abaculus">
			<orth extent="full" lang="la">&abreve;b&abreve;c&ubreve;lus</orth>
			, <itype>i</itype>, <gen>m.</gen> 
			<lbl>dim.</lbl>
			<etym>abacus</etym>, 
			<sense id="n10.0" n="I" level="1">
				<hi rend="ital">a small cube or tile of colored glass for making ornamental pavements</hi>,
				 the Gr. <foreign lang="greek">u\buki/skos</foreign>, 
				<bibl n="urn:cts:latinLit:phi0978.phi001:36:67"><author>Plin.</author> 36, 26, 67, &sect; 199</bibl>. <cb n="ABAL"/>
			</sense>
		</entryFree>
		"""
		if i == limit:
			break
		i += 1 

tree = cElementTree.ElementTree(georges)
tree.write("here.xml", encoding="unicode")