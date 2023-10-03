import os
import re
import threading
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from pymystem3 import Mystem

frame = pd.read_csv('index.csv', sep=';', names=['file', 'url'])

cachedStopWords = stopwords.words("russian")


def prepare_file(filename):
    tokens = {}
    lemmas = {}
    print('Начало обработки "{}.txt"\n'.format(filename))
    file = open('files/{}.txt'.format(filename))
    for line in file:
        texts = re.split('<.*>', line)
        for text in texts:
            text = text.translate(str.maketrans('', '', string.punctuation + '—'))
            raw_tokens = list(
                filter(
                    lambda raw_token:
                    raw_token not in cachedStopWords
                    and not re.match('^[0-9.\s]*$', raw_token)
                    and 'srchttps' not in raw_token
                    and 'alt' not in raw_token
                    and 'title' not in raw_token
                    and 'height' not in raw_token
                    and 'width' not in raw_token,
                    word_tokenize(text)
                )
            )
            m = Mystem()
            text_lemmas = list(
                filter(
                    lambda t: not re.match('[\s]*$', t),
                    m.lemmatize(' '.join(raw_tokens))
                )
            )
            for j in range(len(text_lemmas)):
                lemma = text_lemmas[j]
                if len(raw_tokens) > j:
                    token = raw_tokens[j]
                    if token not in tokens:
                        tokens[token] = 0
                    tokens[token] += 1
                    if m.lemmatize(token)[0] == lemma:
                        if lemma not in lemmas:
                            lemmas[lemma] = []
                        if token not in lemmas[lemma]:
                            lemmas[lemma].append(token)

    tokens_file = open('tokens/{}.txt'.format(filename), 'w')
    total_tokens = sum(tokens.values())
    tokens_file.write('{}\n'.format(total_tokens))
    for token in tokens.keys():
        tokens_file.write('{}: {}\n'.format(token, tokens[token]))

    lemmas_file = open('lemmas/{}.txt'.format(filename), 'w')
    for lemma in lemmas.keys():
        lemmas_file.write('{}: {}\n'.format(lemma, ' '.join(lemmas[lemma])))
    print('"{}.txt" обработан\n'.format(filename))


def prepare_arr_file(files):
    for j in range(len(files)):
        prepare_file(list(files)[j])


filenames = frame['file']
thread_num = 10
threads = []

try:
    os.mkdir('tokens')
    os.mkdir('lemmas')
except FileExistsError:
    pass

for i in range(thread_num):
    size = int(len(filenames) / thread_num)
    cut = filenames[int(i * size):int((i + 1) * size)]
    thread = threading.Thread(target=prepare_arr_file, args=(cut,))
    thread.start()
    threads.append(thread)
