#!/usr/bin/python

def interpolate(al, ah, a, vl ,vh):
	a_d = float(a - al)/float(ah - al)
	return ((1 - a_d)*vl + a_d*vh)

def squareInterpolate(xl, yl, xh, yh, x, y, vll, vlh, vhl, vhh):
	v0 = interpolate(xl, xh, x, vll, vhl)
	v1 = interpolate(xl, xh, x, vlh, vhh)
	return interpolate(yl, yh, y, v0, v1)
	
xl=1
yl=4

xh=3
yh=10

x=2
y=7

vll=10
vlh=20

vhl=20
vhh=20

print(squareInterpolate(xl, yl, xh, yh, x, y, vll, vlh, vhl, vhh))



