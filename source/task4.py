import math
import os

try:
    os.mkdir('token_metrics')
    os.mkdir('lemma_metrics')
except FileExistsError:
    pass

token_idf_dict = {}
lemma_idf_dict = {}

for i in range(100):
    token_file = open('tokens/{}.txt'.format(i))
    lines = token_file.readlines()
    for j in range(1, len(lines)):
        line = lines[j]
        (token, freq) = line.split(': ')
        if token not in token_idf_dict:
            token_idf_dict[token] = []
        token_idf_dict[token].append(i)

for key in token_idf_dict.keys():
    token_idf_dict[key] = math.log(100 / len(token_idf_dict[key]))

for i in range(100):
    lemma_file = open('lemmas/{}.txt'.format(i))
    for line in lemma_file:
        (lemma, tokens) = line.split(': ')
        if lemma not in lemma_idf_dict:
            lemma_idf_dict[lemma] = []
        lemma_idf_dict[lemma].append(i)

for key in lemma_idf_dict.keys():
    lemma_idf_dict[key] = math.log(100 / len(lemma_idf_dict[key]))

for i in range(100):
    token_file = open('tokens/{}.txt'.format(i))
    token_metrics_file = open('token_metrics/{}.txt'.format(i), 'w')
    lines = token_file.readlines()
    total = int(lines[0])
    for j in range(1, len(lines)):
        (token, freq) = lines[j].split(': ')
        tf = int(freq) / total
        idf = token_idf_dict[token]
        token_metrics_file.write('{}: {} {}\n'.format(token, tf, tf * idf))

for i in range(100):
    token_file = open('tokens/{}.txt'.format(i))
    lemma_file = open('lemmas/{}.txt'.format(i))
    lemma_metrics_file = open('lemma_metrics/{}.txt'.format(i), 'w')
    token_dict = {}
    lines = token_file.readlines()
    total = int(lines[0])
    for j in range(1, len(lines)):
        (token, freq) = lines[j].split(': ')
        if token not in token_dict:
            token_dict[token] = 0
        token_dict[token] =  int(freq)
    for line in lemma_file:
        (lemma, tokens) = line.replace('\n', '').split(': ')
        tokens = tokens.split(' ')
        freqs = list(map(lambda t: token_dict[t], tokens))
        tf = sum(freqs) / total
        idf = lemma_idf_dict[lemma]
        lemma_metrics_file.write('{}: {} {}\n'.format(lemma, tf, tf * idf))


