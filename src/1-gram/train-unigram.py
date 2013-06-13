#! /usr/bin/env python
# -*- coding:utf-8  -*-

from collections import defaultdict 
import sys

total = 0
counts = defaultdict(lambda : 0)

for line in iter(sys.stdin.readline, ""):
    words = line.rstrip('\n').split(' ')
    words.append("</s>")
    for w in words:
        counts[w] += 1
        total += 1

for word, count  in sorted(counts.items(), key=lambda x:x[1], reverse=True):
    probability = float(count) / total
    print "%-35s %.15f" % (word, probability)


