import pandas as pd  
import requests
import os
import numpy as np
import csv
import matplotlib.pyplot as plt  
from sklearn import preprocessing
from functools import reduce


dateBegin = '1993-01-01'
dateEnd = '2017-05-01'


def evalueInvest( periods, data ):
	
	perc_gain_list = np.array( list() )
	perc_gain_list = np.append( 0, perc_gain_list )	

	for k in range( 1, periods ):

		np_data = np.array(data)
		sell_value = np_data[ (k) ]
		gain_list = np.array( list() )
		passed_periods = 0
		for i in range( 0, k ):
			passed_periods += 1
			buy_value = np_data[i]
			gain = sell_value - buy_value
			gain_list = np.append( gain_list, gain )

		tot_gain = reduce((lambda x, y: x + y), gain_list)
		tot_invested = 100 * passed_periods
		perc_gain = 100 + (tot_gain / tot_invested) * 100
		#print( "gain until now: " + str(tot_gain) +
		#	";  invested until now: " + str(tot_invested) +
		#	";  perc gain = " + str(perc_gain) )
		perc_gain_list = np.append( perc_gain_list, perc_gain )
	
	return perc_gain_list	

def main():

	dates = pd.date_range( start = dateBegin , end = dateEnd , freq = '1MS' )
	dfDates = pd.DataFrame( index = dates )

	print( '##########################  Read Spy Data  ##########################' )
	dfSpy = pd.read_csv('../SPY.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	dfDatesSpy = dfDates.join(dfSpy)
	#the following line normalizes the values
	dfDatesSpy = dfDatesSpy[['AdjClose']] * ( 100 / dfDatesSpy.loc[dateBegin , 'AdjClose'])
	periods = len(dfDatesSpy['AdjClose'])
	new_col = evalueInvest( periods, dfDatesSpy['AdjClose'] )
	new_col = pd.Series( new_col, index=dfDatesSpy.index)
	#print( "new col length = " + str( len(new_col) ) + "; periods:  " + str(periods) )
	dfDatesSpy['PacGainSpys'] = new_col
	#print( dfDatesSpy )
	
	
	#dfDatesSpy.columns = [['AdjCloseSpys', 'PacGainSpys']]
	#print( "pac payments: " + str(periods) )
	#print( dfDatesSpy['AdjCloseSpys'] )

	dfDatesSpy.plot()
	plt.show()

if __name__ == '__main__':
	main()	