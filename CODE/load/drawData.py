#!/usr/bin/python
# -*- coding: utf-8 -*-
__metaclass__ = type

import sys, re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import MultipleLocator
from numpy import *

if len(sys.argv) != 4:
    print "%s <input.name> <input.out> <output>" % sys.argv[0]
    sys.exit(1)

name = []
for line in open(sys.argv[1]):
    l = line.strip().split(',')
    name.append(l[1])

data = {}
for line in open(sys.argv[2]):
    l = line.strip().split(',')
    data[l[0]] = l[1]

outCSV = open(sys.argv[3]+".csv", 'w')
header = "时间点"
for i in range(len(name)):
    header += "," + name[i]
outCSV.write("%s\n" % header)
for i in range(96):
    line = "%d" % i
    for j in range(len(name)):
        key = "%03d%02d" % (j, i)
        line += ","+data[key]
    outCSV.write("%s\n" % line)
outCSV.close()


fontpath = '/django/CODE/load/font/simfang.ttf'
myfont = fm.FontProperties(fname=fontpath)

x = arange(96)
t = ['00:00','06:00','12:00','18:00','24:00']
for i in range(len(name)):
    y = []
    for j in range(96):
        y.append(float(data["%03d%02d" % (i, j)]))
    plt.clf()
    plt.plot(x,y)
    plt.xlim(24, max(x))
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(24))
    ax.xaxis.set_minor_locator(MultipleLocator(4))
    ax.xaxis.grid(True, which='minor')
    plt.grid(True)
    locs,labels = plt.xticks()
    plt.xticks(locs, t)
    plt.xlabel(u'时间点', fontproperties=myfont)
    plt.title(name[i].decode('utf8'), fontproperties=myfont)
    plt.savefig(sys.argv[3]+'_%03d.png' % i)
