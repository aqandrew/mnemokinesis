#encoding=utf8

"""
process.py

This class represents a process being run by a Mnemokinesis memory manager.
"""

class Process(object):
	def __init__(self, pid, memory_frames, arrival_run_times):
		self.pid = pid
		self.memory_frames = memory_frames
		self.arrival_times = [int(time_pair.split('/')[0]) for time_pair in arrival_run_times]
		self.run_times = [int(time_pair.split('/')[1]) for time_pair in arrival_run_times]

		self.times_run = 0
		self.times_to_run = len(self.run_times)

	def __cmp__(self, other):
		"""
		Any “ties” that occur should be handled using the alphabetical order of
		process IDs.
		"""
		return self.pid < other.pid

	def has_terminated(self):
		return self.times_run == self.times_to_run