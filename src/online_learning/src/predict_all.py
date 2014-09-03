# -*- coding:utf-8 -*-

import sys
import predict_one as po
import create_features as cf
from collections import defaultdict
import gflags

FLAGS = gflags.FLAGS
gflags.DEFINE_string('model_file',
                     'model.txt',
                     'Use model file path.')

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
        print int(y)

if __name__ == "__main__":
    predict_all(FLAGS.model_file)
    
