'''
	Donald Disha, RCS ID: dishad
	Andrew Aquino, RCS ID: dawneraq
	Parker Slote, RCS ID: slotep
	12/12/2016
	Operating Systems
'''

import sys
import os.path

# initializes memory for page references
def initMemory(mem, pos, f):
	for i in range(0, f):
		mem.append('.')
		pos.append(0)

# returns minimum of 2 values
def minimum_val(x, y):
	if x < y:
		return x
	else:
		return y

# looks forward for OPT algorithm
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
	
# finds if any two page references are equal in distance, compares max value
def getEqualMax(li, equal_idx):
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

# finds if any two page references are equal in distance, compares min value
def getEqualMin(li, equal_idx):
	count = 0
	minm = getMin(li)
	equal_idx.append(minm)
	for x in range(0, len(li)):
		if x == minm:
			continue
		else:
			if li[x] == li[minm]:
				equal_idx.append(x)
				count = 1
	
	return count
	
# returns the index of the minimum element in a list
def getMin(li):
	minm = li[0]  
	
	for i in range(1, len(li)):
		if li[i] < minm:
			minm = li[i]
	
	return li.index(minm)

# returns the index of the maximum element in a list
def getMax(li):
	maxm = li[0]  
	
	for i in range(1, len(li)):
		if li[i] > maxm:
			maxm = li[i]
	
	return li.index(maxm)

# OPT Algorithm
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
				
				if getEqualMax(mem_pos, equal_idx) == 1:
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
				equal_idx = []
				print ("referencing page " + references[x] + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (victim page ' + victim + ')')
			num_faults +=1
	
	print ('End of OPT simulation (' + str(num_faults) + ' page faults)')

# LRU Algorithm
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

# LFU Algorithm
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
				if getEqualMin(mem_pos, equal_idx) == 1:
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
				equal_idx = []
				print ("referencing page " + references[x] + ' [mem: ' + ' '.join([i for i in mem]) + '] PAGE FAULT (victim page ' + victim + ')')
			num_faults +=1
		else:
			idx = mem.index(references[x])
			mem_pos[idx] += 1
	
	print ('End of LFU simulation (' + str(num_faults) + ' page faults)')

# Runs OPT, LRU, and LFU Algorithms
def runAlgorithms(f, references):
	optAlg(f, references)
	print 
	lruAlg(f, references)
	print 
	lfuAlg(f, references)

