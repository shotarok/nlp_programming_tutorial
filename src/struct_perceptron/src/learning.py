#! /usr/bin/env python

from collections import defaultdict
from create_feature import create_feature
from random import uniform, seed
from umsgpack import packb
from viterbi import viterbi
import sys
import gflags

FLAGS = gflags.FLAGS

def union_keys(dic1, dic2):
    s1 = set(dic1.keys())
    s2 = set(dic2.keys())
    return s1.union(s2)

def update_weight(w, phi_prime, phi_hat):
    keys = union_keys(phi_prime, phi_hat)
    for k in keys:
        w[k] += phi_prime[k] - phi_hat[k]
    
def learning(T):
    weight = defaultdict(lambda : uniform(-1.0, 1.0))
    data = []
    possible_tags, transition = set(["<s>", "</s>"]), set()
    for line in iter(sys.stdin.readline, ""):
        X, Y = [], []
        pre_y = "<s>"
        for x_y in line.rstrip().split():
            (x, y) = x_y.split('_')
            X.append(x)
            Y.append(y)
            possible_tags.add(y)
            transition.add(" ".join([pre_y, y]))
            pre_y = y
        transition.add(" ".join([pre_y, "</s>"]) )
        data.append((X, Y))
    data_size = len(data)
    for t in range(T):
        for line_num, (X, Y_prime) in enumerate(data):
            sys.stdout.write("\rIteration %d, linenum %d / %d" % (t+1, line_num+1, data_size))
            sys.stdout.flush()
            Y_hat = viterbi(weight, X, possible_tags, transition)
            phi_prime = create_feature(X, Y_prime)
            phi_hat = create_feature(X, Y_hat)
            update_weight(weight, phi_prime, phi_hat)
    return (weight, possible_tags, transition)

def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, argv[0], FLAGS)
        sys.exit(1)

    weight, possible_tags, transition = learning(FLAGS.iteration)

    fout = open(FLAGS.model_file, "w")
    fout.write(packb(weight))
    fout.close()
    fout = open(FLAGS.possible_tags_file, "w")
    fout.write(packb(list(possible_tags)))
    fout.close()
    fout = open(FLAGS.transition_file, "w")
    fout.write(packb(list(transition)))
    fout.close()
    
if __name__ == "__main__":
    gflags.DEFINE_string('model_file',
                         'model.txt',
                         'model file path.') 
    gflags.DEFINE_string('possible_tags_file',
                         'possible_tags.txt',
                         'possible tags file path.')
    gflags.DEFINE_string('transition_file',
                         'transition.txt',
                         'possible transition file path.')
    gflags.DEFINE_integer('iteration', 10,
                         'The number of iteration of learning.')
    SEED = 10
    seed(SEED)
    main(sys.argv)
