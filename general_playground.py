import numpy as np
import tensorflow as tf
from functools import reduce
from testClass import TestClass

test_list = list(["a","g"])


print( "a list initialized with list(): " + str(test_list) )
print( "a list initialized with list() type: " + str(type(test_list)) )  

#append
b = np.array( list() )
b = np.append( b, "a" )

test_object = TestClass( 3 )

a = [["a","b","c", float(2.23) ],
	[test_object , "i", "t", "e", ]]
npa = np.array( a )



print( "list: " + str( a ) )
print( "npa: " + str( npa ) )

print( type(a) )
print( type( npa ) )

print( "dimensions: " + str(npa.ndim) )
print( "shape: " + str(npa.shape) )
print( "size: " + str(npa.size) )
print( "dtype: " + str(npa.dtype.name) )

print( "position r0: " + str( a[0] ) )
print( "position r0-c3: " + str( a[0][3] ) )
print( "position r0-c1-2: " + str( a[0][1:3] ) )

b = np.reshape(a, (1,8)) 

print( "b = reshape a one row long 8: " + str( b ) )

c = np.array( [1,2,3] )
scale = lambda x: (x + x + x)
print( "lambda triple concatenate content on [1,2,3]: " + str( scale(c) ) )

dict_1 = { "a" : "hello", "b" : "world" }

print( "all dictionary: " + str(dict_1) )

print( "'b' element: " + str( dict_1["b"] ) )

print(" \n ######### SET SORT WITH ARRAY #########")
a = [513 , 213, 322,11,1234 , 11 , 213 , 11] 
a = sorted( a )
reva = sorted( a, reverse = True )

print( "sorted a: " + str( a ) + "; type: " + str( type( a ) ) )
print( "reverse-sorted a: " + str( reva )  + "; type: " + str( type( a ) ) )

a = sorted( set( a ) )

print( "sorted SET a: " + str( a ) )

print(" \n ######### SET SORT WITH NP-ARRAY #########")

a = np.array([513 , 213, 322,11,1234 , 11 , 213 , 11]) 
a = np.sort( a )
reva = -np.sort( -a )

print( "sorted a: " + str( a ) + "; type: " + str( type( a ) ) )
print( "reverse-sorted a: " + str( reva )  + "; type: " + str( type( a ) ) )


print( "\n ############### START WORK WITH TENSORFLOW ##############" )

matrix1 = tf.constant([[3., 2.],[1., 7.]])

matrix2 = tf.constant([[9., 4.],[2., 3.]])

data = [[1,2,3],[4,5,6]]
data_np = np.asarray( data )

data_tf = tf.convert_to_tensor(data_np)

with tf.Session() as sess:
	with tf.device("/gpu:0"):
		result = tf.matmul(matrix1, matrix2)
		print ( result )
		print( data_tf )

print( "############## APPLY METHOD ON ARRAYS ##############" )

print( "first way: map" )
a = [1,2,5,8,3,4,9,44,3]
npa = np.array( a )

def add1( x ):
	if( x < 3 ):
		return ( x + 100 )
	else:
		return 0	

result = list( map ( add1, a ) )
resultnp = np.array( list( map ( add1, npa ) ) )

print( "plain: " + str( result ) )			
print( "np array: " + str( resultnp ) )

print( "second way: map + lambda" )
a = [1,2,5,8,3,4,9,44,3]
npa = np.array( a )

def add1( x ):
	if( x < 3 ):
		return ( x + 100 )
	else:
		return 0	

result = list( map ( lambda x: add1(x), a ) )
resultnp = np.array( list( map ( lambda x: add1(x), npa ) ) )

print( "plain: " + str( result ) )			
print( "np array: " + str( resultnp ) )

print( "array filter" )

a = [1,-2,-5,8,3,4,-9,44,-3]
npa = np.array( a )

result = list( filter( lambda x: x < 0, a ) )
resultnp = np.array( list( filter( lambda x: x < 0, npa ) ) )

print( "plain: " + str( result ) )			
print( "np array: " + str( resultnp ) )

print( "array reduce: " )

a = [1,-2,-5,8,3,4,-9,44,-3]
npa = np.array( a )

result = reduce((lambda x, y: x + y), a)
resultnp = np.array( reduce((lambda x, y: x + y), npa) )

print( "plain: " + str( result ) )			
print( "np array: " + str( resultnp ) )

print( "############## LIST COMPREHENSION ############### " )

a = [x**2 for x in range(0,10)]
print (a)

odd = [x for x in range(1,20) if x%2==0 ]
print( odd )

vowels = [x for x in 'Hello World' if x in ['a','e','i','o','u']]
print( vowels )

a = [1,2,3,4,5]
npa = np.array( a )
print( 2 in a )
print( 2 in npa )

matrix = np.array([ range (1,6), range( -2,4),range (10,12) ])
print( str(matrix) )

flatten = [x for row in matrix for x in row ]

print (flatten)

print ("finished")




