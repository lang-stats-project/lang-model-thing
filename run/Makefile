export PATH:=../bin:${PATH} # Binaries in the bin directory
export SHELL := /bin/bash
.PRECIOUS: gridsearch.% merged.train.% merged.dev.%

CLASSIFIER=svm-

prepare:
	cd ../bin ; make libsvm python #downloads

target.random-features.%:
	cd ../bin ; make python
	test -e FEATURES || mkdir FEATURES
	test -e FEATURES/random$* || mkdir FEATURES/random$*
	find ../data/train/fake -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/train.fake.'
	find ../data/train/real -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/train.real.'
	find ../data/dev/fake -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/dev.fake.'
	find ../data/dev/real -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/dev.real.'
	touch $@

target.unigram-features:
	cd ../bin ; make python
	test -e FEATURES || mkdir FEATURES
	find ../data/train -name \*.txt | xargs -I '{}' cat '{}' | awk '{for(i=1;i<=NF;i++)print $$i}' | sort | uniq -c | awk '{print $$2}' > VOCAB
	test -e FEATURES/unigram || mkdir FEATURES/unigram
	find ../data/train/fake -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB 'FEATURES/unigram/train.fake.'
	find ../data/train/real -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB 'FEATURES/unigram/train.real.'
	find ../data/dev/fake -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB 'FEATURES/unigram/dev.fake.'
	find ../data/dev/real -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB 'FEATURES/unigram/dev.real.'
	rm VOCAB
	touch $@

target.3gram-lm-features:
	cd ../bin ; make evallm python
	tar xvfz ../data/projectLM.binlm.tar.gz -C .
	test -e FEATURES || mkdir FEATURES
	test -e FEATURES/3gram-lm || mkdir FEATURES/3gram-lm
	find ../data/train/fake -name \*.txt | xargs -I '{}' run-lm.py '{}' projectLM.binlm 'FEATURES/3gram-lm/train.fake.'
	find ../data/train/real -name \*.txt | xargs -I '{}' run-lm.py '{}' projectLM.binlm 'FEATURES/3gram-lm/train.real.'
	find ../data/dev/fake -name \*.txt | xargs -I '{}' run-lm.py '{}' projectLM.binlm 'FEATURES/3gram-lm/dev.fake.'
	find ../data/dev/real -name \*.txt | xargs -I '{}' run-lm.py '{}' projectLM.binlm 'FEATURES/3gram-lm/dev.real.'
	rm projectLM.binlm
	touch $@

target.word-frequencies:
	cd ../bin; make python
	test -e FEATURES || mkdir FEATURES
	word_frequencies.py -td ../data/train/ -dd ../data/dev/ -fd FEATURES


target.3gram-nico:
	cd ../bin; make python
	test -e FEATURES || mkdir FEATURES
	test -e FEATURES/3gram-nico || mkdir FEATURES/3gram-nico

	for file in `ls -d ../data/dev/fake/[0-9]*.txt`; do echo perplexity -text $$file; done > eval_dev_fake.txt
	cat eval_dev_fake.txt | evallm -binary ../bin/projectLM.binlm > dev_fake_result.txt
	create_features_4gram.py -c dev -sc fake -fd FEATURES/3gram-nico

	for file in `ls -d ../data/dev/real/[0-9]*.txt`; do echo perplexity -text $$file; done > eval_dev_real.txt
	cat eval_dev_real.txt | evallm -binary ../bin/projectLM.binlm > dev_real_result.txt
	create_features_4gram.py -c dev -sc real -fd FEATURES/3gram-nico

	for file in `ls -d ../data/train/fake/[0-9]*.txt`; do echo perplexity -text $$file; done > eval_train_fake.txt
	cat eval_train_fake.txt | evallm -binary ../bin/projectLM.binlm > train_fake_result.txt
	create_features_4gram.py -c train -sc fake -fd FEATURES/3gram-nico

	for file in `ls -d ../data/train/real/[0-9]*.txt`; do echo perplexity -text $$file; done > eval_train_real.txt
	cat eval_train_real.txt | evallm -binary ../bin/projectLM.binlm > train_real_result.txt
	create_features_4gram.py -c train -sc real -fd FEATURES/3gram-nico


target.4gram-nico:
	cd ../bin; make python
	test -e FEATURES || mkdir FEATURES
	test -e FEATURES/4gram-nico || mkdir FEATURES/4gram-nico

	for file in `ls -d ../data/dev/fake/[0-9]*.txt`; do echo perplexity -text $$file; done > eval_dev_fake.txt
	cat eval_dev_fake.txt | evallm -binary ../bin/LM-train-100MW_4g_vocab_10K.bin > dev_fake_result.txt
	create_features_4gram.py -c dev -sc fake -fd FEATURES/4gram-nico

	for file in `ls -d ../data/dev/real/[0-9]*.txt`; do echo perplexity -text $$file; done > eval_dev_real.txt
	cat eval_dev_real.txt | evallm -binary ../bin/LM-train-100MW_4g_vocab_10K.bin > dev_real_result.txt
	create_features_4gram.py -c dev -sc real -fd FEATURES/4gram-nico

	for file in `ls -d ../data/train/fake/[0-9]*.txt`; do echo perplexity -text $$file; done > eval_train_fake.txt
	cat eval_train_fake.txt | evallm -binary ../bin/LM-train-100MW_4g_vocab_10K.bin > train_fake_result.txt
	create_features_4gram.py -c train -sc fake -fd FEATURES/4gram-nico

	for file in `ls -d ../data/train/real/[0-9]*.txt`; do echo perplexity -text $$file; done > eval_train_real.txt
	cat eval_train_real.txt | evallm -binary ../bin/LM-train-100MW_4g_vocab_10K.bin > train_real_result.txt
	create_features_4gram.py -c train -sc real -fd FEATURES/4gram-nico



target.wvec-%: ../data/word_vectors/%.txt.gz
	cd ../bin ; make python
	test -e FEATURES || mkdir FEATURES
	test -e FEATURES/wvec-$* || mkdir FEATURES/wvec-$*
	find ../data/train/fake -name \*.txt  > train.fake.wvec-$*
	find ../data/train/real -name \*.txt  > train.real.wvec-$*
	find ../data/dev/fake -name \*.txt > dev.fake.wvec-$*
	find ../data/dev/real -name \*.txt  > dev.real.wvec-$*

	wvec-feature.py train.fake.wvec-$* $< FEATURES/wvec-$*/train.fake.
	wvec-feature.py train.real.wvec-$* $< FEATURES/wvec-$*/train.real.
	wvec-feature.py dev.fake.wvec-$* $< FEATURES/wvec-$*/dev.fake.
	wvec-feature.py dev.real.wvec-$* $< FEATURES/wvec-$*/dev.real.

	rm -rf train.*.wvec-$* dev.*.wvec-$*
	touch $@

merged.dev.%: run.%
	merge-features.py $< $* dev
merged.train.%: run.%
	merge-features.py $< $* train

SVM_PARAMS=-s 0 -t 2
GRID_INTERVALS=-11,11,0.5
gridsearch.%: merged.train.%
	grid.py ${SVM_PARAMS} -log2c ${GRID_INTERVALS} -log2g ${GRID_INTERVALS} -v 4 -gnuplot null -svmtrain ../bin/svm-train $< > $@

eval.%: gridsearch.% merged.train.% merged.dev.%
	svm-train -b 1 ${SVM_PARAMS} -g `tail -1 $< | awk '{print $$2}'` -c `tail -1 $< | awk '{print $$1}'` -m 10000 merged.train.$* model.$*
	svm-predict -b 1 merged.dev.$* model.$* merged.dev.$*.output > $@
	test -e RUN$* || mkdir RUN$*
	mv merged.*.$* merged.*.$*.* model.$* model.$* gridsearch.$* RUN$*
