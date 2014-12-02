#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys, os
sys.path.append("../")

from nose import with_setup

from tools.generator import Georges

georges = Georges("input/body.xml")
georges.generate(limit = 10, sample = True)


def test_only_one_dive_zero():
	print ("There should be only one div0 with attr=\"a\"")
	xml = georges.root
	div0 = xml.findall(".//div0")
	assert len(div0) == 1
	assert div0[0].get("n") == "A"