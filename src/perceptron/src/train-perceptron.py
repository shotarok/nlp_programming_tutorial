# -*- coding:utf-8 -*-

import sys
from collections import defaultdict
import create_features as cf
import predict_one as po

def get_label_and_sentence(line):
    parts = line.rstrip().split()
    label = parts.pop(0)
    sentence = " ".join(parts)
    return (label, sentence)

def update_weights(w, phi, y):
    for name, value in phi.items():
        w[name] += value * y
    
def learning(weight):
    for line in iter(sys.stdin.readline, ""):
        label, sent = get_label_and_sentence(line)
        phi = cf.create_features(sent)
        pre_label = po.predict_one(weight, phi)
        if int(pre_label) != int(label):
            update_weights(weight, phi, int(label))

if __name__ == "__main__":
    weight = defaultdict(lambda : 0.0)
    learning(weight)
    for key, value in weight.items():
        print "%s %.12f"  % (key, value)
        

