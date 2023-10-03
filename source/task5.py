import math
import re
import pandas as pd
from pymystem3 import Mystem
import numpy as np

import os


def get_lemmas_order():
    lemmas = set()
    for i in range(100):
        file = open('lemma_metrics/{}.txt'.format(i))
        for line in file:
            (lemma, metrics) = line.split(': ')
            lemmas.add(lemma)

    return sorted(lemmas)


def load_lemmas_order():
    file = open('model/order.txt')
    return [line.replace('\n', '') for line in file.readlines()]


def get_lemma_metrics(index):
    file = open('lemma_metrics/{}.txt'.format(index))
    d = {}
    for line in file:
        (lemma, metrics) = line.split(': ')
        (tf, tf_idf) = metrics.split(' ')
        d[lemma] = tf_idf

    return d


def fulfill_metrics(metrics, order):
    for lemma in order:
        if lemma not in metrics:
            metrics[lemma] = 0

    return metrics


def save_fullfiled_metrics():
    order = get_lemmas_order()
    try:
        os.mkdir('model')
    except FileExistsError:
        pass
    file = open('model/order.txt', 'w')
    file.write('\n'.join(order))

    for i in range(100):
        metrics = get_lemma_metrics(i)
        metrics = fulfill_metrics(metrics, order)
        metrics_file = open('model/{}.txt'.format(i), 'w')
        for lemma in order:
            metrics_file.write('{}\n'.format(metrics[lemma]))


def load_model():
    order = load_lemmas_order()
    arr = np.zeros((100, len(order)))
    for i in range(100):
        file = open('model/{}.txt'.format(i))
        metrics = [float(line.replace('\n', '')) for line in filter(lambda s: s != '\n', file.readlines())]
        arr[i] = np.array(metrics)

    return arr


def get_lemma_idf():
    file = open('inverted_index.txt')
    ind = {}
    for line in file:
        (lemma, docs) = line.split(': ')
        ind[lemma] = math.log(100 / len(docs.split(' ')))
    return ind


def get_metrics(query, order, lemma_idf):
    tf_dict = {}
    for lemma in query:
        if lemma not in tf_dict:
            tf_dict[lemma] = 0
        tf_dict[lemma] += 1 / len(query)

    for lemma in order:
        if lemma not in tf_dict:
            tf_dict[lemma] = 0

    metrics = np.array([tf_dict[lemma] * lemma_idf[lemma] for lemma in order])

    return metrics


def get_dist(list1, list2):
    top = sum([a * b for a, b in zip(list1, list2)])

    def get_bottom_elem(l):
        return math.sqrt(sum([elem ** 2 for elem in l]))

    bottom = get_bottom_elem(list1) * get_bottom_elem(list2)
    if bottom == 0:
        bottom = 1

    return top / bottom


def get_near_docs(metrics, model, df):
    for i in range(100):
        df.at[i, 'dist'] = get_dist(metrics, model[i])
    return df


def process_query(query):
    m = Mystem()
    text_lemmas = list(
        filter(
            lambda t: not re.match('[\s]*$', t),
            m.lemmatize(query)
        )
    )
    order = load_lemmas_order()
    lemma_idf = get_lemma_idf()
    metrics = get_metrics(text_lemmas, order, lemma_idf)
    model = load_model()

    df = pd.read_csv('index.csv', sep=';', names=['file', 'url', 'dist'])
    df = get_near_docs(metrics, model, df)

    return list(df.sort_values(by=['dist'], ascending=False)['url'])