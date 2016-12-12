"""
mnemokinesis.py

CSCI-4210 Operating Systems F16

Python simulation of a variety of memory management systems, including
contiguous, non-contiguous, and virtual memory.
"""

import sys
import textwrap
from process import Process

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
		self.read_input(input_file)
		self.allocated_processes = [] # keep track of processes in memory,
			# in the order they were placed, as tuples of (process, last placed index)

	def __repr__(self):
		border = '=' * Mnemokinesis.frames_per_line
		memory_wrapped = textwrap.fill(self.memory, Mnemokinesis.frames_per_line)
		return border + '\n' + memory_wrapped + '\n' + border
		#return border + '\n' + memory_wrapped + '\n' + border + '\n' + '\n'.join([process.pid + ' ' + repr(process.memory_frames) + '\ta: ' + repr([arrival_time for arrival_time in process.arrival_times]) + '\n\tr: ' + repr([run_time for run_time in process.run_times]) for process in self.process_list]) # TODO debug

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
					else:
						# Split on <= 1 space or tab characters.
						process_params = process_string.split()
						pid = process_params[0]
						memory_frames = process_params[1]
						arrival_run_times = process_params[2:]
						self.process_list.append(Process(pid, memory_frames, arrival_run_times))

			except TypeError as err:
				print err
				sys.exit(1)

		self.process_list.sort()

	def simulate(self, algorithm):
		algo_names = {
			'NF': 'Contiguous -- Next-Fit',
			'BF': 'Contiguous -- Best-Fit',
			'WF': 'Contiguous -- Worst-Fit',
			'NC': 'Non-contiguous'
		}

		print 'time {}ms: Simulator started ({})'.format(self.t, algo_names[algorithm])

		while True:
			for process in self.process_list:
				# Place arriving processes if not in memory already.
				if (self.t in process.arrival_times and
						self.memory.find(process.pid) == -1):
					print 'time {}ms: Process {} arrived (requires {} frames)'.format(
						self.t, process.pid, process.memory_frames)

					if self.memory.count('.') >= process.memory_frames:
						if self.must_defragment_for(process):
							print ('time {}ms: Cannot place process {}'.format(
								self.t, process.pid) +
								' -- starting defragmentation')
							self.defragment()
							print self

						if algorithm == 'NF':
							free_index = self.next_fit_index(process)
						elif algorithm == 'BF':
							free_index = self.best_fit_index(process)
						elif algorithm == 'WF':
							free_index = self.worst_fit_index(process)

						self.place_process(process, free_index)
						print 'time {}ms: Placed process {}:\n{}'.format(
							self.t, process.pid, self)
					else:
						print 'time {}ms: Cannot place process {} -- skipped!\n{}'.format(
							self.t, process.pid, self)

				# Remove processes for each finished run time.
				end_times = [process.arrival_times[run] + process.run_times[run]
					for run in range(process.times_run, process.times_to_run)]

				if self.t in end_times and self.memory.find(process.pid) != -1:
					self.remove_process(process)
					process.times_run += 1
					print 'time {}ms: Process {} removed:\n{}'.format(
						self.t, process.pid, self)

			#TODO Non-Contiguous Memory Management

			# Terminate as soon as the last process leaves memory.
			if self.has_terminated():
				break

			self.t += 1

		print 'time {}ms: Simulator ended ({})\n'.format(self.t, algo_names[algorithm])

	def has_terminated(self):
		"""Return True if the time that has elapsed in the simulation surpasses
		all 'interesting events' for each process.
		This is a method extrinsic to each process because there is no guarantee
		 that a process won't be skipped.
		"""
		return (self.memory == '.' * Mnemokinesis.frames_total and
			all([self.t >= process.arrival_times[run] + process.run_times[run]
			for process in self.process_list
			for run in range(len(process.arrival_times))]))

	def next_fit_index(self, process):
		"""Return the first index in memory of a free partition that can fit
		 the specified process for Next-Fit.
		Assume defragmentation has just occurred, if it was necessary.
		"""
		# Search from the most recently allocated partition
		#  until we find a partition that fits this process.
		if self.allocated_processes:
			process_placed_last = self.allocated_processes[-1]
			search_from_index = (process_placed_last[1] +
				process_placed_last[0].memory_frames)
		else:
			search_from_index = 0

		free_partition_bounds = self.get_free_partition(search_from_index)

		while free_partition_bounds[1] - free_partition_bounds[0] + 1 < process.memory_frames:
			free_partition_bounds = self.get_free_partition(
				free_partition_bounds[1])

		return free_partition_bounds[0]

	def get_free_partition(self, index):
		"""Return the bounds of the next free partition sought from index.
		Assume defragmentation has just occurred, if it was necessary.
		"""
		# If not seeking from the end of memory, behave as expected.
		if index < len(self.memory) - 1:
			start_free_index = self.memory.find('.', index)
		# Otherwise, seek from the 'top' of memory.
		else:
			start_free_index = self.memory.find('.')

		for index, char in enumerate(self.memory):
			if ((index > start_free_index and char != '.') or
					index == len(self.memory) - 1):
				end_free_index = index
				break

		return (start_free_index, end_free_index)

	def best_fit_index(self, process):
		"""Return the first index in memory of a free partition that can fit
		 the specified process for Best-Fit.
		Assume defragmentation has just occurred, if it was necessary.
		"""
		# Allocate process P to the smallest free partition
		#  that's big enough to fit process P.
		possible_partitions = []

		free_partition_bounds = self.get_free_partition(0)

		while True:
			free_partition_bounds = self.get_free_partition(
				free_partition_bounds[1])
			# We haven't seen this free partition before.
			if free_partition_bounds not in possible_partitions:
				possible_partitions.append(free_partition_bounds)
			# If we have, we are done looping.
			else:
				break

		if possible_partitions and len(possible_partitions) > 1:
			# Find the smallest partition in the accumulated list.
			best_fit_partition_size = min([partition[1] - partition[0]
				for partition in possible_partitions
				if partition[1] - partition[0] + 1 >= process.memory_frames])
			free_partition_bounds = next(partition for partition in possible_partitions
				if partition[1] - partition[0] == best_fit_partition_size)

		return free_partition_bounds[0]

	def worst_fit_index(self, process):
		"""Return the first index in memory of a free partition that can fit
		 the specified process for Worst-Fit.
		Assume defragmentation has just occurred, if it was necessary.
		"""
		# Allocate process P to the largest free partition
		#  that's big enough to fit process P.
		possible_partitions = []

		free_partition_bounds = self.get_free_partition(0)

		while True:
			free_partition_bounds = self.get_free_partition(
				free_partition_bounds[1])
			# We haven't seen this free partition before.
			if free_partition_bounds not in possible_partitions:
				possible_partitions.append(free_partition_bounds)
			# If we have, we are done looping.
			else:
				break

		if possible_partitions and len(possible_partitions) > 1:
			# Find the largest partition in the accumulated list.
			worst_fit_partition_size = max([partition[1] - partition[0]
				for partition in possible_partitions
				if partition[1] - partition[0] + 1 >= process.memory_frames])
			free_partition_bounds = next(partition for partition in possible_partitions
				if partition[1] - partition[0] == worst_fit_partition_size)

		return free_partition_bounds[0]

	# TODO refactor for NC
	def place_process(self, process, index):
		memory_preceding = self.memory[:index]
		end_index = index + process.memory_frames
		memory_following = self.memory[end_index:]

		self.memory = (memory_preceding + process.pid * process.memory_frames +
			memory_following)

		# If the process was previously allocated, 'refresh' it in allocated_processes
		#  so that it is designated as most recent.
		if process in [process_tuple[0] for process_tuple in self.allocated_processes]:
			self.allocated_processes = filter(lambda p: p[0].pid != process.pid,
				self.allocated_processes) # list.remove() behaves incorrectly

		self.allocated_processes.append((process, index))

	# TODO refactor for NC
	def remove_process(self, process):
		index = self.memory.find(process.pid)
		memory_preceding = self.memory[:index]
		end_index = index + process.memory_frames
		memory_following = self.memory[end_index:]

		self.memory = (memory_preceding + '.' * process.memory_frames +
			memory_following)

	def must_defragment_for(self, process):
		"""Return True if no contiguous partition of free memory is large enough
			to hold process, False otherwise.
		Assume that the total free memory is enough to hold process.
		"""
		end_free_index = 0

		while True:
			free_index = self.memory.find('.', end_free_index)

			if free_index == -1 or free_index == len(self.memory) - 1:
				break

			for index, char in enumerate(self.memory):
				if ((index > free_index and char != '.') or
						index == len(self.memory) - 1):
					end_free_index = index
					break

			if end_free_index - free_index >= process.memory_frames:
				return False

		return True

	def defragment(self):
		# Identify any processes already at the top of memory,
		#  i.e. processes whose frames won't be moved.
		stationary_end_index = 0

		for index, char in enumerate(self.memory):
			if char == '.':
				stationary_end_index = index
				break

		stationary_memory = self.memory[:stationary_end_index]
		moved_processes = [process for process in self.allocated_processes
			if self.memory.find(process[0].pid) != -1 and
				stationary_memory.find(process[0].pid) == -1]
		moved_memory = [process[0].pid * process[0].memory_frames
			for process in moved_processes]

		self.memory = stationary_memory + ''.join(moved_memory)
		frames_moved = len(''.join(moved_memory))
		self.memory += '.' * (Mnemokinesis.frames_total - frames_moved - len(stationary_memory))

		# When defragmentation occurs, all process' pending arrival times must
		#  increase according to defragmentation time.
		defrag_time = frames_moved * Mnemokinesis.t_memmove

		for process in self.process_list:
			process.arrival_times = [
				(arrival_time + defrag_time if arrival_time > self.t else arrival_time)
				for arrival_time in process.arrival_times]
			# Increase current run time for any process that caused defragmentation.
			if self.t in process.arrival_times:
				process.arrival_times[process.times_run] += defrag_time

		# And increase run times for processes that are currently running.
		for process in [process_tuple[0] for process_tuple in self.allocated_processes]:
			if self.memory.find(process.pid) != -1:
				process.run_times[process.times_run] += defrag_time

		self.t += defrag_time
		print 'time {}ms: Defragmentation complete (moved {} frames: {})'.format(
			self.t, frames_moved, ', '.join([process[0].pid
			for process in moved_processes]))

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
	#algorithms = ['NF', 'BF', 'WF', 'NC']
	algorithms = ['NF', 'BF', 'WF'] # TODO for initial testing
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