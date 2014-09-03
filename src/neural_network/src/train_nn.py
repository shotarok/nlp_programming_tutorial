# -*- coding:utf-8 -*-

from collections import defaultdict
from random import uniform, seed
from umsgpack import packb
import create_features as cf
import predict_nn as nn
import gflags
import sys

import copy

FLAGS = gflags.FLAGS
LEARNING_RATE = 0.8

def get_label_and_sentence(line):
    parts = line.rstrip().split()
    label = parts.pop(0)
    sentence = " ".join(parts)
    return (label, sentence)

def update_weights(w, phi, y):
    for name, value in phi.items():
        w[name] += value * y

def update_nn(network, phi, true_label):
    delta = {}
    result, y  = nn.predict_nn(network, phi)
    # make network reverse for learning
    network.reverse()
    is_last = True
    for (name, layer, weight) in network:
        if is_last:
            is_last = False
            delta[name] = float(true_label) - float(result)
        else:
            coefficient = (1.0 - pow(y[layer][name], 2))
            tmp = 0.0
            for (pre_name, pre_layer, pre_weight) in network:
                if layer + 1 == pre_layer:
                    tmp += delta[pre_name] * pre_weight[name]
            delta[name] = coefficient * tmp

    for (node_name, layer, weight) in network:
        for name, val in y[layer-1].items():
            weight[name] += LEARNING_RATE * delta[node_name] * val
        
    # make network original order
    network.reverse()
    
def learning(network):
    lines = sys.stdin.readlines()
    for i in range(FLAGS.iteration):
        sys.stdout.write("\rIteration:%d" % (i+1))
        sys.stdout.flush()
        for line in lines:
            label, sent = get_label_and_sentence(line)
            phi = cf.create_features(sent)
            update_nn(network, phi, label)

def get_radom_weight():
    return defaultdict(lambda : uniform(-1.0, 1.0))
                   
def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, argv[0], FLAGS)
        sys.exit(1)

    SEED = 10
    seed(SEED)
    network = [
        (0, 1, get_radom_weight()),
        (1, 1, get_radom_weight()),
        (2, 1, get_radom_weight()),
        (3, 2, get_radom_weight())
    ]

    learning(network)

    fout = open(FLAGS.model_file, "w")
    fout.write(packb(network))
    fout.close()
    
if __name__ == "__main__":
    gflags.DEFINE_integer('iteration', 10,
                          'The number of iteration.')
    gflags.DEFINE_string('model_file',
                         'model.txt',
                         'Use model file path.')
    main(sys.argv)
