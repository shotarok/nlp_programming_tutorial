# -*- coding:utf-8 -*-

from collections import defaultdict
import math
import sys
import codecs

sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def load_model(probability, model_filename = 'model.txt'):
    fin = codecs.open(model_filename, 'r', 'utf-8')
    for line in iter(fin.readline, ""):
        ngram_and_prob = line.rstrip('\n').split()
        prob  = ngram_and_prob.pop()
        ngram = " ".join(ngram_and_prob)
        probability[ngram] = float(prob)

def Vidabi(probability):

    # constant value
    INF = 10 ** 10
    LAMBDA_KNOWN = 0.95
    LAMBDA_UNKNOWN = 1 - LAMBDA_KNOWN
    V = 10 ** 6

    for line in iter(sys.stdin.readline, ""):

        # initialize
        line = line.rstrip()
        ary_size = len(line) + 1
        best_edge = [None] * ary_size
        best_score = [0.0] * ary_size

        # calc vidabi algorithm
        # Forward Procedure
        for word_end in range(1, ary_size):
            best_score[word_end] = INF
            for word_begin in range(0, word_end):
                word = line[word_begin:word_end]
                if (word in probability) or (len(word) == 1):
                    # calc probability
                    prob = float(LAMBDA_UNKNOWN) / V
                    prob += probability[word] * LAMBDA_KNOWN
                    my_score = best_score[word_begin] - float(math.log(prob, 2))

                    if my_score < best_score[word_end]:
                        best_score[word_end] = my_score
                        best_edge[word_end] = (word_begin, word_end)
                        
        # BackWard Procedure
        words = []
        next_edge = best_edge[len(best_edge)-1]
        while next_edge is not None:
            word = line[next_edge[0]:next_edge[1]]
            words.append(word)
            next_edge = best_edge[next_edge[0]]
        words.reverse()
        print " ".join(words)

if __name__ == "__main__":
    
    # load model file
    probability = defaultdict(lambda : 0.0 )
    load_model(probability)

    # run Vidabi
    Vidabi(probability)

