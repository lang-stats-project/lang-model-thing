#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, time, argparse, operator
from stop_words import *
from collections import Counter
from numpy import arange

def count_dir(dir_name):
    articles_counts = {}
    for article in os.listdir(dir_name):
        article_filename = os.path.join(dir_name, article)
        if os.path.isdir(article_filename):
            continue
        article_id = article.split('.')[0]
        article_counts = Counter()
        with open(article_filename, 'r') as article_file:
            for line in article_file:
                for word in line.split():
                    if not is_stop(word):
                        article_counts[word] += 1
        articles_counts[article_id] = article_counts
        # if len(articles_counts) > 20: break
    return articles_counts

def extract_feature(article_counts, debug):
    art_size = sum(article_counts.values())
    art_most_freq = article_counts.most_common(1)[0][1]
    ratio = art_most_freq / float(art_size)
    if debug:
        print "size: %d, most freq: %d, ratio: %f" % (art_size, art_most_freq, ratio)
    return ratio


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=('desc'))
    parser.add_argument("-r", "--real_dir", dest="real_dir", default="data/train/real/", help="real dir")
    parser.add_argument("-f", "--fake_dir", dest="fake_dir", default="data/train/fake/", help="fake dir")
    args = parser.parse_args()

    if not args.real_dir.endswith("/"): args.real_dir += "/"
    if not args.fake_dir.endswith("/"): args.fake_dir += "/"

    real = count_dir(args.real_dir)
    fake = count_dir(args.fake_dir)

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

    # TODO: test this on dev set
