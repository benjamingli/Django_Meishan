#!/usr/bin/python
# -*- coding: utf-8 -*-
__metaclass__ = type

import sys, re

if len(sys.argv) != 2:
    print "%s <input.csv>" % sys.argv[0]
    sys.exit(1)
infile = sys.argv[1]

count = 0
num = {}
for line in open(infile):
    count += 1
    if count > 400: break
    r = re.match(u"(\d{4}\u5e74\d{2}\u6708\d{2}\u65e5)(|\d{2}\u65f6),([^,]+).*,(\d+)$", line.decode('utf8'))
    if not r:
        continue
    d = r.group(1).encode('utf8')
    if num.has_key(d):
        num[d] += 1
    else:
        num[d] = 1

count = 0
day = ""
hour= ""
print '<div class="tree well"><ul>'
for line in open(infile):
    count += 1
    if count > 400: break
    r = re.match(u"(\d{4}\u5e74\d{2}\u6708\d{2}\u65e5)(|\d{2}\u65f6),([^,]+).*,(\d+)$", line.decode('utf8'))
    if not r:
        continue
    d = r.group(1).encode('utf8')
    h = r.group(2).encode('utf8')
    m = r.group(3).encode('utf8')
    c = r.group(4).encode('utf8')
    if d==day and h!=hour:
        print '</ul></li>'
        if h != "":
            print '<li style="display: none;"><span><i class="icon-minus-sign"></i> %s</span><ul>' % h
    if d != day:
        if day != "":
            print '</ul></li>'
            if hour != "":
                print '</ul></li>'
        print '<li><span><i class="icon-folder-open"></i> %s</span> %s<ul>' % (d, num[d])
        if h != "":
            print '<li style="display: none;"><span><i class="icon-minus-sign"></i> %s</span><ul>' % h
    hour = h
    day = d
    if h != "":
        print '<li><span><i class="icon-leaf"></i> %s</span> %s</li>' % (m, c)
    else:
        print '<li style="display: none;"><span><i class="icon-leaf"></i> %s</span> %s</li>' % (m, c)
if hour != "":
    print '</ul></li>'
if day != "":
    print '</ul></li>'
print '</ul></div>'
