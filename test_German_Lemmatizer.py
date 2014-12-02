#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tools.regexp import LanguageDetector

german = LanguageDetector()

texts = [
	"a Delta transire, auf der Seite, wo das Delta liegt, beim Delta, Auct. b. Al.: exercitus hostium duo, unus ab urbe, alter a Gallia obstant, Sall.: haud parvum munimentum a planioribus aditu locis, Liv.: ab utroque viae latere, Sen.: a theatro, Caes.: a septentrionibus, auf der Nordseite, Caes.: u. so die (bes. milit.) t.t. a fronte, a tergo, a latere, a dextro cornu, Cic., Caes. u.a.: ab novissimis, im Hintertreffen, Caes. – ebenso bei den geograph. Ausdrücken ab occasu et ortu solis, Liv.: Cappadocia, quae patet a Syria, Cic. – Dah. auch bei Tätigkeiten, die von einer Seite od. von einer Person auf derselben herkommen = von od. auf seiten"
]

for text in texts:
	result = german.grouper(text)

for tup in result:
	print (tup)