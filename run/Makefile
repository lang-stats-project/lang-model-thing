BIN=../bin
export PATH:=../bin:.:${PATH} # Binaries in the bin directory
.PRECIOUS:

random-features.%:
	test -e FEATURES/random$* || mkdir FEATURES/random$*
	find ../data/train/fake -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/train.fake.'
	find ../data/train/real -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/train.real.'
	find ../data/dev/fake -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/dev.fake.'
	find ../data/dev/real -name \*.txt | xargs -I '{}' random-feature.py '{}' $* 'FEATURES/random$*/dev.fake.'
	touch $@

eval.%: run.%
	merge-features.py $< $< train
	merge-features.py $< $< dev
	train merged.train.$<
	predict merged.dev.$< merged.train.$<.model merged.dev.$<.output > $@
	test -e RUN$* || mkdir RUN$*
	mv merged.*.$<* RUN$*
