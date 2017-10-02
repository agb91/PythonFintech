import pandas as pd  
import requests
import os
import numpy as np
import csv
import matplotlib.pyplot as plt  
from sklearn import preprocessing

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

def tripleMerger( first, second, third , k1, k2, k3, n1, n2, n3, dateBegin, dateEnd, it ):
	dfDatesGeneral = first.join( second )
	dfDatesGeneral = dfDatesGeneral.join( third )
	kBond = 2
	kStock = 1
	kGold = 1
	totalSum = dfDatesGeneral.loc[: , n1] * k1 + dfDatesGeneral.loc[: , n2] * k2 + dfDatesGeneral.loc[: , n3] * k3
	dfDatesGeneral['total' + str(it)] = totalSum / (k1 + k2 + k3) #beacuse it is an average in my opinion
	stdDevTot = getStdDev(dfDatesGeneral['total' + str(it)])
	annualizedReturnTot = getAnnualizedReturn( dateBegin, dateEnd, 'total' + str(it), dfDatesGeneral )
	sharpeTot = annualizedReturnTot / stdDevTot
	dfDatesGeneral.plot()
	return annualizedReturnTot, stdDevTot, sharpeTot, dfDatesGeneral

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
	print( '##########################  TOTAL  ##########################' )
	annualizedReturnTot, stdDevTot, sharpeTot, dfDatesGeneral = tripleMerger( dfDatesBond, dfDatesSPY, dfDatesGold , 0.5, 0.25, 0.25, 'AdjCloseBonds' , 'AdjCloseStocks' , 'AdjCloseGold', dateBegin, dateEnd, '1')
	#print( 'standard deviation Total: ' + str(stdDevTot) )
	#print( 'annualized return total: ' + str(annualizedReturnTot) )
	print( 'Sharpe Total: ' + str( sharpeTot ) )
	annualizedReturnTot, stdDevTot, sharpeTot, dfDatesGeneral = tripleMerger( dfDatesBond, dfDatesSPY, dfDatesGold , 0.25, 0.5, 0.25, 'AdjCloseBonds' , 'AdjCloseStocks' , 'AdjCloseGold', dateBegin, dateEnd, '2')
	#print( 'standard deviation Total: ' + str(stdDevTot) )
	#print( 'annualized return total: ' + str(annualizedReturnTot) )
	print( 'Sharpe Total: ' + str( sharpeTot ) )
	annualizedReturnTot, stdDevTot, sharpeTot, dfDatesGeneral = tripleMerger( dfDatesBond, dfDatesSPY, dfDatesGold , 0.25, 0.25, 0.5, 'AdjCloseBonds' , 'AdjCloseStocks' , 'AdjCloseGold', dateBegin, dateEnd, '3')
	#print( 'standard deviation Total: ' + str(stdDevTot) )
	#print( 'annualized return total: ' + str(annualizedReturnTot) )
	print( 'Sharpe Total: ' + str( sharpeTot ) )
	

	print('\n\n')
	
	plt.show()
	
	
if __name__ == '__main__':
	main()

