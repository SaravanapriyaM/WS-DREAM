########################################################
# run_rt.py 
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2014/5/10
# Implemented approach: LACF [Tang et al, ICWS'2012]
# Evaluation metrics: MAE, NMAE, RMSE, MRE, NPRE
########################################################

import numpy as np
import os, sys, time
import multiprocessing
sys.path.append('src')
# Build external model
if not os.path.isfile('src/core.so'):
	print 'Lack of core.so (built from the C++ module).' 
	print 'Please first build the C++ code into core.so by using: '
	print '>> python setup.py build_ext --inplace'
	sys.exit()
from utilities import *
import evaluator
import dataloader
 

#########################################################
# config area
#
para = {'dataType': 'rt', # set the dataType as 'rt' or 'tp'
		'dataPath': '../../data/dataset#1/',
		'outPath': 'result/',
		'metrics': ['MAE', 'NMAE', 'RMSE', 'MRE', 'NPRE'], # delete where appropriate		
		'density': list(np.arange(0.05, 0.31, 0.05)), # matrix density
		'rounds': 20, # how many runs are performed at each matrix density 
        'topK': 10, # the parameter of TopK similar users or services, the default value is
					# topK = 10 as in the reference paper
		'lambda': 0.1, # the combination coefficient of UPCC and IPCC. Although the reference
					   # paper uses lambda = 0.7, we find that lambda = 0.1 performs better 
		'saveTimeInfo': False, # whether to keep track of the running time
		'saveLog': False, # whether to save log into file
		'debugMode': False, # whether to record the debug info
        'parallelMode': True # whether to leverage multiprocessing for speedup
		}

initConfig(para)
#########################################################


startTime = time.clock() # start timing
logger.info('==============================================')
logger.info('Approach: LACF [Tang et al, ICWS\'2012].')

# load the dataset
dataMatrix = dataloader.load(para)
logger.info('Loading data done.')

# get the location groups for users as well as for services
(userGroupByAS, userGroupByCountry, wsGroupByAS, wsGroupByCountry) = \
	dataloader.getLocGroup(para)
locGroup = (userGroupByAS, userGroupByCountry, wsGroupByAS, wsGroupByCountry)
logger.info('Location grouping done.')
     
# run for each density
if para['parallelMode']: # run on multiple processes
    pool = multiprocessing.Pool()
    for density in para['density']:
		pool.apply_async(evaluator.execute, (dataMatrix, locGroup, density, para))
    pool.close()
    pool.join()
else: # run on single processes
	for density in para['density']:
		evaluator.execute(dataMatrix, locGroup, density, para)

logger.info(time.strftime('All done. Total running time: %d-th day - %Hhour - %Mmin - %Ssec.',
         time.gmtime(time.clock() - startTime)))
logger.info('==============================================')
sys.path.remove('src')



