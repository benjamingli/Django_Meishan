#!/usr/bin/python
# -*- coding: utf-8 -*-
__metaclass__ = type

import sys, codecs


def ReadFile(filePath,encoding="utf-8"):
    with codecs.open(filePath,"r",encoding) as f:
        return f.read()
  
def WriteFile(filePath,u,encoding="gbk"):
    with codecs.open(filePath,"w",encoding) as f:
        f.write(u)
  
def UTF8_2_GBK(src,dst):
    content = ReadFile(src,encoding="utf-8")
    WriteFile(dst,content,encoding="gbk")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "%s <input(utf8)> <output(gbk)>" % sys.argv[0]
        sys.exit(1)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    UTF8_2_GBK(infile, outfile)

