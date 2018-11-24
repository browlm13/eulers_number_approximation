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

import math
from decimal import *

def an(n):
	""" a(n) = n*a(n-1) + 1, a(0) = 1 """
	an = 1
	for i in range(1,n):
		an = i*an + 1
	return an

def eulers(t):
	""" 
		easy on memory - t, i, v, at (numbers) only variables stored
		2t multiplications, t additions, 1 division - 3t + 1 arithmetic operations
		Big O of t
	"""
	v, at = 1.0, 1.0
	for i in range(1,t+1):
		at = i * at + 1
		v *= i
	return at/v

def eulers2(t):
	""" 
		requires t slots in memory to store 1/i! values in addition to storing i and t
		t divisions, t +1 additions - 2t +1 arithmetic operations
		Big O of t
	"""
	v = np.empty(shape=(t+1,))
	v[0] = 1
	for i in range(1, t+1):
		v[i] = v[i-1]/i
	return sum(v)

def eulers_precise(t, prec=100):
	getcontext().prec = prec
	v, at = Decimal(1.0), Decimal(1.0)
	for i in range(1,t+1):
		vi = i
		at = vi * at + Decimal(1.0)
		v *= vi
	return at/v


def magnitude(x, prec=None):
	"""order of magnitude of x"""
	if Decimal(x).is_zero():
		return prec
	return Decimal(x).log10().quantize(Decimal('1.'), rounding=ROUND_UP)


if __name__ == "__main__":

	# Mathmatica
	e_true = 2.71828182845

	t = 17 # 52 total arithmetic operations, 16 d.p.a
	e_hat = eulers(t)
	error = abs(e_hat - e_true)

	print("t=%s:\n\ttrue value = %s\n\tapproximation = %s,\n\terror = %s" % (t, e_true, e_hat, error))

	# higher precision

	t = 462 # 1387 total arithmetic operations, 1034 d.p.a
	prec = 1034
	e_hat = eulers_precise(t,prec)
	getcontext().prec = prec

	# Mathmatica
	e_true = Decimal('2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274274663919320030599218174135966290435729003342952605956307381323286279434907632338298807531952510190115738341879307021540891499348841675092447614606680822648001684774118537423454424371075390777449920695517027618386062613313845830007520449338265602976067371132007093287091274437470472306969772093101416928368190255151086574637721112523897844250569536967707854499699679468644549059879316368892300987931277361782154249992295763514822082698951936680331825288693984964651058209392398294887933203625094431173012381970684161403970198376793206832823764648042953118023287825098194558153017567173613320698112509961818815930416903515988885193458072738667385894228792284998920868058257492796104841984443634632449684875602336248270419786232090021609902353043699418491463140934317381436405462531520961836908887070167683964243781405927145635490613031072085103837505101157477041718986106873969655212671546889570350354021234078498193343210681701210056278')
	error = Decimal(e_hat - e_true).copy_abs()

	print("t=%s:\n\tmagnitude of error = %s" % (t, magnitude(error, prec)))
