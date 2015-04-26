#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re, argparse

file_id_re = r"\s*to the text [./\w]*?(\d+)\.txt"
perp_re = r"Perplexity = (\d+\.\d+), Entropy = \d+\.\d+ bits"
hit_4gram_re = r"Number of 4-grams hit = \d+  \((\d+\.\d+)%\)"
hit_3gram_re = r"Number of 3-grams hit = \d+  \((\d+\.\d+)%\)"
hit_2gram_re = r"Number of 2-grams hit = \d+  \((\d+\.\d+)%\)"
hit_1gram_re = r"Number of 1-grams hit = \d+  \((\d+\.\d+)%\)"
end_re = r"\d+ OOVs \((\d+\.\d+)%\)"


def create_all_features(corpus, sub_corpus, features_dir):
    results_filename = '{0}_{1}_result.txt'.format(corpus, sub_corpus)
    saved_files = 0
    with open(results_filename, 'r') as article_results:
        for line in article_results:
            art_id_match = re.match(file_id_re, line)
            if art_id_match:
                article_id = art_id_match.groups()[0]

            perp_match = re.match(perp_re, line)
            if perp_match:
                perplexity = perp_match.groups()[0]

            gram4_match = re.match(hit_4gram_re, line)
            if gram4_match:
                gram4 = gram4_match.groups()[0]

            gram3_match = re.match(hit_3gram_re, line)
            if gram3_match:
                gram3 = gram3_match.groups()[0]

            gram2_match = re.match(hit_2gram_re, line)
            if gram2_match:
                gram2 = gram2_match.groups()[0]

            gram1_match = re.match(hit_1gram_re, line)
            if gram1_match:
                gram1 = gram1_match.groups()[0]

            end_match = re.search(end_re, line)
            if end_match:
                oov = end_match.groups()[0]
                #print article_id, perplexity, gram4, gram3, gram2, gram1, oov
                feature_file_name = os.path.join(
                    features_dir,
                    '%s.%s.%s.f' % (corpus, sub_corpus, article_id)
                )
                with open(feature_file_name, 'w') as feature_file:
                    values = (perplexity, gram4, gram3, gram2, gram1, oov)
                    feature_file.write('\t'.join(values))
                saved_files += 1
    print "created %s feature files" % saved_files



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=('desc'))
    parser.add_argument("-c", "--corpus", dest="corpus", required=True)
    parser.add_argument("-sc", "--sub_corpus", dest="sub_corpus", required=True)
    parser.add_argument("-fd", "--features_dir", dest="features_dir", required=True)
    args = parser.parse_args()

    create_all_features(args.corpus, args.sub_corpus, args.features_dir)

#create_all_features('train', 'real')
#create_all_features('train', 'fake')
#create_all_features('dev', 'real')
#create_all_features('dev', 'fake')



# grep Perplexity train_real_eval_result.txt > train_real_eval_result_perp.txt
# grep Perplexity train_fake_eval_result.txt > train_fake_eval_result_perp.txt
# grep Perplexity dev_real_eval_result.txt > dev_real_eval_result_perp.txt
# grep Perplexity dev_fake_eval_result.txt > dev_fake_eval_result_perp.txt