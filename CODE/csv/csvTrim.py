#!/usr/bin/python
# -*- coding: utf-8 -*-
__metaclass__ = type

import sys

if len(sys.argv) != 3:
    print "%s <input.csv> <output.csv>" % sys.argv[0]
    sys.exit(1)
infile = sys.argv[1]
outfile = sys.argv[2]
out = open(outfile, 'w')

for line in open(infile):
    l = line.strip().split(',')
    for i in range(len(l)):
        l[i] = l[i].strip('"')
        if l[i] == "1899-12-30":
            l[i] = "00:00:00"
    out.write("%s\n" % ",".join(l))

out.close()
