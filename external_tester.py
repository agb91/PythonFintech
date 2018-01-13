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

path = "SPY.csv"
dateBegin = '2005-05-01'
dateEnd = '2017-05-01'
	
# correctly read a time series:
dates = pd.date_range( start = dateBegin , end = dateEnd , freq = '1MS' )
dfDates = pd.DataFrame( index = dates )

spy = pd.read_csv(path, index_col='Date', parse_dates=True, na_values=['nan'])
spyDates = dfDates.join(spy)

#print ( spyDates[['AdjClose','Volume']].loc['2016-02-01'] )  #take two columns and a row

#spyDates["maxSince"] = 0.0
#print ( spyDates[['maxSince']] )

#USELESS test of groupby
#maxToday = spyDates.groupby( spyDates.index )['AdjClose'].agg({'maxSince':'max'})
#spyDates["max"] = maxToday
#print( spyDates[["max"]] )

maxSince = 0.0

DDs = []

for index, row in spyDates.iterrows():
	if( row['AdjClose'] > maxSince ):
		maxSince = row['AdjClose']

	DD = ((maxSince - row['AdjClose']) / maxSince ) * 100.0
	if(DD < 0.0 ):
		DD = 0.0	
	#print("index: " + str(index) + ";  DD: " + str( DD ) )
	DDs.append( DD )

spyDates["DDs"] = DDs 	

print( spyDates[["DDs"]].loc[spyDates['DDs'] > 20.0] )








