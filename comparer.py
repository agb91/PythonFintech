import pandas as pd  
import requests
import os
import numpy as np
import csv
import matplotlib.pyplot as plt  
from sklearn import preprocessing

def date_difference_years( date_begin , date_end ):
	year_begin = date_begin.split('-')[0]
	year_end = date_end.split('-')[0]
	return int( int(year_end) - int(year_begin) )

def get_std_dev( column ):
	return np.std(column)	

def get_annualized_return( date_begin, date_end, colname, column ):
	begin_value = column.loc[date_begin , colname]
	end_value = column.loc[date_end , colname]
	return (( end_value - begin_value ) / date_difference_years(date_begin , date_end))

def main():
	#set date range
	date_begin = '2004-11-01'
	date_end = '2017-05-01'
	years_length = date_difference_years( date_begin , date_end )
	print( 'we are reasoning on a span of: ' + str( years_length ) + ' years ' )

	dates = pd.date_range( start = date_begin , end = date_end , freq = '1MS' )
	df_dates = pd.DataFrame( index = dates )
	'''
	print( '##########################  FIRST  ##########################' )
	dfBond = pd.read_csv('BOND.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	df_datesBond = df_dates.join(dfBond)
	#the following line normalizes the values
	df_datesBond = df_datesBond[['AdjClose']] * ( 100 / df_datesBond.loc[date_begin , 'AdjClose'])
	df_datesBond.columns = ['AdjCloseBonds']
	std_devBond = get_std_dev(df_datesBond['AdjCloseBonds'])
	annualized_returnBond = get_annualized_return( date_begin, date_end, 'AdjCloseBonds', df_datesBond )
	print( 'standard deviation Bonds: ' + str(std_devBond) )
	print ( 'annualized return Bonds: ' + str( annualized_returnBond ))
	sharpeBond = annualized_returnBond / std_devBond
	print ( 'Sharpe Bonds: ' + str( sharpeBond ))
	print( '\n\n' )
	
	print( '##########################  SECOND  ##########################' )
	dfBondMilan = pd.read_csv('XBAEMI.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	df_datesBondMilan = df_dates.join(dfBondMilan)
	#the following line normalizes the values
	df_datesBondMilan = df_datesBondMilan[['AdjClose']] * ( 100 / df_datesBondMilan.loc[date_begin , 'AdjClose'])
	df_datesBondMilan.columns = ['AdjCloseBondsMilan']
	std_devBondMilan = get_std_dev(df_datesBondMilan['AdjCloseBondsMilan'])
	annualized_returnBondMilan = get_annualized_return( date_begin, date_end, 'AdjCloseBondsMilan', df_datesBondMilan )
	print( 'standard deviation Bonds Milan: ' + str( std_devBondMilan ) )
	print ( 'annualized return Bonds Milan: ' + str( annualized_returnBondMilan ))
	sharpeBondMilan = annualized_returnBondMilan / std_devBondMilan
	print ( 'Sharpe Bonds Milan: ' + str( sharpeBondMilan ))
	print( '\n\n' )
	
	
	df_gold = pd.read_csv('GLD.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	df_dates_gold = df_dates.join(df_gold)
	#the following line normalizes the values
	df_dates_gold = df_dates_gold[['AdjClose']] * ( 100 / df_dates_gold.loc[date_begin , 'AdjClose'])
	df_dates_gold.columns = ['AdjCloseGold']
	std_dev_gold = get_std_dev(df_dates_gold['AdjCloseGold'])
	annualized_return_gold = get_annualized_return( date_begin, date_end, 'AdjCloseGold', df_dates_gold )
	print( 'standard deviation Gold: ' + str(std_dev_gold) )
	print ( 'annualized return Gold: ' + str( annualized_return_gold ))
	sharpe_gold = annualized_return_gold / std_dev_gold
	print ( 'Sharpe Gold: ' + str( sharpe_gold ))
	print( '\n\n' )

	
	dfCmd = pd.read_csv('CMD.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	df_datesCmd = df_dates.join(dfCmd)
	#the following line normalizes the values
	df_datesCmd = df_datesCmd[['AdjClose']] * ( 100 / df_datesCmd.loc[date_begin , 'AdjClose'])
	df_datesCmd.columns = ['AdjCloseCmd']
	std_devCmd = get_std_dev(df_datesCmd['AdjCloseCmd'])
	annualized_returnCmd = get_annualized_return( date_begin, date_end, 'AdjCloseCmd', df_datesCmd )
	print( 'standard deviation Commodities: ' + str( std_devCmd ) )
	print ( 'annualized return Commodities: ' + str( annualized_returnCmd ))
	sharpeCmd = annualized_returnCmd / std_devCmd
	print ( 'Sharpe Commodities: ' + str( sharpeCmd ))
	print( '\n\n' )
	
	'''

	df_spy = pd.read_csv('SPY.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	df_dates_spy = df_dates.join(df_spy)
	#the following line normalizes the values
	df_dates_spy = df_dates_spy[['AdjClose']] * ( 100 / df_dates_spy.loc[date_begin , 'AdjClose'])
	df_dates_spy.columns = ['AdjCloseSpy']
	#print( df_dates_spy.head() )
	std_dev_spy = get_std_dev(df_dates_spy['AdjCloseSpy'])
	annualized_return_spy = get_annualized_return( date_begin, date_end, 'AdjCloseSpy', df_dates_spy )
	print( 'standard deviation SPY: ' + str( std_dev_spy ) )
	print ( 'annualized return SPY: ' + str( annualized_return_spy ))
	sharpe_spy = annualized_return_spy / std_dev_spy
	print ( 'Sharpe SPY: ' + str( sharpe_spy ))
	print( '\n\n' )

	df_gold = pd.read_csv('GLD.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	df_dates_gold = df_dates.join(df_gold)
	#the following line normalizes the values
	total_sum = df_dates_gold.loc[: , 'AdjClose'] + df_dates_spy.loc[: , 'AdjCloseSpy']
	df_dates_gold[['AdjClose']] = total_sum
	

	df_dates_gold = df_dates_gold[['AdjClose']] * ( 100 / df_dates_gold.loc[date_begin , 'AdjClose'])
	
	df_dates_gold.columns = ['AdjCloseGoldSpy']
	std_dev_gold = get_std_dev(df_dates_gold['AdjCloseGoldSpy'])
	annualized_return_gold = get_annualized_return( date_begin, date_end, 'AdjCloseGoldSpy', df_dates_gold )
	print( 'standard deviation Gold+SPY: ' + str(std_dev_gold) )
	print ( 'annualized return Gold+SPY: ' + str( annualized_return_gold ))
	sharpe_gold = annualized_return_gold / std_dev_gold
	print ( 'Sharpe Gold+SPY: ' + str( sharpe_gold ))
	print( '\n\n' )

	'''
	df_ACWI = pd.read_csv('ACWI.csv', index_col='Date', 
		parse_dates=['Date'], na_values=['nan'])
	df_dates_ACWI = df_dates.join(df_ACWI)
	#the following line normalizes the values
	df_dates_ACWI = df_dates_ACWI[['Value']] * ( 100 / df_dates_ACWI.loc[date_begin , 'Value'])
	df_dates_ACWI.columns = ['AdjCloseACWI']
	#print( df_dates_ACWI.head() )
	std_devACWI = get_std_dev(df_dates_ACWI['AdjCloseACWI'])
	annualized_returnACWI = get_annualized_return( date_begin, date_end, 'AdjCloseACWI', df_dates_ACWI )
	print( 'standard deviation ACWI: ' + str( std_devACWI ) )
	print ( 'annualized return ACWI: ' + str( annualized_returnACWI ))
	sharpeACWI = annualized_returnACWI / std_devACWI
	print ( 'Sharpe ACWI: ' + str( sharpeACWI ))
	print( '\n\n' )
	'''

	'''
	dfACWI_value = pd.read_csv('ACWI-value.csv', index_col='Date', 
		parse_dates=['Date'], na_values=['nan'])
	df_dates_ACWI_value = df_dates.join(dfACWI_value)
	#the following line normalizes the values
	df_dates_ACWI_value = df_dates_ACWI_value[['Value']] * ( 100 / df_dates_ACWI_value.loc[date_begin , 'Value'])
	df_dates_ACWI_value.columns = ['AdjCloseACWI-value']
	std_devACWI_value = get_std_dev(df_dates_ACWI_value['AdjCloseACWI-value'])
	annualized_returnACWI_value = get_annualized_return( date_begin, date_end, 'AdjCloseACWI-value', df_dates_ACWI_value )
	print( 'standard deviation ACWI-value: ' + str( std_devACWI_value ) )
	print ( 'annualized return ACWI-value: ' + str( annualized_returnACWI_value ))
	sharpeACWI_value = annualized_returnACWI_value / std_devACWI_value
	print ( 'Sharpe ACWI-value: ' + str( sharpeACWI_value ))
	print( '\n\n' )

	
	dfBrk = pd.read_csv('BRK-B.csv', index_col='Date', parse_dates=True, na_values=['nan'])
	df_datesBrk = df_dates.join(dfBrk)
	#the following line normalizes the values
	df_datesBrk = df_datesBrk[['AdjClose']] * ( 100 / df_datesBrk.loc[date_begin , 'AdjClose'])
	df_datesBrk.columns = ['AdjCloseBrk']
	std_devBrk = get_std_dev(df_datesBrk['AdjCloseBrk'])
	annualized_returnBrk = get_annualized_return( date_begin, date_end, 'AdjCloseBrk', df_datesBrk )
	print( 'standard deviation BRK: ' + str( std_devBrk ) )
	print ( 'annualized return BRK: ' + str( annualized_returnBrk ))
	sharpeBrk = annualized_returnBrk / std_devBrk
	print ( 'Sharpe BRK: ' + str( sharpeBrk ))
	print( '\n\n' )
	'''

	print( '##########################  TOTAL  ##########################' )
	df_dates_general = df_dates.join( df_dates_gold )
	df_dates_general = df_dates_general.join( df_dates_spy )
	

	
	df_dates_general.plot()
	plt.show()
	
	
if __name__ == '__main__':
	main()

