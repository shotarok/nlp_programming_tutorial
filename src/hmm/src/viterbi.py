# -*- coding:utf-8 -*-

from collections import defaultdict
import sys
import math

def load(transition, emission, possible_tags):
    model_filepath = "model.txt"
    fin = open(model_filepath)
    for line in iter(fin.readline, ""):
        (type_name, context, word, prob) = line.rstrip('\n').split()

        possible_tags[context] = True             
        prob = float(prob)
        if type_name == "T":
            transition[context + " " + word] = prob
        else:
            emission[context + " " + word] = prob
    fin.close()

def viterbi():

    # prepare variables
    transition = defaultdict(lambda : 1.0)
    emission = defaultdict(lambda : 0.0)
    possible_tags = defaultdict(lambda : 0.0)
    load(transition, emission, possible_tags)
    
    # forward step
    for line in iter(sys.stdin.readline, ""):

        words = line.rstrip("\n").split()
        length = len(words)
        best_score = {}
        best_edge = defaultdict(lambda : None)
        best_score["0 <s>"] = 0.0
        best_edge["0 <s>"] = None

        for i in range(0, length+1):
            for prev_tag in possible_tags.keys():
                for next_tag in possible_tags.keys():

                    if i == length:
                        next_tag = "</s>"
                    score_key = "%d %s" % (i, prev_tag)
                    trans_key = "%s %s" % (prev_tag, next_tag)
                    next_score_key = "%d %s" % (i+1, next_tag)
                    emit_key = ""
                    if i != length:
                        emit_key = "%s %s" % (next_tag, words[i])

                    if best_score.has_key(score_key) and transition.has_key(trans_key):
                        score = best_score[score_key]
                        score -= math.log(transition[trans_key])
                        score -= math.log(0.95 * emission[emit_key] + 0.05 / 10**6)
                        
                        if not best_score.has_key(next_score_key) or best_score[next_score_key] > score:
                            best_score[next_score_key] = score
                            best_edge[next_score_key] = score_key
                            
                    if i == length:
                        break

        # backward step
        tags = []
        last_key = "%d </s>" % (length+1)
        first_edge = "0 <s>"
        next_edge = best_edge[last_key]
        while next_edge != first_edge:
            (position, tag) = next_edge.split()
            tags.append(tag)
            next_edge = best_edge[next_edge]

        tags.reverse()
        print " ".join(tags)

if __name__ == "__main__":
    viterbi()
