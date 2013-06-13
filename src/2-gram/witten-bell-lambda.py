#! /usr/bin/env python
# -*- coding:utf-8 -*-

from collections import defaultdict
import sys

word_contexts = {}

for line in iter(sys.stdin.readline, ""):
    words = line.rstrip('\n').split()
    words.append("</s>")
    words.insert(0, "<s>")

    for i in range(1, len(words) -1):
        now = words[i]
        prv = words[i-1]
        if prv in word_contexts:
            word_contexts[prv][now] = 1
        else:
            word_contexts[prv] = {now: 1}

for word, context in word_contexts.items():
    print word, len(context)
