# -*- coding:utf-8 -*-

from collections import defaultdict
import sys
import math
import numpy as np
import codecs

sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

class LDA:

    def sample_one(self, probs):
        z = sum(probs)
        remainnig = np.random.uniform(0.00, z)

        for index, value in enumerate(probs):
            remainnig -= value
            if remainnig <= 0:
                return index
        # error
        return -1

    def add_counts(self, word, topid, docid, amount):
        topid = str(topid)
        docid = str(docid)
        self.xcounts[topid] += amount
        self.xcounts[word + "|" + topid] += amount
        self.ycounts[docid] += amount
        self.ycounts[topid + "|" + docid] += amount
        return

    def __init__(self):

        # initialize const variables
        self.NUM_TOPIC = 2
        self.ITERATION = 10 ** 2
        self.ALPHA = 0.08
        self.BETA = 0.08

        # initialize variables
        self.xcounts = defaultdict(lambda : 0.0)
        self.ycounts = defaultdict(lambda : 0.0)
        self.N = defaultdict(lambda : set())
        self.xcorpus = []
        self.ycorpus = []

        # load data
        for line in iter(sys.stdin.readline, ""):
            docid = len(self.xcorpus)
            words = line.rstrip('\n').split()
            topics = []
            for word in words:
                topid = int(np.random.uniform(0.00, self.NUM_TOPIC+0.01))
                topics.append(topid)
                self.add_counts(word, topid, docid, 1)
                self.N[word].add(topid)
                self.N[topid].add(docid)
            self.xcorpus.append(words)
            self.ycorpus.append(topics)
        return

    def calc_word_prob(self, word, topid):
        prob = self.xcounts[word + "|" + topid] + self.ALPHA
        prob /= self.xcounts[topid] + self.ALPHA * len(self.N[word])
        return prob

    def calc_topic_prob(self, topid, docid):
        prob = self.ycounts[topid + "|" + docid] + self.BETA
        prob /= self.ycounts[docid] + self.BETA * len(self.N[topid])
        return prob
        
    def learn(self):
        # Gibbs Sampling
        corpus_size = len(self.xcorpus)
        for step in range(self.ITERATION):
            loglikehood = 0.0
            for i in range(0, corpus_size):
                line_size = len(self.xcorpus[i])
                for j in range(0, line_size):
                    x = self.xcorpus[i][j]
                    y = self.ycorpus[i][j]
                    self.add_counts(x, y, i, -1)
                    probs = []
                    for k in range(self.NUM_TOPIC):
                        prob = self.calc_word_prob(x, str(y))
                        prob *= self.calc_topic_prob(str(y), str(i))
                        probs.append(prob)
                    new_y = self.sample_one(probs)
                    loglikehood += math.log(probs[new_y])
                    self.add_counts(x, new_y, i, 1)
                    self.ycorpus[i][j] = new_y
            print "(step:%04d) %f" %(step, loglikehood)

    def output(self):
        print self.xcorpus
        print self.ycorpus
                    
                
if __name__ == "__main__":
    print "start to init."
    lda = LDA()
    print "init done."
    print "start to learn."
    lda.learn()
    print "learning done."
    lda.output()
