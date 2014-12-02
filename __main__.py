#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tools.generator import Georges

sample = True

georges = Georges("input/body.xml")
georges.generate(limit = 10, sample = sample)
georges.quoted(sample = sample)
georges.xml(sample = sample)