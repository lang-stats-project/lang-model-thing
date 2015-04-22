#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, time, argparse, operator
from stop_words import *
from collections import Counter
from numpy import arange
from random import *

def get_dir(dir_name, create_if_missing=False):
    if not os.path.exists(dir_name):
        if create_if_missing:
            os.makedirs(dir_name)
        else:
            print("unexisting dir '{}'".format(dir_name))
            exit()
    return dir_name

# corpus is train/dev; sub_dir is real/fake
def count_dir(corpus_dir, sub_dir_name):
    full_dir = os.path.join(corpus_dir, sub_dir_name)
    articles_counts = {}
    for article in os.listdir(full_dir):
        article_filename = os.path.join(full_dir, article)
        if os.path.isdir(article_filename): continue
        article_id = article.split('.')[0]
        article_counts = Counter()
        with open(article_filename, 'r') as article_file:
            for line in article_file:
                for word in line.split():
                    word = word.lower()
                    if not is_stop(word):
                        article_counts[word] += 1
        articles_counts[article_id] = article_counts
        # if len(articles_counts) > 20: break
    return articles_counts

def extract_feature(article_counts, debug):
    art_size = sum(article_counts.values())
    art_most_freq = article_counts.most_common(1)[0][1]
    ratio = art_most_freq / float(art_size)
    if debug and random() > 0.9:
        print "size: %d, most freq: %d, ratio: %f" % (art_size, art_most_freq, ratio)
        print article_counts
    return ratio

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=('desc'))
    parser.add_argument("-td", "--train_dir", dest="train_dir", default="data/train/", help="train dir")
    parser.add_argument("-dd", "--dev_dir", dest="dev_dir", default="data/dev/", help="dev dir")
    parser.add_argument("-r", "--real_dir", dest="real_dir", default="real/", help="real dir")
    parser.add_argument("-f", "--fake_dir", dest="fake_dir", default="fake/", help="fake dir")
    args = parser.parse_args()

    if not args.train_dir.endswith("/"): args.train_dir += "/"
    if not args.dev_dir.endswith("/"): args.dev_dir += "/"
    if not args.real_dir.endswith("/"): args.real_dir += "/"
    if not args.fake_dir.endswith("/"): args.fake_dir += "/"

    threshold = get_optimal_threshold_from_train(args)

    test_threshold_on_dev(threshold, args)
