"""
process.py

This class represents a process being run by a Mnemokinesis memory manager.
"""

class Process(object):
	def __init__(self, pid):
		this.pid = pid

	def __cmp__(self, other):
		"""
		Any “ties” that occur should be handled using the alphabetical order of
		process IDs.
		"""
		return self.pid < other.pid