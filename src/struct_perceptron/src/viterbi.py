#! usr/bin/env python

from collections import defaultdict
from create_feature import add_trans
from create_feature import add_emit

def get_score(weight, prev, curr, word):
    phi, score = {}, 0.0
    add_trans(phi, prev, curr)
    add_emit(phi, curr, word)
    for k in phi.keys():
        score += weight[k]
    return score

def viterbi(weight, words, possible_tags, transition):
    words.append("</s>")
    length_of_words = len(words)
    best_score, best_edge = {}, {}
    first_tag = "0 <s>"
    best_score[first_tag] = 0
    best_edge[first_tag] = None
    # forward step
    for i in range(length_of_words):
        for prev in possible_tags:
            for curr in possible_tags:
                score_tag = "%d %s" % (i, prev)
                trans_tag = "%s %s" % (prev, curr)
                if (best_score.has_key(score_tag) and
                    trans_tag in transition):
                    score = best_score[score_tag]
                    score += get_score(weight, prev, curr, words[i])
                    new_score_tag = "%d %s" % (i+1, curr)
                    if ((not best_score.has_key(new_score_tag)) or
                        best_score[new_score_tag] < score):
                        best_score[new_score_tag] = score
                        best_edge[new_score_tag] = score_tag
    # backward step
    tags = []
    last_tag = "%d </s>" % (length_of_words)
    next_tag = best_edge[last_tag]
    while next_tag != first_tag:
        (position, tag) = next_tag.split()
        tags.append(tag)
        next_tag = best_edge[next_tag]
    tags.reverse()
    return tags
