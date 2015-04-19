import os
import sys

data = [l.strip() for l in open(sys.argv[1]).readlines()]
truth = [l.strip() for l in open(sys.argv[1].replace('.dat','Labels.dat')).readlines()]

bigsent = ''
for l in data:
	bigsent += (l + '\n')

articles = bigsent.split('~~~~~\n')[1:]

for i in range(len(truth)):
	val = truth[i]
	if val == '0':
		open('fake/' + str(i) + '.txt', 'w').write(articles[i])
	if val == '1':	
		open('real/' + str(i) + '.txt', 'w').write(articles[i])



