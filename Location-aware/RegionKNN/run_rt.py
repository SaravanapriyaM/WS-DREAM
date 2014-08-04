########################################################
# run_rt.py 
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2014/5/26
# Implemented approach: RegionKNN [Chen et al, ICWS'2010]
# Evaluation metrics: MAE, NMAE, RMSE, MRE, NPRE
########################################################

import numpy as np
import os, sys, time
sys.path.append('src')
# Build external model
if not os.path.isfile('src/RegionKNN.so'):
	print 'Lack of RegionKNN.so (the built C++ module of core RegionKNN).' 
	print 'Please first build the C++ code into RegionKNN.so by using: '
	print '>> python setup.py build_ext --inplace'
	sys.exit()
from utilities import *
import execute
 

#########################################################
# config area
#
para = {'dataPath': '../../data/dataset#1/rtMatrix.txt',
		'userLocFile': '../../data/dataset#1/userlist.txt',
		'wsLocFile': '../../data/dataset#1/wslist.txt',
		'outPath': 'result/rtResult_',
		'metrics': ['MAE', 'NMAE', 'RMSE', 'MRE', 'NPRE'], # delete where appropriate
		# matrix density
		'density': list(np.arange(0.01, 0.051, 0.01))
					+ list(np.arange(0.10, 0.31, 0.05)),
		'rounds': 20, # how many runs are performed at each matrix density
        'topK': 10, # the parameter of TopK similar users or services, the default value is
					# topK = 10 as in the reference paper
		'lambda': 0.8, # the threshold for sensitive region, lambda = 0.8 in the paper
	   	'mu_u': 0.3, # the threshold for user region clustering
		'saveTimeInfo': False, # whether to keep track of the running time
		'saveLog': False, # whether to save log into file
		'debugMode': False # whether to record the debug info
		}

initConfig(para)
#########################################################


startTime = time.clock() # start timing
logger.info('==============================================')
logger.info('Approach: RegionKNN [Chen et al, ICWS\'2010].')
logger.info('Loading data: %s'%para['dataPath'])
dataMatrix = np.loadtxt(para['dataPath']) 

# get the inital user regions
initUserRegion = execute.RegionKNN.getInitalRegion(para)
logger.info('Create initial user regions done.')

# run for each density
for density in para['density']:
    execute.predict(dataMatrix, initUserRegion, density, para)

logger.info(time.strftime('All done. Total running time: %d-th day - %Hhour - %Mmin - %Ssec.',
         time.gmtime(time.clock() - startTime)))
logger.info('==============================================')
sys.path.remove('src')


