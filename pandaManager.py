from __future__ import division
import pandas as pd  
import requests
import os
import numpy as np
import csv
import matplotlib.pyplot as plt  
from sklearn import preprocessing
from gene import Gene
from breeder import Breeder


def dateDifferenceYears( dateBegin , dateEnd ):
	yearBegin = dateBegin.split('-')[0]
	yearEnd = dateEnd.split('-')[0]
	return int( int(yearEnd) - int(yearBegin) )

def getStdDev( column ):
	return np.std(column)	

def getAnnualizedReturn( dateBegin, dateEnd, colname, column ):
	beginValue = column.loc[dateBegin , colname]
	endValue = column.loc[dateEnd , colname]
	return (( endValue - beginValue ) / dateDifferenceYears(dateBegin , dateEnd))

def analyzeData( path , dateRange, dateBegin, dateEnd, closeColumname ):
	dfOb = pd.read_csv(path, index_col='Date', parse_dates=True, na_values=['nan'])
	dfDatesOb = dateRange.join(dfOb)
	#the following line normalizes the values
	dfDatesOb = dfDatesOb[['AdjClose']] * ( 100 / dfDatesOb.loc[dateBegin , 'AdjClose'])
	dfDatesOb.columns = [closeColumname]
	stdDevOb = getStdDev(dfDatesOb[closeColumname])
	annualizedReturnOb = getAnnualizedReturn( dateBegin, dateEnd, closeColumname, dfDatesOb )
	sharpeOb = annualizedReturnOb / stdDevOb
	return annualizedReturnOb, stdDevOb , sharpeOb, dfDatesOb

def addDD( df, colTotalName ):
	maxSince = 0.0
	DDs = []
	for index, row in df.iterrows():
		if( row[colTotalName] > maxSince ):
			maxSince = row[colTotalName]
		DD = ((maxSince - row[colTotalName]) / maxSince ) * 100.0
		if(DD < 0.0 ):
			DD = 0.0	
		DDs.append( DD )
	df[ "DDs" ] = DDs 
	return df

def tripleMerger( first, second, third , gene, n1, n2, n3, dateBegin, dateEnd, it , isPlot ):
	dfDatesGeneral = first.join( second )
	dfDatesGeneral = dfDatesGeneral.join( third )
	totalSum = dfDatesGeneral.loc[: , n1] * gene.w1 + dfDatesGeneral.loc[: , n2] * gene.w2 + dfDatesGeneral.loc[: , n3] * gene.w3
	dfDatesGeneral['total' + str(it)] = totalSum 
	dfDatesGeneral = addDD(dfDatesGeneral , 'total' + str(it) )
	stdDevTot = getStdDev(dfDatesGeneral['total' + str(it)])
	annualizedReturnTot = getAnnualizedReturn( dateBegin, dateEnd, 'total' + str(it), dfDatesGeneral )
	sharpeTot = annualizedReturnTot / stdDevTot 
	sharpeTotAdj = sharpeTot - ( dfDatesGeneral["DDs"].max() / 300.0 ) 
	
	if(isPlot == 1):
		dfDatesGeneral.plot()
	return annualizedReturnTot, stdDevTot, sharpeTot, dfDatesGeneral , sharpeTotAdj

def main():
	#set date range
	dateBegin = '2005-05-01'
	dateEnd = '2017-05-01'
	yearsLength = dateDifferenceYears( dateBegin , dateEnd )
	print( 'we are reasoning on a span of: ' + str( yearsLength ) + ' years ' )

	dates = pd.date_range( start = dateBegin , end = dateEnd , freq = '1MS' )
	dfDates = pd.DataFrame( index = dates )

	print ('-------------------------- ANALYSIS PART ---------------------------')
	#read about bonds
	print( '##########################  BONDS  ##########################' )
	annualizedReturnBond, stdDevBond, sharpeBond, dfDatesBond = analyzeData( 'BOND.csv', dfDates, dateBegin, dateEnd, 'AdjCloseBonds' )
	print( 'standard deviation Bonds: ' + str(stdDevBond) )
	print ( 'annualized return Bonds: ' + str( annualizedReturnBond ))
	print ( 'Sharpe Bonds: ' + str( sharpeBond ))
	print( '\n\n' )

	print( '##########################  STOCKS  ##########################' )
	annualizedReturnSPY, stdDevSPY, sharpeSPY, dfDatesSPY = analyzeData( 'SPY.csv', dfDates, dateBegin, dateEnd, 'AdjCloseStocks' )
	print( 'standard deviation Stocks: ' + str(stdDevSPY) )
	print ( 'annualized return Stocks: ' + str( annualizedReturnSPY ))
	print ( 'Sharpe Stocks: ' + str( sharpeSPY ))
	print('\n\n')

	print( '##########################  GOLD  ##########################' )
	annualizedReturnGold, stdDevGold, sharpeGold, dfDatesGold = analyzeData( 'GLD.csv', dfDates, dateBegin, dateEnd, 'AdjCloseGold' )
	print( 'standard deviation Gold: ' + str(stdDevGold) )
	print ( 'annualized return Gold: ' + str( annualizedReturnGold ))
	print ( 'Sharpe Gold: ' + str( sharpeGold ))
	print('\n\n')

	print ('\n\n\n-------------------------- AI PART ---------------------------\n\n\n')
	print( '##########################  TOTAL  ##########################\n' )

	epochs = 30
	population = 20
	breeder = Breeder()



	generation = breeder.create( population )

	for epoch in range( 0 , epochs ):

		generation = breeder.populate( generation , population )	
		for i in range( 0, len(generation) ):
			#generation[i].printStr()
			g = generation[i]	
			annualizedReturnTot, stdDevTot, sharpeTot, dfDatesGeneral, sharpeTotAdj = tripleMerger( dfDatesBond, dfDatesSPY, dfDatesGold , g, 'AdjCloseBonds' , 'AdjCloseStocks' , 'AdjCloseGold', dateBegin, dateEnd, '1' , 0)
			g.sharpe = sharpeTotAdj
			#print( 'population sharpe : ' + str( g.sharpe ) )

		generation = breeder.getBests( len(generation) * 0.5 , generation )	
		topBest = breeder.getBests( 1, generation )[0]	
		print( "sharpe ration epoch " + str(epoch) + ":  " + str(topBest.sharpe) )
		
	topBest = breeder.getBests( 1, generation )[0]	
	topBest.printStr()

	#gene1 = Gene(0.5,0.25,0.25)
	#annualizedReturnTot, stdDevTot, sharpeTot, dfDatesGeneral = tripleMerger( dfDatesBond, dfDatesSPY, dfDatesGold , gene1, 'AdjCloseBonds' , 'AdjCloseStocks' , 'AdjCloseGold', dateBegin, dateEnd, '1', 0)
	#print( 'standard deviation Total: ' + str(stdDevTot) )
	#print( 'annualized return total: ' + str(annualizedReturnTot) )
	#print( 'Sharpe Total: ' + str( sharpeTot ) )

	#gene2 = Gene(0.25,0.5,0.25)
	#annualizedReturnTot, stdDevTot, sharpeTot, dfDatesGeneral = tripleMerger( dfDatesBond, dfDatesSPY, dfDatesGold , gene2, 'AdjCloseBonds' , 'AdjCloseStocks' , 'AdjCloseGold', dateBegin, dateEnd, '2', 0)
	#print( 'standard deviation Total: ' + str(stdDevTot) )
	#print( 'annualized return total: ' + str(annualizedReturnTot) )
	#print( 'Sharpe Total: ' + str( sharpeTot ) )
	
	#gene3 = Gene(0.25,0.25,0.5)
	#annualizedReturnTot, stdDevTot, sharpeTot, dfDatesGeneral = tripleMerger( dfDatesBond, dfDatesSPY, dfDatesGold , gene3, 'AdjCloseBonds' , 'AdjCloseStocks' , 'AdjCloseGold', dateBegin, dateEnd, '3', 0)
	#print( 'standard deviation Total: ' + str(stdDevTot) )
	#print( 'annualized return total: ' + str(annualizedReturnTot) )
	#print( 'Sharpe Total: ' + str( sharpeTot ) )

	annualizedReturnTot, stdDevTot, sharpeTot, dfDatesGeneral, sharpeTotAdj = tripleMerger( dfDatesBond, dfDatesSPY, dfDatesGold , topBest, 'AdjCloseBonds' , 'AdjCloseStocks' , 'AdjCloseGold', dateBegin, dateEnd, '4', 1)
	print( 'standard deviation Total AI-CREATURE: ' + str(stdDevTot) )
	print( 'annualized return total AI-CREATURE: ' + str(annualizedReturnTot) )
	print( 'Sharpe Total AI-CREATURE: ' + str( sharpeTot ) )
	

	print('\n\n')
	
	plt.show()
	
	
if __name__ == '__main__':
	main()

