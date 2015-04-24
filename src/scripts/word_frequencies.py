#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, time, argparse, operator
from stop_words import *
from collections import Counter
from numpy import arange
from random import *
from math import *

def get_dir(dir_name, create_if_missing=False):
    if not os.path.exists(dir_name):
        if create_if_missing:
            os.makedirs(dir_name)
        else:
            print("unexisting dir '{}'".format(dir_name))
            exit()
    return dir_name


class Article:
    def __init__(self, filepath):
        self.filepath = filepath
        self.id = os.path.basename(self.filepath).split('.')[0]
        self.process()

    # count words and content words
    def process(self):
        self.words = Counter() # excluding <s> and </s>
        self.content_words = Counter() # only content words
        with open(self.filepath, 'r') as article_file:
            for line in article_file:
                for word in line.split():
                    word = word.lower()
                    if not is_delimeter(word):
                        self.words[word] += 1
                        if not is_stop(word):
                            self.content_words[word] += 1

    def get_most_frequent_word_prob(self):
        most_freq_content_words = self.content_words.most_common(1)[0][1]
        return most_freq_content_words / sum(self.content_words.values(), 0.0)


def get_entropy(counts):
    q = sum(counts.values(), 0.0)
    h = 0
    for word in counts:
        p_word = counts[word] / q
        h = p_word * log(p_word, 2)
    return h # should be negative

# corpus is train/dev; sub_dir is real/fake
def count_dir(corpus_dir, sub_dir_name):
    full_dir = os.path.join(corpus_dir, sub_dir_name)
    articles = {}
    for article in os.listdir(full_dir):
        article_filename = os.path.join(full_dir, article)
        if os.path.isdir(article_filename):
            continue
        article = Article(article_filename)
        articles[article.id] = article
        # if len(articles_counts) > 20: break
    return articles

def extract_features(article, feature_name):
    if feature_name == 'most_freq_content_word_prob':
        return article.get_most_frequent_word_prob()
    if feature_name == 'words_h':
        return get_entropy(article.words)
    if feature_name == 'content_words_h':
        return get_entropy(article.content_words)
    if feature_name == 'q_words':
        return sum(article.words.values(), 0.0)
    if feature_name == 'q_content_words':
        return sum(article.content_words.values(), 0.0)
    raise ValueError("unknown feature " + feature_name)

def get_optimal_threshold_from_train(directories):
    # train
    real = count_dir(directories.train_dir, directories.real_dir)
    fake = count_dir(directories.train_dir, directories.fake_dir)

    real_ratios = []
    for art_id in real:
        real_ratios.append(extract_feature(real[art_id], False))

    fake_ratios = []
    for art_id in fake:
        fake_ratios.append(extract_feature(fake[art_id], False))

    corpus_size = len(real_ratios) + len(fake_ratios)
    results = []
    for i in arange(0.018, 0.03, 0.0002):
        good = len([ratio for ratio in real_ratios if ratio >= i])
        good += len([ratio for ratio in fake_ratios if ratio < i])
        (threshold, accuracy) = (i, good / float(corpus_size))
        results.append((threshold, accuracy))
        print (threshold, accuracy)
    result = sorted(results, key=operator.itemgetter(1), reverse=True)[0]
    print "and the winner is... %f with a training accuracy of %f" % result
    return result[0]

def test_threshold_on_dev(threshold, directories):
    # dev
    real = count_dir(args.dev_dir, args.real_dir)
    fake = count_dir(args.dev_dir, args.fake_dir)

    real_ratios = []
    for art_id in real:
        real_ratios.append(extract_feature(real[art_id], False))

    fake_ratios = []
    for art_id in fake:
        fake_ratios.append(extract_feature(fake[art_id], False))

    corpus_size = len(real_ratios) + len(fake_ratios)
    good = len([ratio for ratio in real_ratios if ratio >= threshold])
    good += len([ratio for ratio in fake_ratios if ratio < threshold])
    accuracy = good / float(corpus_size)
    print "dev", threshold, accuracy

def generate_features_for_all(directories):
    for corpus_name in ('train', 'dev'):
        for class_name in ('real', 'fake'):
            generate_features(corpus_name, class_name, directories)


def generate_features(corpus_name, class_name, directories):
    features_dir = get_dir(directories.features_dir, False)
    directories = vars(directories)
    corpus_dir = directories[corpus_name + '_dir']
    class_dir = directories[class_name + '_dir']
    klass_articles = count_dir(corpus_dir, class_dir)
    for article in klass_articles:
        filename = "%s.%s.%s.f" % (corpus_name, class_name, article)
        for feature in 'most_freq_content_word_prob words_h content_words_h q_words q_content_words'.split():
            feature_dir = get_dir(os.path.join(features_dir, feature), True)
            feature_filename = os.path.join(feature_dir, filename)
            with open(feature_filename, 'w') as feature_file:
                feature_value = '%.8f' % extract_features(klass_articles[article], feature)
                feature_file.write(feature_value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=('desc'))
    parser.add_argument("-td", "--train_dir", dest="train_dir", default="data/train/", help="train dir")
    parser.add_argument("-dd", "--dev_dir", dest="dev_dir", default="data/dev/", help="dev dir")
    parser.add_argument("-r", "--real_dir", dest="real_dir", default="real/", help="real dir")
    parser.add_argument("-f", "--fake_dir", dest="fake_dir", default="fake/", help="fake dir")
    parser.add_argument("-fd", "--features_dir", dest="features_dir", default="run/FEATURES/", help="directory where to put the features")
    args = parser.parse_args()

    if not args.train_dir.endswith("/"): args.train_dir += "/"
    if not args.dev_dir.endswith("/"): args.dev_dir += "/"
    if not args.real_dir.endswith("/"): args.real_dir += "/"
    if not args.fake_dir.endswith("/"): args.fake_dir += "/"

    #threshold = get_optimal_threshold_from_train(args)
    #test_threshold_on_dev(threshold, args)

    generate_features_for_all(args)
