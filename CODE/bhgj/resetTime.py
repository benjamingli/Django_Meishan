#!/usr/bin/python
# -*- coding: utf-8 -*-
__metaclass__ = type

import sys, datetime, re

if len(sys.argv) != 3:
    print "%s <input.csv> <output.csv>" % sys.argv[0]
    sys.exit(1)
infile = sys.argv[1]
outfile = sys.argv[2]
out = open(outfile, 'w')

h = {}
output = {}
for line in open(infile):
    r = re.match(u".+(\d{4})\u5e74(\d{2})\u6708(\d{2})\u65e5(\d{2})\u65f6(\d{2})\u5206(\d{2})\u79d2\s+(.+?)\s+(\u52a8\u4f5c|\u590d\u5f52)", line.decode('utf8'))
    if r:
        d = datetime.datetime(int(r.group(1)), int(r.group(2)), int(r.group(3)),\
                              int(r.group(4)), int(r.group(5)), int(r.group(6)))
        key = r.group(7).encode('utf8')
        typ = r.group(8).encode('utf8')
        if typ == "动作":
            if h.has_key(key):
                output[h[key].strftime('%Y-%m-%d %H:%M:%S')+",无,"+key] = 99999
            h[key] = d
        if typ == "复归" and h.has_key(key):
            value = (d-h[key]).seconds
            if value >= 30:
                output[h[key].strftime('%Y-%m-%d %H:%M:%S')+","+d.strftime('%Y-%m-%d %H:%M:%S')+","+key] = value
            del h[key]
for key in h:
    output[h[key].strftime('%Y-%m-%d %H:%M:%S')+",无,"+key] = 99999

s = sorted(output.keys())
for i in range(len(s)):
    out.write("%s,%s\n" % (s[i],output[s[i]]))

out.close()
