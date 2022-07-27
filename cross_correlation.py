#!/bin/env/python
import os

#Import from other libraries:
import numpy as np
import matplotlib.pyplot as plt

import nitime
#Import the time-series objects:
from nitime.timeseries import TimeSeries
#Import the analysis objects:
from nitime.analysis import CorrelationAnalyzer, CoherenceAnalyzer
#Import utility functions:
from nitime.utils import percent_change
from nitime.viz import drawmatrix_channels, drawgraph_channels, plot_xcorr
from pylab import figure, axes, pie, title, show
#turn off scientific notation
np.set_printoptions(suppress=True)


subjects=[
 'MID0001',
 'MID0002', 
 'MID0003',
 'MID0004', 
 'MID0005', 
 'MID0006', 
 #'MID0008', 
 'MID0009', 
 'MID0010', 
 'MID0011', 
 'MID0012', 
 'MID0013',
 'MID0015', 
 'MID0020', 
 'MID0021', 
 'MID0022', 
 'MID0023', 
 'MID0025', 
 'MID0026', 
 'MID0028', 
 'MID0029',
 'MID0030', 
 'MID0031', 
 'MID0032', 
 'MID0033', 
 'MID0034', 
 'MID0035', 
 'MID0036', 
 #'MID0037', 
 'MID0038', 
 'MID0039', 
 'MID0040', 
 'MID0041', 
 'MID0042', 
 'MID0043', 
 'MID0045', 
 'MID0046', 
 'MID0047', 
 'MID0048',
 'MID0049',
 'MID0050', 
 'NECON0001',
 'NECON0006',
 'NECON0007',
 'NECON0009',
 'NECON0010',
 'NECON0011',
 'NECON0012',
 'NECON0013',
 'NECON0014',
 'NECON0015',
 'NECON0016',
 'NECON0017',
 'NECON0018',
 'NECON0019',
 'NECON0020',
 'NECON0021',
 'NECON0023',
 'NECON0024',
 'NECON0025',
 'NECON0026',
 'NECON0027',
 'NECON0028',
 'NECON0029',
 'NECON0030',
 'NECON0031',
 'NECON0032',
 'NECON0033',
 'NECON0034',
 'NECON0035',
 'NECON0036',
 'NECON0037',
 'NECON0039',
 'NECON0040'  
 ]

TR = 2.2
f_lb = 0.02
f_ub = 0.15

for subject in subjects: 

	data_path = os.path.join(nitime.__path__[0], 'data')
	data_rec = np.genfromtxt(os.path.join(data_path, '/Volumes/ActiveStorage-11TB/RSP.01/Analysis/timeseries_data/%(MYSUBJECT)s/%(MYSUBJECT)s_timeseries.txt' %{"MYSUBJECT": (subject)}), names=True, delimiter=',')


	roi_names = np.array(data_rec.dtype.names)
	n_samples = data_rec.shape[0]


	#Make an empty container for the data
	data = np.zeros((len(roi_names), n_samples))

	for n_idx, roi in enumerate(roi_names):
 	   data[n_idx] = data_rec[roi]

	#Normalize the data:
	data = percent_change(data)


	T = TimeSeries(data, sampling_interval=TR)
	T.metadata['roi'] = roi_names
	C = CorrelationAnalyzer(T)

	#save single subject results as a csv
	np.savetxt('/Volumes/ActiveStorage-11TB/RSP.01/Analysis/timeseries_data/%(MYSUBJECT)s/%(MYSUBJECT)s_cross_correlation_2d.csv' %{"MYSUBJECT": (subject)}, C.corrcoef,'%5.7f', delimiter=',') 

	#flatten the matrix, and save as csv
	c=np.array(C.corrcoef)
	f=c.flatten()
	np.savetxt('/Volumes/ActiveStorage-11TB/RSP.01/Analysis/timeseries_data/%(MYSUBJECT)s/%(MYSUBJECT)s_cross_correlation_1d.csv' %{"MYSUBJECT": (subject)}, f,'%5.7f', delimiter=',') 


#make an empty array
a=[]

#append all into a single matrix and output into results directory
for subject in subjects: 
	single_subject_results=np.genfromtxt('/Volumes/ActiveStorage-11TB/RSP.01/Analysis/timeseries_data/%(MYSUBJECT)s/%(MYSUBJECT)s_cross_correlation_1d.csv' %{"MYSUBJECT": (subject)},delimiter=',')
	#a=np.concatenate((a,single_subject_results),axis=1)
	a.append(single_subject_results)

a_array=np.array(a)

np.savetxt('group_results.csv',a_array, '%5.7f', delimiter=',')