
#read READ CSV TO SCRR_TRAINING & SCRR_TEST

#treining = pd.read_csv('../training.csv')	#examples
#test = pd.read_csv('../test.csv')			#examples

import numpy as np
import pandas as pd 
import verde as vd

def grafita_reduce(training_csv,test_csv,n_iterations=1,*different_spacing=false,*spacing_range=[500]):
    """
    (get a better description)
    Grafita info: Receive data an replies (number of iterations) at differents filtred parameters    

     Parameters
        ----------
        training_csv : pdlist
        test_csv : pdlist
        n_iterations : int
        *different_spacing : boolean

        Returns
        -------
        description : type
        	what does..
    """
    #CREATE THC/KC & KC/CTC
    training_csv['THC/KC'] = training_csv['THC']/training_csv['KC']
    test_csv['KC/CTC'] = test_csv['KC']/test_csv['CTC']

    training_csv.drop('Unnamed: 0', axis='columns', inplace=True) #getting rid of unnamed columns, do it before loading to this function, and save to csv.

    list_training=copy.deepcopy()#create a list of same data, to generate (do filter just for needed features)

	vd.BlockReduce(np.median, spacing=spacing_range) #ATRIBUTE VARIABLE BEHAVIOR AT spacing=500

###CONSTRUTIVE THOUGHTS FOR THIS FUNCTION:
	#try to compare each training process before it's complete 
	#if this is possible, compute remaining process and return a range value of best results
	#probably is best creat a new scope, or build it's own class to manage many functionalities. 
	
	pass
