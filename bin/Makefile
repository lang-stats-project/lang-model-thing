all: liblinear libsvm python evallm

liblinear: check
	test -e ../src/liblinear-1.96 || (wget -O liblinear.tar.gz http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/liblinear.cgi?+http://www.csie.ntu.edu.tw/~cjlin/liblinear+tar.gz; 	tar xvf liblinear.tar.gz -C ../src)
	cd ../src/liblinear-1.96 ; make
	rm -f liblinear.tar.gz
	ln -s ../src/liblinear-1.96/train .
	ln -s ../src/liblinear-1.96/predict .

libsvm: check
	test -e ../src/libsvm-3.20 || (wget -O libsvm.tar.gz http://www.csie.ntu.edu.tw/~cjlin/cgi-bin/libsvm.cgi?+http://www.csie.ntu.edu.tw/~cjlin/libsvm+tar.gz; tar xvf libsvm.tar.gz -C ../src)
	cd ../src/libsvm-3.20 ; make
	rm -f libsvm.tar.gz
	ln -s ../src/libsvm-3.20/svm-train .
	ln -s ../src/libsvm-3.20/svm-predict .

python: check
	ls *.py | xargs -I '{}' unlink '{}'
	ln -s ../src/scripts/*.py .
	chmod +x *.py

evallm: check
	cd ../src/CMU-Cam_Toolkit_v2/src; make
	mv ../src/CMU-Cam_Toolkit_v2/src/evallm .
	cd ../src/CMU-Cam_Toolkit_v2/src; ls -l | grep '^\S*x\S*' | grep -v "drwxr" | awk '{print $NF}' | xargs -I '{}' rm -f '{}' ; make clean

check:
	true

clean:
	rm -rf *.py *train *predict ../src/liblinear-1.96 evallm
