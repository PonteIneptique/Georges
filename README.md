Georges
=======
This is an automated conversion made by Thibault Clérice for the [Georges Latin dictionary](http://outils.biblissima.fr/collatinus/ressources/Georges_1913.xml) found on [Biblissima](http://outils.biblissima.fr)

There is a small sample available in `output/sample.xml` to check the formatting and potential error of the transformation

Full document in output.xml

##Automatic replacement
The abbreviation system being chaotic and random in the Georges, I have use a book.csv dictionary issue through `fuzzywuzzy.processs` in `StringComparison/WerkStringComparison.py` to normalize names. From 4241 lines of Books/Author found (`/output/old-werken.csv`), I came to have 2647 such tuples.

##Improve Author/Work Replacement
- Add manuals abbreviations and synonyms in `author-synonyms`, `pauly-double-authors` and `automatic-normalizing-books`
- Run `index.py` with `ignoreReplacer` set to `True`
- Run `StringComparison/WerkStringComparison.py`
- Run `StringComparison/generateNormalizingBook.py`
- Run `index.py` with `ignoreReplacer` set to `False`

##Generating TEI FILE
- Add or update revision in `input/header.xml`
- Run merge.py

##Credits
- [Abzkurzung.txt](http://www.zeno.org/Georges-1913/M/Verzeichnis+der+Abk%C3%BCrzungen)
- [Header and Body](http://outils.biblissima.fr/collatinus/ressources/Georges_1913.xml)