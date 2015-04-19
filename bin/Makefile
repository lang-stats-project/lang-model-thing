all: liblinear python

liblinear: check
	test -e ../src/liblinear-1.96 || (wget -O liblinear.tar.gz http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/liblinear.cgi?+http://www.csie.ntu.edu.tw/~cjlin/liblinear+tar.gz; 	tar xvf liblinear.tar.gz -C ../src)
	cd ../src/liblinear-1.96 ; make
	rm liblinear.tar.gz
	ln -s ../src/liblinear-1.96/train .
	ln -s ../src/liblinear-1.96/predict .

python: check
	test -e `ls *.py` || ls *.py | xargs -I '{}' unlink '{}'
	ln -s ../src/scripts/*.py .
check:
	true

clean:
	rm -rf *.py train predict ../src/liblinear-1.96
