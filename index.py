#!/usr/bin/python
# -*- coding: utf-8 -*-

from libxml2 import parseDoc
import codecs
import xml.etree.cElementTree as ET

def getH1(doc):
	div1 = doc.xpathEval("//div/H1|h1")
	try:
		return div1[0].getContent()
	except Exception as E:
		print("No H1 \n\t" + E)

def getNotH1(doc):	
	div = doc.xpathEval("//div/*[not(self::H1|h1)]") #Should return text only
	try:
		return " ".join([element.getContent() for element in div])
	except Exception as E:
		print("No H1 \n\t" + E)
i = 0
limit = 10
#Corrected = 400
with codecs.open("Georges_1913_no_header.xml", "r", "utf-8") as f:

	georges = ET.Element("div")
	#In this document, we have one line = one word definition, h1 represent orth
	for word in f.readlines():
		#We create a node for this element
		entryFree = ET.SubElement(georges, "entryFree")

		#We get the word into xml format to parse it...
		word = word.encode("utf-8")
		line = "<div>{0}</div>".format(word)

		try:
			doc = parseDoc(line)
			ctxt = doc.xpathNewContext()
		except Exception as E:
			print( E)
			print( i)
			print( line)
			break

		if doc:
			h1 = getH1(ctxt)
			orth = ET.SubElement(entryFree, "orth")
			orth.set("key", h1)
			orth.text = h1
			print getNotH1(ctxt)
			
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

tree = ET.ElementTree(georges)
tree.write("here.xml", encoding="utf-8")