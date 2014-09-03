# -*- coding:utf-8 -*-

from collections import defaultdict
import sys
import math
import codecs

sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def tm_load(transition, model_filepath = "model.txt"):
    fin = codecs.open(model_filepath, 'r', 'utf-8')
    for line in iter(fin.readline, ""):
        (type_name, word, pron, prob) = line.rstrip('\n').split(' ')
        prob = float(prob)
        if type_name == "E":
            transition[pron][word] = prob
    fin.close()

def lm_load(probability, model_filepath = 'model.txt'):
    fin = codecs.open(model_filepath, 'r', 'utf-8')
    for line in iter(fin.readline, ""):
        ngram_and_prob = line.rstrip('\n').split()
        prob  = ngram_and_prob.pop()
        ngram = " ".join(ngram_and_prob)
        probability[ngram] = float(prob)

def better_than(lhs, rhs):
    return lhs < rhs
        
def get_word(index, best_score):
    tmp_score, word = None, ""
    for w, s in best_score[index].items():
        # print "(w):", w, "(s):", s
        if tmp_score is None or better_than(s, tmp_score):
            tmp_score = s
            word = w
    # print "(word):", word,
    # print "(index):", index
    return word
    
def backward(best_edge, best_score, line):
    words = []
    word = get_word(len(line), best_score)
    next_edge = best_edge[len(line)][word]
    # print word    
    while next_edge is not None:
        words.append(word)
        word = get_word(next_edge[0], best_score)
        # print word
        next_edge = best_edge[next_edge[0]][word]
    words.reverse()
    return " ".join(words)
        
def forward(line, tm_probs, lm_probs):

    line = line.rstrip('\n')
    length = len(line)
    best_score = defaultdict(lambda : defaultdict(lambda : None))
    best_edge = defaultdict(lambda : defaultdict(lambda : None))
    best_score[0]["<s>"] = 0.0
    best_edge[0]["<s>"] = None

    for end in range(length + 1):
        for begin in range(0, end):
            pron = line[begin:end]
            my_tm = tm_probs[pron]
            if not my_tm and len(pron) == 1:
                my_tm[pron] = 0.0

            # print "(pron):", pron
            # print "(my_tm):", " ".join([i[0] for i in my_tm.items()])

            for curr_word, tm_prob in my_tm.items():
                for prev_word, prev_score in best_score[begin].items():
                    get_lm_prob = lambda : lm_probs[prev_word + " " + curr_word] * 0.95 + (1.0 / 10 ** 6) * 0.05
                    # print curr_word + " " + prev_word, tm_prob, get_lm_prob(), tm_prob * get_lm_prob()
                    prob = float(tm_prob * get_lm_prob())
                    if tm_prob == 0.0:
                        # for log(tm_prob) = 0.0                        
                        #continue
                        prob = float(get_lm_prob())
                        
                    curr_score = prev_score - math.log(prob)
                    if (best_score[end][curr_word] is None) or better_than(curr_score, best_score[end][curr_word]):
                        # print "(curr_word):", curr_word, 
                        # print "(begin:end)", (begin, end)
                        best_score[end][curr_word] = curr_score
                        best_edge[end][curr_word] = (begin, end)

    return backward(best_edge, best_score, line)

def kcc():

    TM_FILE, LM_FILE = "tm.txt", "lm.txt"
    tm_probs = defaultdict( lambda : {} )
    lm_probs = defaultdict( lambda : 0.0)
    
    tm_load(tm_probs, TM_FILE)
    lm_load(lm_probs, LM_FILE)
    # for k, v in tm_probs.items():
    #     print k, " ".join(v.keys())

    for line in iter(sys.stdin.readline, ""):
        print forward(line, tm_probs, lm_probs)
        
    
if __name__ == "__main__":
    
    kcc()
