# -*- coding:utf-8 -*-

import sys
import predict_one as po
import create_features as cf
from collections import defaultdict


def predict_all(model_file):
    weight = defaultdict(lambda : 0.0)

    # load model_file
    fin = open(model_file)
    for line in iter(fin.readline, ""):
        parts = line.rstrip("\n").split()
        value = parts.pop()
        name  = " ".join(parts)
        weight[name] = float(value)
    fin.close()

    # predict all
    for line in iter(sys.stdin.readline, ""):
        phi = cf.create_features(line)
        y   = po.predict_one(weight, phi)
        print y

if __name__ == "__main__":
    model_file = "model.txt"
    predict_all(model_file)
    
