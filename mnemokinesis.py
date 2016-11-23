"""
mnemokinesis.py

CSCI-4210 Operating Systems F16

Python simulation of a variety of memory management systems, including
contiguous, non-contiguous, and virtual memory.
"""

import sys
import textwrap

class Mnemokinesis(object):
	frames_total = 256
	frames_per_line = 32 # output tuning
	t_memmove = 1 # ms taken to move one frame of memory

	def __init__(self, input_file):
		self.reset(input_file)

	def reset(self, input_file):
		self.memory = '.' * Mnemokinesis.frames_total

	def __repr__(self):
		border = '=' * Mnemokinesis.frames_per_line
		memory_wrapped = textwrap.fill(self.memory, Mnemokinesis.frames_per_line)
		return  border + '\n' + memory_wrapped + '\n' + border

	def read_input(self, input_file):
		with open(input_file, 'r') as input_data:
			print 'TODO'

def main():
	# Check command line arguments.
	if len(sys.argv) != 2:
		print 'ERROR Invalid arguments'
		print 'USAGE: python mnemokinesis.py <input-file>'
		sys.exit(2)

	input_file = sys.argv[1]

	#TODO Contiguous Memory Management
		#TODO Next-Fit
		#TODO Best-Fit
		#TODO Worst-Fit
	#TODO Non-Contiguous Memory Management
	#TODO Virtual Memory Management
		#TODO OPT
		#TODO LRU
		#TODO LFU


if __name__ == '__main__':
	main()