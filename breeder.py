from __future__ import division
import os
import random
from gene import Gene

class Breeder:

	def create( self, k ):
		generation = []
		for i in range( 0 , k ):
			v1 = random.random()
			v2 = random.random()
			v3 = random.random()
			g = Gene( v1 , v2 , v3 )
			generation.append(g)

		return generation


	def getBests( self, n , generation):
		bests = []
		generation.sort(key = lambda x: x.sharpe , reverse=True)

		bests = generation[ :int(n) ]
		return bests

	def populate( self, bests, n ):
		bsize = len( bests )
		toAdd = n - bsize
		generation = bests
		for i in range( 0, toAdd ):
			r1 = random.randint( 0 , (bsize - 1) )
			w1 = bests[ r1 ].w1 + ( (random.random()  ) / 3 )
			r2 = random.randint( 0 , (bsize - 1) )
			w2 = bests[ r2 ].w2 + ( (random.random()  ) / 3 )
			r3 = random.randint( 0 , (bsize - 1) )
			w3 = bests[ r3 ].w3 + ( (random.random()  ) / 3 )
			g = Gene( w1,w2,w3 )
			generation.append(g)
		return generation	


