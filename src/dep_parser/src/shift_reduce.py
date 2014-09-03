#! /usr/bin/env python

import dparser_util as util
from make_feature import make_feature

def get_action(feats, w_s, w_l, w_r, queue):
    feats = make_feature(stack, queue)
    score_s = get_score(feats, w_s)
    score_l = get_score(feats, w_l)
    score_r = get_score(feats, w_r)
    if score_s >= score_l and score_s >= score_r and len(queue) > 0:
        return util.SHIFT
    elif score_l >= score_s:
        return util.LEFT_REDUCE
    return util.RIGHT_REDUCE

def do_action(action, stack, queue, heads):
    if action == util.SHIFT:
        stack.append( queue.pop(0) )
    elif action == util.LEFT_REDUCE:
        heads[ stack[-1].id ] = stack[-1].id
        stack.pop(-2)
    elif action == util.RIGHT_REDUCE:
        heads[ stack[-1].id ] = stack[-2].id
        stack.pop()
    else:
        raise
    
def shift_reduce(queue, w_s, w_l, w_r):
    heads = []
    stack = [util.Token(0, util.ROOT, util.ROOT, None)]
    while len(queue) > 0 or len(stack) > 1:
        feats = make_feature(stack, queue)
        action = get_action(feats, w_s, w_l, w_r, queue)
        do_action(action, stack, queue, heads)
    return heads
            
