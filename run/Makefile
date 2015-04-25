export PATH:=../bin:${PATH} # Binaries in the bin directory
export SHELL := /bin/bash
.PRECIOUS: gridsearch.% merged.train.% merged.dev.%

CLASSIFIER=svm-

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
	find ../data/train/fake -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB $* 'FEATURES/unigram/train.fake.'
	find ../data/train/real -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB $* 'FEATURES/unigram/train.real.'
	find ../data/dev/fake -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB $* 'FEATURES/unigram/dev.fake.'
	find ../data/dev/real -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB $* 'FEATURES/unigram/dev.real.'
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

merged.dev.%: run.%
	merge-features.py $< $* dev
merged.train.%: run.%
	merge-features.py $< $* train

SVM_PARAMS=-s 0 -t 2
gridsearch.%: merged.train.%
	grid.py ${SVM_PARAMS} -log2c -11,11,2 -log2g -11,11,2 -v 4 -gnuplot null -svmtrain ../bin/svm-train $< > $@

eval.%: gridsearch.% merged.train.% merged.dev.%
	svm-train ${SVM_PARAMS} -g `tail -1 $< | awk '{print $$2}'` -c `tail -1 $< | awk '{print $$1}'` -m 10000 merged.train.$* model.$*
	svm-predict merged.dev.$* model.$* merged.dev.$*.output > $@
	test -e RUN$* || mkdir RUN$*
	mv merged.*.$* merged.*.$*.* model.$* gridsearch.$* RUN$*
