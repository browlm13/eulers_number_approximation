#!/usr/bin/env python3

"""

	Racing methods for approximating euler's number
	
	
	general methods found online: eulers2, eulers3	(O(n^2))
	methods created in this directory: eulers, parallel_eulers (O(n))
	
"""

__author__  = "LJ Brown"
__file__ = "test_eulers_number.py"

import multiprocessing as mp
import math 
from decimal import *

import numpy as np

#
# half and half
#

def P(a, b, output, a_factorial):
	""" 
		p(t) = p(t-1) + 1/t!
		p(t) = p(t-2) + 1/(t-1)! + 1/t!
		p(b) = p(a) + 1/(a+1)! + ... + 1/(b-1)! + 1/b!
		p(b) - p(a) = 1/(a+1)! + 1/(a+2)! + ... + 1/(b-1)! + 1/b!, a < b

		a(a,a+1) = a + 1
		a(a,a+2) = (a + 2) * a(a,a+1) + 1
		a(a,b) = b * a(a,b-1) + 1
	"""
	ab = Decimal(1)
	v = a_factorial
	for i in range(a+1, b+1):
		ab = Decimal(i)*ab + Decimal(1)
		v *= Decimal(i)
	output.put(ab/v)


def falling_factorial(a,b, output):
	""" computes a*(a+1)*...*(b-1)*b """
	n = Decimal(1)
	for i in range(a+1,b+1):
		n*=Decimal(i)
	output.put(n)


def generate_args_list(t, n=4):
	# compute arguments for process
	step = math.floor(t/n)

	args_list=[(step*i, step*(i+1), output) for i in range(0, n-1)]
	if args_list[-1][1] != t:
		args_list.append((args_list[-1][1], t, output))

	return args_list


def parallel_eulers(t, n=4, prec=100):

	assert n > 1

	# Define an output queue
	output = mp.Queue()

	getcontext().prec = prec

	ff_args_list = generate_args_list(t, n=n)


	# Setup list of processes
	falling_factorial_ps = [mp.Process(target=falling_factorial, args=a) for a in ff_args_list]


	# Run processes
	for p in falling_factorial_ps:
	    p.start()

	# Exit the completed processes
	for p in falling_factorial_ps:
	    p.join()

	# Get process results from the output queue
	falling_factorials = [output.get() for p in falling_factorial_ps]

	# set up args list for euler steps

	e_args_list = []

	# current factorial for argument
	a_factorial = 1
	for z in zip(ff_args_list, falling_factorials):
		a, b, o , ff = *z[0], z[1] 
		# e_args_list.append((a,b,o,a_factorial))

		e_args_list.append((a+1,b,o,a_factorial*(a+1)))
		a_factorial *= ff


	# create euler parrallel processes
	euler_ps = [mp.Process(target=P, args=a) for a in e_args_list]


	# Run processes
	for p in euler_ps:
	    p.start()

	# Exit the completed processes
	for p in euler_ps:
	    p.join()

	# Get process results from the output queue
	Ps = [output.get() for p in euler_ps]

	return sum(Ps) + 1




def parallel_falling_factorial(t, n=4):
	""" computes t! """

	assert n > 1

	args_list = generate_args_list(t, n=n)

	# Setup list of processes
	processes = [mp.Process(target=falling_factorial, args=a) for a in args_list]



	# Run processes
	for p in processes:
	    p.start()

	# Exit the completed processes
	for p in processes:
	    p.join()

	# Get process results from the output queue
	results = [output.get() for p in processes]


	return np.prod(results)

def eulers_precise(t, prec=100):
	getcontext().prec = prec
	v, at = Decimal(1.0), Decimal(1.0)
	for i in range(1,t+1):
		at = Decimal(i) * at + Decimal(1.0)
		v *= Decimal(i)
	return at/v

def eulers2_precise(t, prec=100):
	""" 
		requires t slots in memory to store 1/i! values in addition to storing i and t
		fast t divisions, t additions - 2t arithmetic operations
		Big O of t

		memory: t + 2 (not including array pointers)
		operations: 2t + 1 (not including counter)
	"""
	v = [1]*(t+1)
	v[0] = Decimal(1.0)
	e = Decimal(v[0])
	for i in range(1, t+1):
		v[i] = Decimal(v[i-1]/i)
		e +=  v[i]

	return e 

def eulers3_precise(t, prec=100):
	""" 
		similar to eulers2 except only stores 2 additional values in memory
	"""
	v0 = Decimal(1.0)
	e = Decimal(v0)
	for i in range(1, t+1):
		v1 = Decimal(v0/i)
		e +=  v1
		v0 = v1
	return e 

def magnitude(x, prec=None):
	"""order of magnitude of x"""
	if Decimal(x).is_zero():
		return prec
	return Decimal(x).log10().quantize(Decimal('1.'), rounding=ROUND_UP)


if __name__ == "__main__":

	# https://apod.nasa.gov/htmltest/gifcity/e.2mil
	path = "e_2million.txt"
	file = open(path,'r')
	e_string = file.readlines()
	e_string = [l[:-1] for l in e_string]
	e_string = ''.join(e_string)


	# time performace differences
	import time

	step = 500
	low = 2000
	high = 20000
	ratio = 0.75

	ts = [t for t in range(low,high,step)]
	precs = [int(t*ratio) for t in ts]
	runs_per = 3 # take average time of runs

	methods = [eulers2_precise, eulers_precise, parallel_eulers, eulers3_precise]
	times = [[None]*len(ts) for i in range(len(methods))]
	approximations_errors = [[None]*len(ts) for i in range(len(methods))]

	j = 0
	for t, prec in zip(ts,precs):

		# set precision
		getcontext().prec = prec
		e_true = Decimal(e_string[:prec])

		completion_percentage_estimate = j/len(ts)*100*(prec/precs[-1])**2
		if int(completion_percentage_estimate)%2 == 0:
			print("percentage complete: ", completion_percentage_estimate)

		for i,m in enumerate(methods):

			run_times = []
			for r in range(runs_per):

				t0 = time.time()
				# run
				approx = m(t, prec=prec)
				t1 = time.time()

				total = t1-t0

				run_times.append(total)

			avg_run_time = sum(run_times)/runs_per
			times[i][j] = avg_run_time*10

			error = Decimal(approx - e_true).copy_abs()

			approximations_errors[i][j] = magnitude(error, prec)

		j+= 1

	m1_times, m2_times, m3_times, m4_times = times
	m1_errs, m2_errs, m3_errs, m4_errs = approximations_errors
	
	import matplotlib.pyplot as plt

	plt.plot(ts,m1_times,'b*-', label = 'euler2')
	plt.plot(ts,m2_times,'r*-', label = 'euler')
	plt.plot(ts,m3_times,'g*-', label = 'parallel euler')
	plt.plot(ts,m4_times,'y*-', label = 'euler3')
	plt.xlabel('precision d.p.a', fontsize=18)
	plt.ylabel('average time (seconds)', fontsize=16)
	plt.legend()
	plt.show()

	plt.plot(ts, m1_errs, 'b*-', label = 'euler2')
	plt.plot(ts, m2_errs, 'r*-', label = 'euler')
	plt.plot(ts,m3_errs,'g*-', label = 'parallel euler')
	plt.plot(ts,m4_errs,'y*-', label = 'euler3')
	plt.xlabel('precision d.p.a', fontsize=18)
	plt.ylabel('magnitude of error', fontsize=16)
	plt.grid()
	plt.legend()
	plt.show()
