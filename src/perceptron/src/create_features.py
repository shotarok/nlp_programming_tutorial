# -*- coding:utf-8 -*-

from collections import defaultdict

def create_features(sentence):
    phi = defaultdict(lambda : 0)
    words = sentence.rstrip().split()
    # add uni-gram
    for w in words:
        phi["UNI:" + w] += 1
    return phi

if __name__ == '__main__':
    sentence = "hello world"
    phi = create_features(sentence)
    for key, value in phi.items():
        print key, value
        
