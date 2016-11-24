"""
mnemokinesis.py

CSCI-4210 Operating Systems F16

Python simulation of a variety of memory management systems, including
contiguous, non-contiguous, and virtual memory.
"""

import sys
import textwrap

class Mnemokinesis(object):
	"""
	Memory is represented here as a string, to simplify worst- and best-fit algorithms.
	"""
	frames_total = 256 # total number of memory frames to simulate
	frames_per_line = 32 # output tuning
	t_memmove = 1 # ms taken to move one frame of memory
	frames_virtual = 3 # number of frames in fixed memory allocation scheme for some process

	def __init__(self, input_file):
		self.reset(input_file)

	def reset(self, input_file):
		self.t = 0 # Time elapsed
		self.memory = '.' * Mnemokinesis.frames_total # Periods represent free memory frames.

	def __repr__(self):
		border = '=' * Mnemokinesis.frames_per_line
		memory_wrapped = textwrap.fill(self.memory, Mnemokinesis.frames_per_line)
		return  border + '\n' + memory_wrapped + '\n' + border

	def valid_line(self, line):
		"""
		Any line beginning with a # character is ignored (these lines are comments).
		Further, all blank lines are also ignored, including lines containing only
		whitespace characters.
		"""
		return (not line.isspace()) and line[0] != '#'

	def read_input(self, input_file):
		"""
		The maximum number of processes in the simulation will be 26.
		Processes are not guaranteed to be given in alphabetical order.
		"""
		with open(input_file, 'r') as input_data:
			process_strings = [line.strip() for line in input_data if self.valid_line(line)]
			self.process_list = []

			try:
				for process_string in process_strings:
					# The overall number of processes to simulate is specified first
					#  on a line by itself.
					# This allows for dynamic memory allocation to occur.
					if process_string == process_strings[0]:
						self.num_processes = int(process_string)

					# Split on <= 1 space or tab characters.
					process_params = process_string.split()
					pid = process_params[0]
					arrival_run_times = process_params[1:]
					self.process_list.append(Process(pid, arrival_run_times))

			except TypeError as err:
				print 'TODO handle TypeErrors'

			#TODO maintain a list containing
				#where each process is allocated
				#how much contiguous memory each process uses
				#where and how much free memory is available
					#i.e. where each free partition is

			print 'TODO read_input'

	def simulate(self, algorithm):
		algo_names = {
			'NF': 'Contiguous -- Next-Fit',
			'BF': 'Contiguous -- Best-Fit',
			'WF': 'Contiguous -- Worst-Fit',
			'NC': 'Non-contiguous'
		}

		print 'time {}ms: Simulator started ({})'.format(self.t, algo_names[algorithm])

		#TODO When defragmentation occurs, all process' pending arrival times must
		# increase according to defragmentation time.

		#TODO Next-Fit

		#TODO Best-Fit

		#TODO Worst-Fit

		#TODO Non-Contiguous Memory Management

		print 'TODO simulate ' + algorithm

	def simulate_virtual(self, algorithm):
		print 'Simulating {} with fixed frame size of {}'.format(algorithm, Mnemokinesis.frames_virtual)

		#TODO OPT

		#TODO LRU

		#TODO LFU

		print 'TODO simulate ' + algorithm


def main():
	# Check command line arguments.
	if len(sys.argv) != 3:
		print 'ERROR Invalid arguments'
		print 'USAGE: python mnemokinesis.py <input_file> <page_reference_file>'
		sys.exit(2)

	input_file = sys.argv[1]
	page_reference_file = sys.argv[2]

	mk = Mnemokinesis(input_file)
	algorithms = ['NF', 'BF', 'WF', 'NC']
	algorithms_virtual = ['OPT', 'LRU', 'LFU']

	for algorithm in algorithms:
		mk.simulate(algorithm)
		mk.reset(input_file)

	for algorithm in algorithms_virtual:
		# TODO Should a separate mk class be specified for virtual memory?
		mk.simulate_virtual(algorithm)
		mk.reset(input_file)


if __name__ == '__main__':
	main()