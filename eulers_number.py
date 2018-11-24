#!/usr/bin/env python3

"""
	Efficient approximation of Euler's number
	
	combining t terms in the series expansion of e for efficient evaluation,
	
		e = 1/0! + 1/1! + 1/2! + ...
	
	computing approximation for e,
	
		a0 = 1.0
		a_{t} = (1.0 + t) * a_{t-1} + 1.0
		p_{t} = a_{t} / (1.0 + t)!

		as t -> inf:
			e = p_{t}

		a_{t} = (1 + t)((1 + t - 1)(...((1 + 1)*1 + 1)...) + 1) + 1
		
		a_{t}'s are a member of this sequence:
		
			http://oeis.org/A002627
	
"""

__author__  = "LJ Brown"
__file__ = "eulers_number.py"

def eulers(t):
	""" 
		2(t+1) multiplications, 2(t+1) additions, 1 division - 4(t+1) + 1 arithmetic operations

		Big O of t

	"""
	v = 1.0
	at = 1.0
	for i in range(0,t+1):
		vi = ( 1 + i )
		at = vi * at + 1
		v *= vi
	return at/v

if __name__ == "__main__":
	# Mathmatica
	e_true = 2.718281828459045

	t = 16 # 68 total arithmetic operations
	e_hat = eulers(t)
	error = abs(e_hat - e_true)

	print("t=%s:\n\ttrue value = %s\n\tapproximation = %s,\n\terror = %s" % (t, e_true, e_hat, error))
