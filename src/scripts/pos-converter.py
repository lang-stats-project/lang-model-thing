#!/usr/bin/env python
import sys

for line in sys.stdin:
	if len(line) == 1:
		print
		continue

	right_p = line.strip().split(')')
	for tok_r in right_p:
		left_p = tok_r.split('(')
		for tok_l in left_p:
			token = tok_l.split()
			if len(token) == 2:
				print token[0]
	print

