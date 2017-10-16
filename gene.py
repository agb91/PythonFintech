from __future__ import division

class Gene:

	def __init__(self, w1, w2, w3):
		self.tot = (w1+w2+w3)
		self.w1 = w1 / self.tot
		self.w2 = w2 / self.tot
		self.w3 = w3 / self.tot
		self.tot = 1
		self.sharpe = 0


	def printStr( self ):
		print( "w1: " + str( self.w1 ) + ";  w2:" + str( self.w2 )
			 + ";  w3:" + str( self.w3 )  + ";  SHARPE: " + str(self.sharpe) )




    