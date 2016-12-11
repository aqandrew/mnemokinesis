'''
	Donald Disha, RCS ID:
	Andrew Aquino, RCS ID:
	12/12/2016
	Operating Systems
'''

import sys

def optAlg(f):
	num_faults = 0
	print ('Simulating OPT with fixed frame size of ' + str(f))
	print ('End of OPT simulation (' + str(num_faults) + ' page faults)')

def lruAlg(f):	
	num_faults = 0
	print ('Simulating LRU with fixed frame size of ' + str(f))
	print ('End of LRU simulation (' + str(num_faults) + ' page faults)')

def lfuAlg(f):
	num_faults = 0
	print ('Simulating LFU with fixed frame size of ' + str(f))
	print ('End of LFU simulation (' + str(num_faults) + ' page faults)')

def runAlgorithms(f):
	print ("Beginning Virtual Memory Algorithms\n")
	optAlg(f)
	print ()
	lruAlg(f)
	print ()
	lfuAlg(f)

def main():
	runAlgorithms(3)

if __name__ == '__main__':
	main()
