# -*- coding:utf-8 -*-

from collections import defaultdict
import sys


TRANSITiON_FILENAME = "transition_prob.txt"
EMIT_FILENAME = "emit_prob.txt"

def learn():

    # constant value
    LAMBDA_KNOWN = 0.95
    LAMBDA_UNKNOWN = 1 - LAMBDA_KNOWN
    V = 10 ** 6

    # prepare variables
    emit = defaultdict(lambda : 0)
    transition = defaultdict(lambda : 0)
    context = defaultdict(lambda : 0)

    # calc the frequencies
    for line in iter(sys.stdin.readline, ""):
        previous = "<s>"
        context[previous] += 1
        word_tags = line.rstrip('\n').split()
        for wordtag in word_tags:
            (word, tag) = wordtag.split("_")
            transition[previous + " " + tag] += 1
            context[tag] += 1
            emit[tag + " " + word] += 1
            previous = tag
        transition[previous + " </s>"] += 1

    # output trainsition prob
    for key, value in transition.items():
        (previous, word) = key.split()
        print "T", key, float(value)/context[previous]

    # output emit prov
    for key, value in emit.items():
        (tag, word) = key.split()
        prob = LAMBDA_KNOWN * float(value)/context[tag] + LAMBDA_UNKNOWN * 1.0 / float(V)
        # prob = float(value)/context[tag]
        print "E", key, prob
        
if __name__ == "__main__":
    learn()

        
        
