#!/usr/bin/python
# -*- coding: utf-8 -*-
__metaclass__ = type

import sys, codecs


def ReadFile(filePath,encoding="gbk"):
    with codecs.open(filePath,"r",encoding) as f:
        return f.read()
  
def WriteFile(filePath,u,encoding="utf-8"):
    with codecs.open(filePath,"w",encoding) as f:
        f.write(u)
  
def GBK_2_UTF8(src,dst):
    content = ReadFile(src,encoding="gbk")
    WriteFile(dst,content,encoding="utf-8")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "%s <input(gbk)> <output(utf8)>" % sys.argv[0]
        sys.exit(1)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    GBK_2_UTF8(infile, outfile)

