#! /usr/bin/env python
# -*- coding:utf-8 -*-

from collections import defaultdict
import sys
import math

def load_model(probability, model_filename = 'model.txt'):
    fin = open(model_filename)
    for line in iter(fin.readline, ""):
        ngram_and_prob = line.rstrip('\n').split()
        prob  = ngram_and_prob.pop()
        ngram = " ".join(ngram_and_prob)
        probability[ngram] = float(prob)

def calculate_entropy(prob, lambda_one, lambda_two):
    V = 10 ** 6
    H = 0.0
    W = 1
    for line in iter(sys.stdin.readline, ""):
        words = line.rstrip('\n').split()
        words.append("</s>")
        for i in range(1, len(words)-1):
            bigram = " ".join(words[(i-1):i+1])
            word   = words[i]
            # print "bigram:" + bigram, "word" + word, "prob:",  prob[word]
            P_1 = lambda_one * prob[word] + float(1 - lambda_one) / V
            P_2 = lambda_two * prob[bigram] + float(1 - lambda_two) * P_1
            H -= float(math.log(P_2, 2))
            W += 1
    entropy = (H/W)
    # print  "lambda_one", "lambda_two", "entropy"
    print  "%.2f       %.2f       %f" % (lambda_one, lambda_two, entropy)
            
if __name__ == '__main__':
    probability = defaultdict(lambda : 0.0)
    lambda_one  = 0.95
    lambda_two  = 0.95

    if len(sys.argv) > 2:
        lambda_one = float(sys.argv[1])
        lambda_two = float(sys.argv[2])
        
    load_model(probability)
    calculate_entropy(probability, lambda_one, lambda_two)


    
