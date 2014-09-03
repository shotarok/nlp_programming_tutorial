#! /usr/bin/env python

from collections import defaultdict
from umsgpack import unpackb
from viterbi import viterbi
import gflags
import sys

FLAGS = gflags.FLAGS

def predict_one(weight, words, possible_tags, transition):
    return " ".join(viterbi(weight, words, possible_tags, transition))
    
def predict_all(weight, possible_tags, transition):
    for line in iter(sys.stdin.readline, ""):
        words = line.split()
        print predict_one(weight, words, possible_tags, transition)
    
def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, argv[0], FLAGS)
        sys.exit(1)

    w_binary, p_binary, t_binary = "", "", ""
    try:
        fin = open(FLAGS.model_file, "r")
        w_binary = fin.read()
        fin.close()
        fin = open(FLAGS.possible_tags_file, "r")
        p_binary = fin.read()
        fin.close()
        fin = open(FLAGS.transition_file, "r")
        t_binary = fin.read()
        fin.close()
    except IOError:
        print "Error: %s does not appear to exist." % (FLAGS.model_file)
        exit(0)

    possible_tags = unpackb(p_binary)
    w_hash = unpackb(w_binary)
    weight = defaultdict(lambda : 0.0)
    transition = unpackb(t_binary)
    for k, v in w_hash.items():
        weight[k] = v
    predict_all(weight, possible_tags, transition)

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
    main(sys.argv)
