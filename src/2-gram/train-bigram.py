#! /usr/bin/env python
# -*- coding:utf-8 -*-

from collections import defaultdict
import sys

context_counts = defaultdict(lambda: 0)
counts = defaultdict(lambda: 0)

for line in iter(sys.stdin.readline, ""):
    words = line.rstrip('\n').split()
    words.append("</s>")
    words.insert(0,"<s>")

    # from '<s>' until a previous word of '</s>'
    for i in range(1, len(words)-1):
        bi_gram = " ".join(words[(i-1):i+1])
        counts[bi_gram] += 1
        context_counts[words[i-1]] += 1
        counts[words[i]] += 1
        context_counts[""] += 1

for n_gram, count in counts.items():
    words = n_gram.split(' ')
    words.pop()
    context = " ".join(words)
    prob = float(count) / context_counts[context]
    print "%-30s %.15f" % (n_gram, prob)

