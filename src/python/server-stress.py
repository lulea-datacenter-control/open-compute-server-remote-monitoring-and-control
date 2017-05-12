#!/usr/bin/env python

#
# Copyright (c) 2017 Martin Eriksson
#		2017 Riccardo Lucchese <riccardo.lucchese@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import platform
import re
import time
import argparse
import subprocess
import numpy
import scipy
import scipy.io
import multiprocessing
import shlex
import psutil


class hw_platform(object):
	def __init__(self):
		self._is_linux = (platform.system() == 'Linux')
		self._nr_sockets = None
		self._socket_cores = None

	def is_linux(self):
		return self._is_linux
		
	def _read_topology(self):
		assert(self._nr_sockets is None)
		assert(self._socket_cores is None)

		#
		# retrieve the nr. of cores and nr. of sockets
		#
		nr_cores = multiprocessing.cpu_count()
		if self.is_linux():
			p = subprocess.Popen(shlex.split('numactl -H'), shell=False,	\
						 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			p.wait()
			info, err = p.communicate()
			
			lines = info.splitlines()
			nr_sockets = None
			for k in lines:
					match = re.match('available:\s(\d+)\snodes\s[(]\d[-]\d[)]', k)
					if match is not None:
						nr_sockets = int(match.group(1))
						break

			if nr_sockets == None:
				print 'hw_platform, cannot find the number of sockets'
				assert False

			self._nr_sockets = nr_sockets
			self._socket_cores = []
			for i in range(nr_sockets):
				self._socket_cores.append([])

			nr_cores_per_socket = psutil.cpu_count()/2
			fmt = '\s(\d+)'*nr_cores_per_socket
			for sockid in range(nr_sockets):
				for l in lines:
					#print "matching line:", l
					match = re.match('node\s%d\scpus:%s' % (sockid, fmt), l)
					if match is not None:
						for i in range(nr_cores_per_socket):
							self._socket_cores[sockid].append(int(match.group(i+1)))

		else:							
			self._nr_sockets = 2
			self._sockets_cores.append(list(range(nr_cores/2)))
			self._sockets_cores.append(list(range(nr_cores/2, nr_cores)))

	def get_nr_sockets(self):
		if self._nr_sockets is None:
			self._read_topology()

		return self._nr_sockets

	def get_cores_per_socket(self, sockid):
		if self._nr_sockets is None:
			self._read_topology()

		assert sockid >= 0
		assert sockid <= self._nr_sockets
		return self._socket_cores[sockid]

	def get_nr_cores_per_socket(self, sockid):
		if self._nr_sockets is None:
			self._read_topology()

		cores = self.get_cores_per_socket(sockid)
		return len(cores)

	def get_cores_string(self, sockid):
		if self._nr_sockets is None:
			self._read_topology()

		ids = self.get_cores_per_socket(sockid)
		return ','.join([str(x) for x in ids])

	def kill_with_children(self, proc_pid):
		p = psutil.Process(proc_pid)
		for c in p.children(recursive=True):
			try:
				c.kill()
			except:
				print 'warning, failed to kill child %s' % repr(c)
		try:
			p.kill()
		except:
			print 'warning, failed to kill proc %s' % repr(p)



class pseudo_random_binary_signal(object):
	def __init__(self, name, size, period):
		assert isinstance(name, str)
		assert len(name) > 0
		assert isinstance(size, (int, float))
		assert size > 0

		self._name = name
		self._size = size;
		self._period = period;
		self._time = numpy.arange(0, size*period, period)
		self._values = numpy.random.choice([0, 1], size = (len(self._time)))
		assert(len(self._time) == len(self._values));

	def get_name(self):
		return self._name

	def get_size(self):
		return self._size

	def get_value_at_time(self, t):
		assert isinstance(t, (int,float))
		assert t>=0.

		#
		# actually fetch the value by looking at self._time and self._values
		#
		idx = max(0, numpy.searchsorted(self._time, t) - 1);
		assert(idx >= 0)
		assert idx < len(self._time);
		value = self._values[idx]
		return value
		
	def dump(self):
		print "pseudo_random_binary_signal.dump()"
		print "  name   : %s" % self._name
		print "  size   : %d" % self._size
		print "  values : %s" % repr(self._values)
		print "  time   : %s" % repr(self._time)
		print " period : %d" % self._period

	def get_time(self):
		return numpy.array(self._time)

	def get_values(self):
		return numpy.array(self._values)



class sysid_cpu_load(pseudo_random_binary_signal):
	def __init__(self, sockid, size, period):
		assert isinstance(sockid, int)
		assert sockid >= 0
		
		name = 'socket%02d' % sockid
		pseudo_random_binary_signal.__init__(self, name, size, period)
		self._socket_id = sockid
		
	def get_socket_id(self):
		return self._socket_id


def stress_cpus(timelength, period):
	#print timelength
	#print period
	assert isinstance(timelength, (int,float))
	assert timelength > 0
	assert isinstance(period, (int,float))
	assert period > 0
	

	endtest_time = timelength * 3600

	trace_size = endtest_time/period
	print "Stress-test ends in %d seconds" % endtest_time

	# retrieve the hw spec
	hw = hw_platform()
	nr_sockets = hw.get_nr_sockets()
		
	#
	# generate the pseudo random binary signals (i.e., computational loads) to
	# use for sysid
	#
	print "Generating %d socket loads ..." % nr_sockets
	socket_loads = []
	for sockid in range(nr_sockets):
		l = sysid_cpu_load(sockid, trace_size, period)
		socket_loads.append(l)
		l.dump()		
	# 
	# enter the main-loop where we set the computational loads that have been
	# computed above    
	#
	zero_time = None
	cur_socket_loads = [0.]*nr_sockets;
	stress_ng_procs = [None]*nr_sockets;
	try:
		from subprocess import DEVNULL # py3k
	except ImportError:
		DEVNULL = open(os.devnull, 'wb')
	while True:
		# get current time from the start 
		cur_time = time.time()
		meas_t = cur_time
		if zero_time == None:
			zero_time = meas_t
		meas_t = meas_t - zero_time
			
		if meas_t >= endtest_time:
			for p in stress_ng_procs:
				if p is not None:
					hw.kill_with_children(p.pid)
			print "Reached end of test: %.2f / %.2f [sec]" % (meas_t, endtest_time)
			break

		for i,load in enumerate(socket_loads):
			sockid = load.get_socket_id()
			cur_load = cur_socket_loads[i]
			desired_load = load.get_value_at_time(meas_t)

			if cur_load != desired_load:
				print "%.3f: socket %d, load --> %d" % (meas_t, sockid, desired_load)

				p = stress_ng_procs[i]
				if p is not None:
					#print 'killing stress-ng on socket %d (pid=%d)' % (sockid, p.pid)
					hw.kill_with_children(p.pid)
					p = None
				else:
					#print 'starting stress-ng on socket %d' % (sockid)
					core_str = hw.get_cores_string(sockid)
					#print core_str
					nr_cores = hw.get_nr_cores_per_socket(sockid)
					#print nr_cores
					cmd = "taskset -c %s stress-ng --class cpu  --sequential %d --timeout 10m" % (core_str, nr_cores)
					print "  cmd: %s" % cmd
					p = subprocess.Popen(shlex.split(cmd), shell=False, stdout=DEVNULL, stderr=DEVNULL)
					
				stress_ng_procs[i] = p
				cur_socket_loads[i] = desired_load

		time.sleep(0.5)
	return socket_loads, zero_time

			
def save_matlab(socket_loads, zero_time, timelength, period, path):
	mdict = {}
	# save nr of sockets
	mdict['nr_sockets'] = len(socket_loads)
	mdict['s_t'] = zero_time
	mdict['timelength'] = timelength
	mdict['period'] = period
	for load in socket_loads:
		name = load.get_name()
		time_var = name + '_time'
		mdict[time_var] = load.get_time()

		value_var = name + '_values'
		mdict[value_var] = load.get_values()

		sockid = load.get_socket_id()
	
	#print mdict
	scipy.io.savemat(path, mdict)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-t","--timelength", dest="timelength", default=1, help="The runtime of the script (default 1h)")
	parser.add_argument("-T","--period", dest="period", default=5, help="The sampling period for --timelength in seconds (default 5s)")
	parser.add_argument("-m","--outfile-matlab", dest="outfile_mat", default=None, help="Path to the output file (matlab .mat format)")
	args = parser.parse_args()

	try:
		period = float(args.period)
	except:
		print "The period \"%s\" is not a numeric type" % args.period
		sys.exit(1)
	try:
		timelength = float(args.timelength)
	except:
		print "The timelength \"%s\" is not a numeric type" % args.timelength
		sys.exit(1)

	socket_loads, zero_time = stress_cpus(timelength, period)
	save_matlab(socket_loads, zero_time, timelength, period, args.outfile_mat)
	
	sys.exit(0)
