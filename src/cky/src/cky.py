
import sys
import gflags

from collections import defaultdict
from math import log

FLAGS = gflags.FLAGS
gflags.DEFINE_string('grammar_file',
                     'grammar.txt',
                     'Use grammar file.')
gflags.DEFINE_string('delimiter',
                     '#',
                     'Use a character as delimiter.')
START_SYMBOL = "S"
INFINITY = 1<<28

def load_grammar(nonterm, preterm, grammar_file):
    fin = open(grammar_file)
    for rule in iter(fin.readline, ""):
        (lhs, rhs, prob) = rule.split("\t")
        rhs_symbols = rhs.split(" ")
        prob = log(float(prob))
        if len(rhs_symbols) == 1:
            preterm[rhs].append((lhs, prob))
        else:
            nonterm.append((lhs, rhs_symbols[0],
                            rhs_symbols[1], prob))
    fin.close()

def get_key(ary):
    return FLAGS.delimiter.join(map(lambda x : str(x), ary))
    
def cky(nonterm, preterm):
    for line in iter(sys.stdin.readline, ""):
        words = line.rstrip().split(" ")
        best_score = defaultdict(lambda : -INFINITY)
        best_edge = {}

        # Preprocess for pre-terminate symbols
        for i in range(len(words)):
            for (lhs, log_prob) in preterm[words[i]]:
                key = get_key((lhs, i, i+1))
                best_score[key] = log_prob

        # Process for non-terminate symbols
        right_range = range(2, len(words)+1) # [2, ... , len(words)+1]
        for j in right_range:
            left_range = range(0, j-1) # [j-2, ..., 0]
            left_range.reverse()
            for i in left_range:
                middle_range = range(i+1, j) # [i+1, ..., j-1]
                for k in middle_range:
                    for (sym, lsym, rsym, log_prob) in nonterm:
                        left_key = get_key((lsym, i, k))
                        right_key = get_key((rsym, k, j))
                        if best_score[left_key] > -INFINITY and best_score[right_key] > -INFINITY:
                            this_log_prob = best_score[left_key] + best_score[right_key] + log_prob
                            key = get_key((sym, i, j))
                            if this_log_prob > best_score[key]:
                                best_score[key] = this_log_prob
                                best_edge[key] = (left_key, right_key)

        print_sexp(words, best_edge)

def print_sexp(words, best_edge):
    S = get_key((START_SYMBOL, 0, len(words)))
    print get_sexp(S, best_edge, words)

def get_sexp(sym_i_j, best_edge, words):
    (sym, i, j) = sym_i_j.split(FLAGS.delimiter)
    if best_edge.has_key(sym_i_j):
        edge = best_edge[sym_i_j]
        return "(%s %s %s)" % (sym,
                               get_sexp(edge[0], best_edge, words),
                               get_sexp(edge[1], best_edge, words))
    else:
        return "(%s %s)" % (sym, words[int(i)])
        
def main(argv):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, argv[0], FLAGS)
        sys.exit(1)

    nonterm = []
    preterm = defaultdict(lambda : [])
    load_grammar(nonterm, preterm, FLAGS.grammar_file)
    cky(nonterm, preterm)

if __name__ == '__main__':
    main(sys.argv)
