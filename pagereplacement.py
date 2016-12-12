'''
<<<<<<< HEAD:pagereference.py
	Donald Disha, RCS ID:
	Andrew Aquino, RCS ID:
	Parker Slote RCS ID: slotep
=======
	Donald Disha, RCS ID: dishad
	Andrew Aquino, RCS ID: dawneraq
>>>>>>> 201e93c6a76bfbcf023e9cd4d1ac5f63880840f4:pagereplacement.py
	12/12/2016
	Operating Systems
'''

import sys
import os.path

def initMemory(mem, pos, f):
	for i in range(0, f):
		mem.append('.')
		pos.append(0)

def minimum_val(x, y):
	if x < y:
		return x
	else:
		return y

def seeFuture(page, references, counter):
	lengthRemaining = len(references) - counter
	remainingPages = counter - 1
	for i in range(1, lengthRemaining+1):
		idx = i + remainingPages
		current_page = references[idx]

		if page == current_page:
			return i

		if i == lengthRemaining:
			return i
	
def getEqual(li, equal_idx):
	count = 0
	maxm = getMax(li)
	equal_idx.append(maxm)
	for x in range(0, len(li)):
		if x == maxm:
			continue
		else:
			if li[x] == li[maxm]:
				equal_idx.append(x)
				count = 1
	
	return count
	
def getMin(li):
	minm = li[0]  
	
	for i in range(1, len(li)):
		if li[i] < minm:
			minm = li[i]
	
	return li.index(minm)

def getMax(li):
	maxm = li[0]  
	
	for i in range(1, len(li)):
		if li[i] > maxm:
			maxm = li[i]
	
	return li.index(maxm)

def optAlg(f, references):
	num_faults = 0
	idx = 0
	point_pos = 0
	mem = []
	mem_pos = []
	equal_idx = []

	initMemory(mem, mem_pos, f)
		
	print ('Simulating OPT with fixed frame size of ' + str(f))
	for x in range(0, len(references)):
		if references[x] not in mem:
			if mem.count('.') > 0:
				point_pos = mem.index('.')
				mem[point_pos] = references[x]
				idx = mem.index(references[x])
				mem_pos[idx] = x
				print ("referencing page " + references[x] + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (no victim page)')
			else:
				for i in range(0, f):
					mem_pos[i] = seeFuture(mem[i], references, x)
				
				if getEqual(mem_pos, equal_idx) == 1:
					min_idx = mem.index(min(mem))
					if min_idx in equal_idx:
						opt_idx = min_idx
					else:
						cur_min = minimum_val(mem[equal_idx[0]],mem[equal_idx[1]])
						opt_idx = mem.index(cur_min)
				else:
					opt_idx = getMax(mem_pos)
				victim = mem[opt_idx]
				mem[opt_idx] = references[x]
				equal_mem = []
				equal_idx = []
				print ("referencing page " + references[x] + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (victim page ' + victim + ')')
			num_faults +=1
	
	print ('End of OPT simulation (' + str(num_faults) + ' page faults)')

def lruAlg(f, references):	
	num_faults = 0
	idx = 0
	point_pos = 0
	lru_idx = 0
	mem = []
	mem_pos = []

	initMemory(mem, mem_pos, f)

	print ('Simulating LRU with fixed frame size of ' + str(f))
	for x in range(0, len(references)):
		if references[x] not in mem:
			if mem.count('.') > 0:
				point_pos = mem.index('.')
				mem[point_pos] = references[x]
				idx = mem.index(references[x])
				mem_pos[idx] = x
				print ("referencing page " + references[x] + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (no victim page)')
			else:
				lru_idx = getMin(mem_pos)
				victim = mem[lru_idx]
				mem[lru_idx] = references[x]
				mem_pos[lru_idx] = x
				print ("referencing page " + references[x] + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (victim page ' + victim + ')')
			num_faults +=1
		else:
			idx = mem.index(references[x])
			mem_pos[idx] = x

	print ('End of LRU simulation (' + str(num_faults) + ' page faults)')

def lfuAlg(f, references):
	num_faults = 0
	idx = 0
	point_pos = 0
	mem = []
	mem_pos = []
	equal_idx = []

	initMemory(mem, mem_pos, f)
	
	print ('Simulating LFU with fixed frame size of ' + str(f))
	for x in range(0, len(references)):
		if references[x] not in mem:
			if mem.count('.') > 0:
				point_pos = mem.index('.')
				mem[point_pos] = references[x]
				idx = mem.index(references[x])
				mem_pos[idx] = 1
				print ("referencing page " + references[x] + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (no victim page)')
			else:
				if getEqual(mem_pos, equal_idx) == 1:
					min_idx = mem.index(min(mem))
					if min_idx in equal_idx:
						lfu_idx = min_idx
					else:
						cur_min = minimum_val(mem[equal_idx[0]],mem[equal_idx[1]])
						lfu_idx = mem.index(cur_min)
				else:
					lfu_idx = getMin(mem_pos)
				victim = mem[lfu_idx]
				mem[lfu_idx] = references[x]
				mem_pos[lfu_idx] = 1
				print ("referencing page " + references[x] + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (victim page ' + victim + ')')
			num_faults +=1
		else:
			idx = mem.index(references[x])
			mem_pos[idx] += 1
	
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
