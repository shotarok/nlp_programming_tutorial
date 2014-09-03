# -*- coding:utf-8 -*-

from collections import defaultdict
from random import random, seed
from umsgpack import unpackb
from math import copysign 
import sys
import predict_one as po
import create_features as cf
import gflags

FLAGS = gflags.FLAGS

def predict_all(network):
    # predict all
    for line in iter(sys.stdin.readline, ""):
        phi = cf.create_features(line)
        result, y = predict_nn(network, phi)
        # 1.0 * sign(result)
        print int(copysign(1, result))

def predict_nn(network, phi):

    max_layer = 1
    for (name, layer, weight) in network:
        max_layer = max(max_layer, layer)

    # Init y
    y = [{} for i in range(max_layer+1)]
    y[0] = phi

    # Run perceptron at each layer.
    for (name, layer, weight) in network:
        answer = po.predict_one(weight, y[layer-1])
        y[layer][name] = answer

    # The value of last layer is output of nn.
    last_perceptron_name = len(network)-1
    return (y[-1][last_perceptron_name], y)

def get_weight():
    return defaultdict(lambda : 0.0)
    
if __name__ == "__main__":
    gflags.DEFINE_string('model_file',
                         'model.txt',
                         'Use model file path.')
    bstr = ""
    try:
        fin = open(FLAGS.model_file, "r")
        bstr = fin.read()
        fin.close()
    except IOError:
        print "Error: %s does not appear to exist." % (FLAGS.model_file)
        exit(0)

    network = unpackb(bstr)
    for (name, layer, weight) in network:
        new_weight = get_weight()
        for key, val in weight.items():
            new_weight[key] = val
        network[name] = (name, layer, new_weight)
 
    predict_all(network)
