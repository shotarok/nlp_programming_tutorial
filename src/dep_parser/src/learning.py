#! /usr/bin/env python

import dparser_util as util
from make_feature import make_feature
from shift_reduce import get_action
from shift_reduce import do_action

def update_weight(feats, w_a, w_ca):
    for key, value in feats.keys():
        w_a[key] -= value
    for key, value in feats.keys():
        w_ca[key] += value

def get_weight_of(action, w_s, w_l, w_s):
    if action == util.SHIFT:
        return w_s
    elif action == util.LEFT_REDUCE:
        return w_l
    return w_r

def shift_reduce_train(queue, w_s, w_l, w_r):
    heads = []
    stack = [util.Token(0, util.ROOT, util.ROOT, util.ROOT)]
    while len(queue) > 0 or len(stack) > 1:
        feats = make_feature(stack, queue)
        action = get_action(feats, w_s, w_l, w_s, queue)
        correct_action = get_correct_action()
        if action != correct_action:
            w_a = get_weight_of(action, w_s, w_l, w_r)
            w_ca = get_weight_of(correct_action, w_s, w_l, w_r)
            update_weight(feats, w_a, w_ca)
            do_action(action, stack, queue, heads)
