#!/usr/bin/env python3

"""
	Efficient approximation of Euler's number
	
	
	combining t terms in the series expansion of e for efficient evaluation,
	
		e = 1/0! + 1/1! + 1/2! + ...

		e ~= [t(t-1(...4(3(2(1(1) +1)+1)+1)+1...)+1) +1]/t!

		compute t! while evaluating the nested seiers
	
	computing approximation for e,
	
		a(0) = 1.0
		a(t) = t * a(t-1) + 1.0
		a(t) ~= t!e
		
		p(t) = a(t)/t!
		p(t) ~= e
		
		as t -> inf:
			e = p(t)

	a(t)'s are a members of this sequence:
		
		1, 2, 5, 16, 65, 326, 1957, ...
			
		a(t) = t! sum(i=0,i=t,1/i!) ~= t!e
		a(t) = t*a(t-1) + 1, a(0) = 1. 

		http://oeis.org/A000522
			



	
"""

__author__  = "LJ Brown"
__file__ = "eulers_number.py"

def an(n):
	""" a(n) = n*a(n-1) + 1, a(0) = 0 """
	an = 0
	for i in range(1,n):
		an = i*an + 1
	return an

def eulers(t):
	""" 
		2t multiplications, t additions, 1 division - 3t + 1 arithmetic operations
		Big O of t
	"""
	v, at = 1.0, 1.0
	for i in range(1,t+1):
		vi = i
		at = vi * at + 1
		v *= vi
	return at/v

if __name__ == "__main__":
	# Mathmatica
	e_true = 2.718281828459045

	t = 17 # 52 total arithmetic operations, 16 d.p.a
	e_hat = eulers(t)
	error = abs(e_hat - e_true)

	print("t=%s:\n\ttrue value = %s\n\tapproximation = %s,\n\terror = %s" % (t, e_true, e_hat, error))
