#!/usr/bin/env python3

"""

	can compute e starting from old approximation

	
	
"""

__author__  = "LJ Brown"
__file__ = "scratch.py"

import math 
import numpy as np

def a(t):
	""" a(t) = t*a(t-1) + 1, a(0) = 1 """
	at = 1
	for i in range(1,t+1):
		at = i*at + 1
	return at

def a_seg(t,n):
	""" 
		a(t) - a(n) = t(t-1)(...(n+2)((n+1)+ 1)...+1)+1)+1 	
	"""
	a_tmn = 1
	for i in range(n+1, t+1):
		a_tmn = i*a_tmn +1
	return a_tmn

def p(t):
	v, at = 1.0, 1.0
	for i in range(1,t+1):
		at = i * at + 1
		v *= i
	return at/v

def p_seg(t,n,n_factorial=None):

	assert t > n
	if n_factorial is None:
		n_factorial = math.factorial(n)

	v, a_tmn = n_factorial, 1
	for i in range(n+1,t+1):
		a_tmn = i*a_tmn + 1
		v *= i
	return a_tmn/v

def e_approx(t,step_size):
	e_segs = []
	for i in range(0, t, step_size+1):
		e_segs += [p_seg(i+step_size, i)]
	return sum(e_segs)

for i in range(13,14):
	print(e_approx(i, 2))


