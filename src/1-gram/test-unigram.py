#! /usr/bin/env python
# -*- coding:utf-8 -*-

import math
import sys

lambda_known = 0.95
lambda_unkwn = 1.0 - lambda_known

test_total = 0
log_likelihood = 0.0
unknown_total = 0
smoothing_value = 10 ** 6

probability = {}
model_filename = "test-model.txt"
if len(sys.argv) > 1:
    model_filename = sys.argv[1]

# set probability from model.txt
fin = open(model_filename)
for line in iter(fin.readline, ""):
    word, prob = line.rstrip('\n').split()
    probability[word] = float(prob)
fin.close()

# calculate Entropy and Coverrage
for line in iter(sys.stdin.readline, ""):

    words = line.rstrip('\n').split()
    # append </s>
    words.append( "</s>")

    for word in words:
        test_total += 1
        # use prob of a known word as defalut value.
        prob = float(lambda_unkwn) / smoothing_value
        if word in probability:
            prob += probability[word] * lambda_known
        else:
            unknown_total += 1

        # print word, prob, float(math.log(prob, 2))
        log_likelihood -= float(math.log(prob, 2))

print test_total        
        
print "entropy = %5f" % (log_likelihood / test_total)
print "coverage = %5f" % (float(test_total - unknown_total)/ test_total)


