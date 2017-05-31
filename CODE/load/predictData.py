#!/usr/bin/python
# -*- coding: utf-8 -*-
__metaclass__ = type

import sys, re, os

if len(sys.argv) != 5:
    print "%s <.name.wc-l.int> <2016-3-9> <weather.str> <output>" % sys.argv[0]
    sys.exit(1)

linecount = int(sys.argv[1])
day = re.match(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', sys.argv[2])
d = "%s,%s,%s" % (int(day.group(1)),int(day.group(2)),int(day.group(3)))
w = sys.argv[3]
out = open(sys.argv[4], 'w')

for i in range(linecount):
    h = 0.0
    for j in range(96):
        out.write("%s,%s,%s,%s,%d%.2d\n"% (i,d,h,w,i,j))
        h += 0.25

out.close()
