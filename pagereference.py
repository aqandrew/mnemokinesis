'''
	Donald Disha, RCS ID:
	Andrew Aquino, RCS ID:
	12/12/2016
	Operating Systems
'''

import sys
import os.path

def countNum(memory):
	num_counter = 0
	for x in memory:
		if x > 0:
			num_counter += 1
	return num_counter

def optAlg(f, references):
	num_faults = 0
	
	mem = []
	idx = 0
	
	for i in range(0, f):
		mem.append('.')
	
	print ('Simulating OPT with fixed frame size of ' + str(f))
	for x in references:
		if x not in mem:
			if mem.count('.') > 0:
				idx = mem.index('.')
				mem[idx] = x
				print ("referencing page " + x + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (no victim page)')
			else:
				victim = mem[2]
				mem[2] = x
				print ("referencing page " + x + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (victim page ' + victim + ')')
			num_faults +=1
		'''
		else:
			if countNum(mem) == 3:
				mem[2] = x
			else if countNum(mem) == 2:
				mem[1] = 
			else if countNum(mem) == 1:
				mem[0] = '.'
		'''
		
		

	print ('End of OPT simulation (' + str(num_faults) + ' page faults)')

def lruAlg(f, references):	
	num_faults = 0
	mem = ['.', '.', '.']
	print ('Simulating LRU with fixed frame size of ' + str(f))
	for x in references:
		if x not in mem and mem.count('.') > 0:
			idx = mem.index('.')
			mem[idx] = x
			print ("referencing page " + x + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (no victim page)')
			num_faults += 1
	
	print ('End of LRU simulation (' + str(num_faults) + ' page faults)')

def lfuAlg(f, references):
	num_faults = 0
	mem = ['.', '.', '.']
	print ('Simulating LFU with fixed frame size of ' + str(f))
	for x in references:
		if x not in mem and mem.count('.') > 0:
			idx = mem.index('.')
			mem[idx] = x
			print ("referencing page " + x + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (no victim page)')
			num_faults += 1
	
	print ('End of LFU simulation (' + str(num_faults) + ' page faults)')

def runAlgorithms(f, references):
	print ("Beginning Virtual Memory Algorithms\n")
	optAlg(f, references)
	print ()
	lruAlg(f, references)
	print ()
	lfuAlg(f, references)

def main():
	if not os.path.isfile(sys.argv[1]):
		print ("page reference input file doesnt exist")
		sys.exit()
	
	ref_file = open(sys.argv[1], 'r')
	file_string = ref_file.read()
	reference_list = file_string.split()
	runAlgorithms(3, reference_list)
	ref_file.close()

if __name__ == '__main__':
	main()
