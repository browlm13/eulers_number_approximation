#!/usr/bin/env python3

"""
	Efficient approximation of Euler's number
"""

__author__  = "LJ Brown"
__file__ = "eulers_number.py"

def eulers(t):
	""" 
		2(t+1) multiplications, 2(t+1) additions, 1 division - 4(t+1) + 1 operations

		Big O of t

	"""
	v = 1.0
	at = 1.0

	for i in range(0,t+1):
		vi = ( 1 + i )
		at = vi * at + 1
		v *= vi

	return at/v

# Mathmatica
e_true = 2.718281828459045235360287471352662497757247093699959574966967627724076630353547594571382178525166427427466391932003059921817413596629043572900334295260

t = 16 # 68 total arithmetic operations
e_hat = eulers(t)
error = abs(e_hat - e_true)

print("t=%s:\n\ttrue value = %s\n\tapproximation = %s,\n\terror = %s" % (t, e_true, e_hat, error))
