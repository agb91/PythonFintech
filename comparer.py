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

def main():
	#set date range
	dateBegin = '2006-05-01'
	dateEnd = '2017-05-01'
	yearsLength = dateDifferenceYears( dateBegin , dateEnd )
	print( 'we are reasoning on a span of: ' + str( yearsLength ) + ' years ' )

	dates = pd.date_range( start = dateBegin , end = dateEnd , freq = '1MS' )
	dfDates = pd.DataFrame( index = dates )
	'''
	print( '##########################  FIRST  ##########################' )
	dfBond = pd.read_csv('BOND.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	dfDatesBond = dfDates.join(dfBond)
	#the following line normalizes the values
	dfDatesBond = dfDatesBond[['AdjClose']] * ( 100 / dfDatesBond.loc[dateBegin , 'AdjClose'])
	dfDatesBond.columns = ['AdjCloseBonds']
	stdDevBond = getStdDev(dfDatesBond['AdjCloseBonds'])
	annualizedReturnBond = getAnnualizedReturn( dateBegin, dateEnd, 'AdjCloseBonds', dfDatesBond )
	print( 'standard deviation Bonds: ' + str(stdDevBond) )
	print ( 'annualized return Bonds: ' + str( annualizedReturnBond ))
	sharpeBond = annualizedReturnBond / stdDevBond
	print ( 'Sharpe Bonds: ' + str( sharpeBond ))
	print( '\n\n' )
	
	print( '##########################  SECOND  ##########################' )
	dfBondMilan = pd.read_csv('XBAEMI.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	dfDatesBondMilan = dfDates.join(dfBondMilan)
	#the following line normalizes the values
	dfDatesBondMilan = dfDatesBondMilan[['AdjClose']] * ( 100 / dfDatesBondMilan.loc[dateBegin , 'AdjClose'])
	dfDatesBondMilan.columns = ['AdjCloseBondsMilan']
	stdDevBondMilan = getStdDev(dfDatesBondMilan['AdjCloseBondsMilan'])
	annualizedReturnBondMilan = getAnnualizedReturn( dateBegin, dateEnd, 'AdjCloseBondsMilan', dfDatesBondMilan )
	print( 'standard deviation Bonds Milan: ' + str( stdDevBondMilan ) )
	print ( 'annualized return Bonds Milan: ' + str( annualizedReturnBondMilan ))
	sharpeBondMilan = annualizedReturnBondMilan / stdDevBondMilan
	print ( 'Sharpe Bonds Milan: ' + str( sharpeBondMilan ))
	print( '\n\n' )
	
	
	dfGold = pd.read_csv('GLD.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	dfDatesGold = dfDates.join(dfGold)
	#the following line normalizes the values
	dfDatesGold = dfDatesGold[['AdjClose']] * ( 100 / dfDatesGold.loc[dateBegin , 'AdjClose'])
	dfDatesGold.columns = ['AdjCloseGold']
	stdDevGold = getStdDev(dfDatesGold['AdjCloseGold'])
	annualizedReturnGold = getAnnualizedReturn( dateBegin, dateEnd, 'AdjCloseGold', dfDatesGold )
	print( 'standard deviation Gold: ' + str(stdDevGold) )
	print ( 'annualized return Gold: ' + str( annualizedReturnGold ))
	sharpeGold = annualizedReturnGold / stdDevGold
	print ( 'Sharpe Gold: ' + str( sharpeGold ))
	print( '\n\n' )


	dfCmd = pd.read_csv('CMD.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	dfDatesCmd = dfDates.join(dfCmd)
	#the following line normalizes the values
	dfDatesCmd = dfDatesCmd[['AdjClose']] * ( 100 / dfDatesCmd.loc[dateBegin , 'AdjClose'])
	dfDatesCmd.columns = ['AdjCloseCmd']
	stdDevCmd = getStdDev(dfDatesCmd['AdjCloseCmd'])
	annualizedReturnCmd = getAnnualizedReturn( dateBegin, dateEnd, 'AdjCloseCmd', dfDatesCmd )
	print( 'standard deviation Commodities: ' + str( stdDevCmd ) )
	print ( 'annualized return Commodities: ' + str( annualizedReturnCmd ))
	sharpeCmd = annualizedReturnCmd / stdDevCmd
	print ( 'Sharpe Commodities: ' + str( sharpeCmd ))
	print( '\n\n' )
	
	'''

	dfSpy = pd.read_csv('SPY.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	dfDatesSpy = dfDates.join(dfSpy)
	#the following line normalizes the values
	dfDatesSpy = dfDatesSpy[['AdjClose']] * ( 100 / dfDatesSpy.loc[dateBegin , 'AdjClose'])
	dfDatesSpy.columns = ['AdjCloseSpy']
	stdDevSpy = getStdDev(dfDatesSpy['AdjCloseSpy'])
	annualizedReturnSpy = getAnnualizedReturn( dateBegin, dateEnd, 'AdjCloseSpy', dfDatesSpy )
	print( 'standard deviation SPY: ' + str( stdDevSpy ) )
	print ( 'annualized return SPY: ' + str( annualizedReturnSpy ))
	sharpeSpy = annualizedReturnSpy / stdDevSpy
	print ( 'Sharpe SPY: ' + str( sharpeSpy ))
	print( '\n\n' )

	dfBrk = pd.read_csv('BRK-B.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	dfDatesBrk = dfDates.join(dfBrk)
	#the following line normalizes the values
	dfDatesBrk = dfDatesBrk[['AdjClose']] * ( 100 / dfDatesBrk.loc[dateBegin , 'AdjClose'])
	dfDatesBrk.columns = ['AdjCloseBrk']
	stdDevBrk = getStdDev(dfDatesBrk['AdjCloseBrk'])
	annualizedReturnBrk = getAnnualizedReturn( dateBegin, dateEnd, 'AdjCloseBrk', dfDatesBrk )
	print( 'standard deviation BRK: ' + str( stdDevBrk ) )
	print ( 'annualized return BRK: ' + str( annualizedReturnBrk ))
	sharpeBrk = annualizedReturnBrk / stdDevBrk
	print ( 'Sharpe BRK: ' + str( sharpeBrk ))
	print( '\n\n' )
	

	print( '##########################  TOTAL  ##########################' )
	dfDatesGeneral = dfDates.join( dfDatesBrk )
	dfDatesGeneral = dfDatesGeneral.join( dfDatesSpy )


	
	dfDatesGeneral.plot()
	plt.show()
	
	
if __name__ == '__main__':
	main()

