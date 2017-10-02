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
	dateBegin = '2003-11-01'
	dateEnd = '2017-05-01'
	yearsLength = dateDifferenceYears( dateBegin , dateEnd )
	print( 'we are reasoning on a span of: ' + str( yearsLength ) + ' years ' )

	dates = pd.date_range( start = dateBegin , end = dateEnd , freq = '1MS' )
	dfDates = pd.DataFrame( index = dates )

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
	dfBondMilan = pd.read_csv('BONDMilano.csv', index_col='Date', parse_dates=True, na_values=['nan'])
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


	print( '##########################  TOTAL  ##########################' )
	dfDatesGeneral = dfDatesBond.join( dfDatesBondMilan )

	
	dfDatesGeneral.plot()
	plt.show()
	
	
if __name__ == '__main__':
	main()

