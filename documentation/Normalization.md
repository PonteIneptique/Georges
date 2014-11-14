#Normalization

**This part of the documentation might be out of date. Be careful with it**

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