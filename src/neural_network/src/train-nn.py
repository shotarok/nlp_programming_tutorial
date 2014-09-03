# -*- coding:utf-8 -*-

from collections import defaultdict
import create_features as cf
import predict_nn as nn
import gflags
import sys

FLAGS = gflags.FLAGS
gflags.DEFINE_boolean('use_average', False, 'Use averaged perceptoron.' )
gflags.DEFINE_float('use_margin', 0.0, 'Use margin perceptoron.' )
gflags.DEFINE_float('l1_value', 0.0, 'Use L1 regularization.')

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
    
def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, argv[0], FLAGS)
        sys.exit(1)

    weight = defaultdict(lambda : 0.0)
    learning(weight)

    
if __name__ == "__main__":
    main(sys.argv)
