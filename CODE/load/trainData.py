#!/usr/bin/python
# -*- coding: utf-8 -*-
__metaclass__ = type

import sys, re, MySQLdb

if len(sys.argv) < 3:
    print "%s <output> <<input.csv>>" % sys.argv[0]
    sys.exit(1)

out = open(sys.argv[1], 'w')
outName = open(sys.argv[1]+".name", 'w')
conn = MySQLdb.Connection('localhost', 'django', 'django', 'django')

name = {}
nameNumber = 0
for i in range(2, len(sys.argv)):
    target = {}
    f = open(sys.argv[i])
    l = f.readline().strip().split(',')
    for j in range(2, len(l)):
        if(not name.has_key(l[j])):
            outName.write("%d,%s\n" % (nameNumber,l[j]))
            name[l[j]] = nameNumber
            nameNumber += 1
        target[j] = name[l[j]]
    cur = conn.cursor()
    while True:
        line = f.readline()
        if not line: break
        l = line.strip().split(',')

        day = re.match(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', l[0])
        year = int(day.group(1))
        month= int(day.group(2))
        dayy = int(day.group(3))
        lines = cur.execute('SELECT holiday,maxTemp,minTemp,typeDay FROM load_weather WHERE date="%s-%02d-%02d";' % (year,month,dayy))
        if lines != 1:
            print "请输入当日天气:%s\n" % l[0]
            exit(1)
        r = cur.fetchall()
        w = "%s,%s,%s,%s" % (r[0][0],r[0][1],r[0][2],r[0][3])

        d = "%s,%s,%s" % (year, month, dayy)

        hour = re.match(r'(\d{1,2}):(\d{1,2}):\d{1,2}', l[1])
        h = str(int(hour.group(1)))
        if hour.group(2) == '15':
            h += '.25'
        if hour.group(2) == '30':
            h += '.5'
        if hour.group(2) == '45':
            h += '.75'

        for i in range(2,len(l)):
            if l[i] == '0' or l[i] == '-':
                continue
            out.write("%s,%s,%s,%s,%s\n" % (target[i],d,h,w,l[i]))

    f.close()
    cur.close()

conn.close()
out.close()
outName.close()
