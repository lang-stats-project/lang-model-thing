export PATH:=${PATH}:../bin:. # Binaries in the bin directory
export SHELL := /bin/bash
.PRECIOUS:

CLASSIFIER=svm-

target.random-features.%:
	test -e FEATURES/random$* || mkdir FEATURES/random$*
	find ../data/train/fake -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/train.fake.'
	find ../data/train/real -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/train.real.'
	find ../data/dev/fake -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/dev.fake.'
	find ../data/dev/real -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/dev.real.'
	touch $@

target.unigram-features:
	find ../data/train -name \*.txt | xargs -I '{}' cat '{}' | awk '{for(i=1;i<=NF;i++)print $$i}' | sort | uniq -c | awk '{print $$2}' > VOCAB
	test -e FEATURES/unigram || mkdir FEATURES/unigram
	find ../data/train/fake -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB $* 'FEATURES/unigram/train.fake.'
	find ../data/train/real -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB $* 'FEATURES/unigram/train.real.'
	find ../data/dev/fake -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB $* 'FEATURES/unigram/dev.fake.'
	find ../data/dev/real -name \*.txt | xargs -I '{}' unigram-feature.py '{}' VOCAB $* 'FEATURES/unigram/dev.real.'
	rm VOCAB
	touch $@

eval.%: run.%
	merge-features.py $< $< train
	merge-features.py $< $< dev
	${CLASSIFIER}train merged.train.$<
	${CLASSIFIER}predict merged.dev.$< merged.train.$<.model merged.dev.$<.output > $@
	test -e RUN$* || mkdir RUN$*
	mv merged.*.$<* RUN$*
