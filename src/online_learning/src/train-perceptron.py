# -*- coding:utf-8 -*-

from collections import defaultdict
import create_features as cf
import predict_one as po
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

def margin_learning(weight, margin):
    last = defaultdict(lambda : 0)
    for index, line in enumerate(iter(sys.stdin.readline, "")):
        label, sent = get_label_and_sentence(line)
        phi = cf.create_features(sent)
        val = po.get_score(weight, phi,
                           FLAGS.l1_value,
                           index, last) * float(label)
        if val <= margin:
            update_weights(weight, phi, int(label))
            
def average_learning(weight):
    updates = 0.0
    average = defaultdict(lambda : 0.0)
    for line in iter(sys.stdin.readline, ""):
        label, sent = get_label_and_sentence(line)
        phi = cf.create_features(sent)
        pre_label = po.predict_one(weight, phi)
        if int(pre_label) != int(label):
            update_weights(weight, phi, int(label))
        updates += 1.0
        for key, value in weight.items():
            average[key] = (average[key] * (updates - 1.0) + value) / updates
    # copy to weight from average
    for key in weight.keys():
        weight[key] = average[key]
    
def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, argv[0], FLAGS)
        sys.exit(1)

    weight = defaultdict(lambda : 0.0)
    if FLAGS.use_average:
        average_learning(weight)
    elif FLAGS.use_margin > 0.0:
        margin_learning(weight, FLAGS.use_margin)
    else:
        learning(weight)
    for key, value in weight.items():
        print "%s %.12f"  % (key, value)   
    
if __name__ == "__main__":
    main(sys.argv)
