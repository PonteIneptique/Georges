#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#Reading manual one

with open("../dictionary/author-manual.csv") as f:
	general = [line.replace("\n", "") for line in f.readlines()]
	f.close()

#Reading manual one
with open("../dictionary/authors-automatic-pauly.csv") as f:
	general = general + [line.replace("\n", "") for line in f.readlines()]
	f.close()

#Generation General one
with open("../dictionary/authors.csv", "w") as f:
	f.write("\n".join(general))
	f.close()