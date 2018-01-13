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


def date_difference_years( date_begin , date_end ):
	year_begin = date_begin.split('-')[0]
	year_end = date_end.split('-')[0]
	return int( int(year_end) - int(year_begin) )

def get_std_dev( column ):
	return np.std(column)	

#already normalized at 100...
def get_annualized_return( date_begin, date_end, colname, column, tax, commissions  ):
	begin_value = column.loc[date_begin , colname]
	end_value = column.loc[date_end , colname]
	#let's consided taxes and brokerage commissions

	gross = (( end_value - begin_value ) / begin_value) * 100
	gross = gross / date_difference_years(date_begin , date_end)
	#print(" GROSS :   " + str(gross)  )
	#print( "tax: " + str(tax) + " comms : " + str(commissions) )
	net = ( gross * ( 1.0 - float(tax) ) ) - float(commissions)
	#print( "NET : " + str(net) )
	return (net )

def analyze_data( path , date_range, date_begin, date_end, close_columname, tax ):
	df_ob = pd.read_csv(path, index_col='Date', parse_dates=True, na_values=['nan'])
	df_dates_ob = date_range.join(df_ob)
	#the following line normalizes the values
	df_dates_ob = df_dates_ob[['AdjClose']] * ( 100 / df_dates_ob.loc[date_begin , 'AdjClose'])
	df_dates_ob.columns = [close_columname]
	std_dev_ob = get_std_dev(df_dates_ob[close_columname])
	annualized_return_ob = get_annualized_return( date_begin, date_end, close_columname, df_dates_ob , float(tax) , float(1.0) )
	sharpe_ob = annualized_return_ob / std_dev_ob
	return annualized_return_ob, std_dev_ob , sharpe_ob, df_dates_ob

def addDD( df, col_total_name ):
	max_since = 0.0
	DDs = []
	for index, row in df.iterrows():
		if( row[col_total_name] > max_since ):
			max_since = row[col_total_name]
		DD = ((max_since - row[col_total_name]) / max_since ) * 100.0
		if(DD < 0.0 ):
			DD = 0.0	
		DDs.append( DD )
	df[ "DDs" ] = DDs 
	return df

#at the moment it works with 3 etfs.. so triple.. we'll modify this point
def triple_merger( first, second, third , gene, n1, n2, n3, date_begin, date_end, it , to_plot ):
	#I use sometimes it parameters in debugging, so I maintain it even if at the moment is
	#useless
	
	df_dates_general = first.join( second )
	df_dates_general = df_dates_general.join( third )
	total_sum = df_dates_general.loc[: , n1] * gene.w1 + df_dates_general.loc[: , n2] * gene.w2 + df_dates_general.loc[: , n3] * gene.w3
	df_dates_general['Portfolio' + str(it)] = total_sum 
	df_dates_general = addDD(df_dates_general , 'Portfolio' + str(it) )
	std_dev_tot = get_std_dev(df_dates_general['Portfolio' + str(it)])
	
	#referred to the Italian tax level (different for bonds and 'all the rest')
	weighted_taxes = (0.125 * gene.w1) + 0.25 * (gene.w2 + gene.w3)
	annualized_return_tot = get_annualized_return( date_begin, date_end, 'Portfolio' + str(it), df_dates_general, weighted_taxes, 1.0 )
	sharpe_tot = annualized_return_tot / std_dev_tot 

	#this is a formula created by me, surely something better exists
	sharpe_tot_adj = sharpe_tot - ( df_dates_general["DDs"].max() / 300.0 ) 
	
	if(to_plot == 1):
		df_dates_to_print = pd.DataFrame()
		df_dates_to_print[['Portfolio', 'Worst Drowdown']] = df_dates_general[['Portfolio4', 'DDs']]
		#I print only the minimum amount of data for the moment
		#df_dates_to_print = df_dates_to_print.ix[:, ['total4', 'DDs']]
		#print( df_dates_to_print )
		df_dates_to_print.plot()
	return annualized_return_tot, std_dev_tot, sharpe_tot, df_dates_general , sharpe_tot_adj

def main():
	#set date range
	date_begin = '2005-05-01'
	date_end = '2017-05-01'
	years_length = date_difference_years( date_begin , date_end )
	print( 'we are reasoning on a span of: ' + str( years_length ) + ' years ' )

	dates = pd.date_range( start = date_begin , end = date_end , freq = '1MS' )
	df_dates = pd.DataFrame( index = dates )

	print ('-------------------------- ANALYSIS PART ---------------------------')
	print('Simply evaluates some features of some stand-alone ETFs')
	#read about bonds
	print( '##########################  BONDS  ##########################' )
	annualized_return_bond, std_dev_bond, sharpe_bond, df_dates_bond = analyze_data( 'BOND.csv', df_dates, date_begin, date_end, 'AdjClose_bonds' , 0.125 )
	print( 'standard deviation Bonds: ' + str(std_dev_bond) )
	print ( 'annualized return Bonds: ' + str( annualized_return_bond ))
	print ( 'Sharpe Bonds: ' + str( sharpe_bond ))
	print( '\n\n' )

	print( '##########################  STOCKS  ##########################' )
	annualized_return_SPY, std_dev_SPY, sharpe_SPY, df_dates_SPY = analyze_data( 'SPY.csv', df_dates, date_begin, date_end, 'AdjCloseStocks' , 0.25 )
	print( 'standard deviation Stocks: ' + str(std_dev_SPY) )
	print ( 'annualized return Stocks: ' + str( annualized_return_SPY ))
	print ( 'Sharpe Stocks: ' + str( sharpe_SPY ))
	print('\n\n')

	print( '##########################  GOLD  ##########################' )
	annualized_return_gold, std_dev_gold, sharpe_gold, df_dates_gold = analyze_data( 'GLD.csv', df_dates, date_begin, date_end, 'AdjClose_gold', 0.25 )
	print( 'standard deviation Gold: ' + str(std_dev_gold) )
	print ( 'annualized return Gold: ' + str( annualized_return_gold ))
	print ( 'Sharpe Gold: ' + str( sharpe_gold ))
	print('\n\n')
	
	
	print ('\n\n\n-------------------------- AI PART ---------------------------\n\n\n')
	

	print( '##########################  TOTAL  ##########################\n' )
	print( 'run a genetic algorithm in order to buld a diversified portfolio' )
	epochs = 30
	population = 20
	breeder = Breeder()



	generation = breeder.create( population )

	for epoch in range( 0 , epochs ):

		generation = breeder.populate( generation , population )	
		for i in range( 0, len(generation) ):
			#generation[i].printStr()
			g = generation[i]	
			annualized_return_tot, std_dev_tot, sharpe_tot, df_dates_general, sharpe_tot_adj = triple_merger( df_dates_bond, df_dates_SPY, df_dates_gold , g, 'AdjClose_bonds' , 'AdjCloseStocks' , 'AdjClose_gold', date_begin, date_end, '1' , 0)
			g.sharpe = sharpe_tot_adj
			#print( 'population sharpe : ' + str( g.sharpe ) )

		generation = breeder.get_bests( len(generation) * 0.5 , generation )	
		topBest = breeder.get_bests( 1, generation )[0]	
		print( "sharpe ration epoch " + str(epoch) + ":  " + str(topBest.sharpe) )
		
	topBest = breeder.get_bests( 1, generation )[0]	
	topBest.printStr()

	#just to take some experiment..
	#gene1 = Gene(0.5,0.25,0.25)
	#annualized_return_tot, std_dev_tot, sharpe_tot, df_dates_general = triple_merger( df_dates_bond, df_dates_SPY, df_dates_gold , gene1, 'AdjClose_bonds' , 'AdjCloseStocks' , 'AdjClose_gold', date_begin, date_end, '1', 0)
	#print( 'standard deviation Total: ' + str(std_dev_tot) )
	#print( 'annualized return total: ' + str(annualized_return_tot) )
	#print( 'Sharpe Total: ' + str( sharpe_tot ) )

	#gene2 = Gene(0.25,0.5,0.25)
	#annualized_return_tot, std_dev_tot, sharpe_tot, df_dates_general = triple_merger( df_dates_bond, df_dates_SPY, df_dates_gold , gene2, 'AdjClose_bonds' , 'AdjCloseStocks' , 'AdjClose_gold', date_begin, date_end, '2', 0)
	#print( 'standard deviation Total: ' + str(std_dev_tot) )
	#print( 'annualized return total: ' + str(annualized_return_tot) )
	#print( 'Sharpe Total: ' + str( sharpe_tot ) )
	
	#gene3 = Gene(0.25,0.25,0.5)
	#annualized_return_tot, std_dev_tot, sharpe_tot, df_dates_general = triple_merger( df_dates_bond, df_dates_SPY, df_dates_gold , gene3, 'AdjClose_bonds' , 'AdjCloseStocks' , 'AdjClose_gold', date_begin, date_end, '3', 0)
	#print( 'standard deviation Total: ' + str(std_dev_tot) )
	#print( 'annualized return total: ' + str(annualized_return_tot) )
	#print( 'Sharpe Total: ' + str( sharpe_tot ) )

	annualized_return_tot, std_dev_tot, sharpe_tot, df_dates_general, sharpe_tot_adj = triple_merger( df_dates_bond, df_dates_SPY, df_dates_gold , topBest, 'AdjClose_bonds' , 'AdjCloseStocks' , 'AdjClose_gold', date_begin, date_end, '4', 1)
	print( 'standard deviation Total AI-CREATURE: ' + str(std_dev_tot) )
	print( 'annualized return total AI-CREATURE: ' + str(annualized_return_tot) )
	print( 'Sharpe Total AI-CREATURE: ' + str( sharpe_tot ) )
	
	print('\n\n')
	
	plt.show()
	
	
if __name__ == '__main__':
	main()

