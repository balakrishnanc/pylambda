#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# lambda.py
# Created by Balakrishnan Chandrasekaran on 2017-10-17 14:44 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balakrishnan.c@gmail.com>.
#

"""
lambda.py
Lambda calculus in Python.
"""

__author__ = 'Balakrishnan Chandrasekaran <balakrishnan.c@gmail.com>'
__version__ = '1.0'
__license__ = 'MIT'


# Identity function.
ID = lambda z: z


# Void value as a function.
VOID = ID
# "Void" value for debugging purposes.
def _VOID(_):
    raise Exception('Cannot invoke VOID!')


# Logical values as functions.
TRUE  = lambda true_value: lambda false_val: true_value()
FALSE = lambda true_value: lambda false_value: false_value()

# `IF`-conditional.
IF = lambda cond: lambda true_value: lambda false_value: cond(true_value)(false_value)


# Function composition.
compose = lambda f,g: lambda x: f(g(x))


# Church numerals.
ONE   = lambda f: f
TWO   = lambda f: compose(f, f)
THREE = lambda f: compose(f, TWO(f))

# Turn any (Python) number into a Church numeral.
# Accept a one-argument function and an identify value, and convert the (Python)
# number to a Church numeral.
def numeral(n):
    return lambda f: lambda z: z if n == 0 else f(numeral(n-1)(f)(z))

# Church numerals, continued.
FOUR  = numeral(4)
EIGHT = numeral(8)

# Increment function.
INC = lambda x: x+1

# Convert church numerals to natural numbers.
natify = lambda f: f(INC)(0)


# Successor.
# Takes a Church numeral and outputs it's successor by applying the function one
# more time.
SUCC = lambda n: lambda f: lambda z: f(n(f)(z))


# Addition.
# SUM = lambda n: lambda m: lambda f: lambda z: n(f)(m(f)(z))
SUM = lambda n: lambda m: lambda f: compose(n(f), m(f))


# Multiplication.
# MULT = lambda n: lambda m: lambda f: lambda z: n(m(f))(z)
# MULT = lambda n: lambda m: lambda f: n(m(f))
# MULT = lambda n: lambda m: lambda f: compose(n,m)(f)
MULT = lambda n: lambda m: compose(n,m)


# Pairs.
PAIR  = lambda a: lambda b: lambda f: f(a)(b)
LEFT  = lambda pair: pair(lambda a: lambda b: a)
RIGHT = lambda pair: pair(lambda a: lambda b: b)


# Lists.
NIL  = lambda onnil: lambda onlist: onnil()
CONS = lambda hd: lambda tl: lambda onnil: lambda onlist: onlist(hd)(tl)
NILP = lambda lst: lst (lambda: TRUE) (lambda hd: lambda tl: FALSE)
HEAD = lambda lst: lst (VOID) (lambda hd: lambda tl: hd)
TAIL = lambda lst: lst (VOID) (lambda hd: lambda tl: tl)


# U Combinator.
U = lambda f: f(f)


# Recursion through self-application.
#
# fact = lambda n: 1 if n <= 0 else n*fact(n-1)
# fact = ((lambda f: lambda n: 1 if n <= 0 else n*fact(n-1))
#         (lambda f: lambda n: 1 if n <= 0 else n*fact(n-1)))
# ---(1)
# Assume g = (lambda f: lambda n: 1 if n <= 0 else n*fact(n-1))
# then fact = g(g), from (1)
#
# Apply the U combinator to `fact`, fact = U(g) = g(g)
#
# fact = U(lambda f: lambda n: 1 if n <= 0 else n*fact(n-1))
#
# > `fact` above still has a recursive call to `fact`.
#

# Fixed points of functions.
#
# fact = lambda n: 1 if n <= 0 else n*fact(n-1)
#
# Let's assume the following.
# f = lambda f: fact
#
#    f = lambda f: lambda n: 1 if n <= 0 else n*fact(n-1)
# => f = lambda f: lambda n: 1 if n <= 0 else n*f(n-1)
#

# Y combinators.
#
# Y(F) = f, where `f` is the fixed point of the function F.
#
# Y(F) = f
#      => F(f) = f
#      => F(Y(F)), since f = Y(F)
#      => Y(F) = F(Y(F))
#
# Y = lambda F: F(Y(F))
#
# Does not work, since Python tries to eagerly compute 'Y'.
#
# Apply eta conversion (or, more precisely, eta abstraction).
# e <=> lambda x: e(x)
#
# Y(F) <=> lambda x: Y(F)(x)
#
# Y = lambda F: F(lambda x: Y(F)(x))
# (The above version works, but we have a reference to `Y`.)
#
# Apply `U` combinator to eliminate the explicit recursion in `Y`.
#
# Y = U(lambda h: lambda F: F(lambda x: U(h)(F)(x)))
#
# Inline `U`.
#
# Inlining the outer `U`,
# Y = ((lambda h: lambda F: F(lambda x: U(h)(F)(x)))
#      (lambda h: lambda F: F(lambda x: U(h)(F)(x))))
#
# Inlining the inner `U`,
Y = ((lambda h: lambda F: F(lambda x: h(h)(F)(x)))
     (lambda h: lambda F: F(lambda x: h(h)(F)(x))))


if __name__ == '__main__':
    print("> Church numerals.")
    print(">")
    print("> numeral({0})(lambda x: x+1) (id: {2}): {1}".format(0, numeral(0)(lambda x: x+1)(0), 0))
    print("> numeral({0})(lambda x: x+1) (id: {2}): {1}".format(1, numeral(1)(lambda x: x+1)(0), 0))
    print("> numeral({0})(lambda x: x+1) (id: {2}): {1}".format(2, numeral(2)(lambda x: x+1)(0), 0))
    print("> numeral({0})(lambda x: x+1) (id: {2}): {1}".format(3, numeral(3)(lambda x: x+1)(0), 0))
    print("> numeral({0})(lambda x: x+1) (id: {2}): {1}".format(7, numeral(7)(lambda x: x+1)(0), 0))
    print(">")
    print("> numeral({0})(lambda x: 2*x) (id: {2}): {1}".format(0, numeral(0)(lambda x: 2*x)(1), 1))
    print("> numeral({0})(lambda x: 2*x) (id: {2}): {1}".format(1, numeral(1)(lambda x: 2*x)(1), 1))
    print("> numeral({0})(lambda x: 2*x) (id: {2}): {1}".format(2, numeral(2)(lambda x: 2*x)(1), 1))
    print("> numeral({0})(lambda x: 2*x) (id: {2}): {1}".format(3, numeral(3)(lambda x: 2*x)(1), 1))
    print("> numeral({0})(lambda x: 2*x) (id: {2}): {1}".format(7, numeral(7)(lambda x: 2*x)(1), 1))
    print(">")
    print("> using `numeral(x)`")
    print("> numeral({0}) = natify(numeral{0}) = {1}".format(0, natify(numeral(0))))
    print("> using `compose(f,g)`")
    print("> numeral({0}) = natify(numeral{0}) = {1}".format(1, natify(ONE)))
    print("> numeral({0}) = natify(numeral{0}) = {1}".format(2, natify(TWO)))
    print("> numeral({0}) = natify(numeral{0}) = {1}".format(3, natify(THREE)))
    print("> using `numeral(x)`")
    print("> numeral({0}) = natify(numeral{0}) = {1}".format(4, natify(FOUR)))
    print("> numeral({0}) = natify(numeral{0}) = {1}".format(8, natify(EIGHT)))
    print(">")
    print("> Successors (SUCC)")
    print("> SUCC({0}): {1}".format(1, SUCC(ONE)(INC)(0)))
    print("> SUCC({0}): {1}".format(2, SUCC(TWO)(INC)(0)))
    print("> SUCC({0}): {1}".format(4, SUCC(FOUR)(INC)(0)))
    print("> SUCC({0}): {1}".format(8, SUCC(EIGHT)(INC)(0)))
    print(">")
    print("> Sum.")
    print("> SUM({0})({1}): {2}".format(2, 8, SUM(TWO)(EIGHT)(INC)(0)))
    print(">")
    print("> Multiplication.")
    print("> MULT({0})({1}): {2}".format(2, 8, MULT(TWO)(EIGHT)(INC)(0)))
    print(">")
    print(Y(lambda f: lambda n: 1 if n <= 0 else n*f(n-1))(5))
