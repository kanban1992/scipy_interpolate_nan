import readData

import numpy as np

from random import randint
import random

import math
import sys
import scipy.interpolate as ip_scipy


from ROOT import TFile, TH2D, TCanvas


# # # # # # ## 
#Read in data#
#            #

file_dir="./TH2D_A00_TB10.root"
file_name="TH2D_A00_TB10.root"
hist_name= "LHCChi2_CMSSM_nObs1061_A00_TB10"


rfile = TFile(file_dir)
histogram = rfile.Get(hist_name)


N=histogram.GetXaxis().GetNbins() * histogram.GetYaxis().GetNbins() #number of points in full_set

x=np.ndarray(shape=(N,2))
y=np.ndarray(shape=(N,1))

i=0
for x_bin in range(0, histogram.GetXaxis().GetNbins()):
  for y_bin in range(0, histogram.GetYaxis().GetNbins()):
    x[i][0]=histogram.GetXaxis().GetBinCenter(x_bin)
    x[i][1]=histogram.GetYaxis().GetBinCenter(y_bin)
    y[i][0]=histogram.GetBinContent(x_bin,y_bin)
    if i<10:
      print x[i][0]
    #set the maximum output
    if y[i][0] >100.0:
      y[i][0] =100.0
    i=i+1

N_validation = 10000
N_training = N-N_validation

full_indices=range(0,N)

random.shuffle(full_indices)

training_indices=full_indices[:N_training]#indices for training set
validation_indices=full_indices[N_training:N]#indices for validation set

x_training=np.ndarray(shape=(N_training,2))
y_training=np.ndarray(shape=(N_training,1))

for i in range(0,N_training):
  x_training[i][0]=x[training_indices[i]][0]
  x_training[i][1]=x[training_indices[i]][1]
  y_training[i][0]=y[training_indices[i]][0]	    


x_validation=np.ndarray(shape=(N_validation,2))
y_validation=np.ndarray(shape=(N_validation,1))

for i in range(0,N_validation):
  x_validation[i][0]=x[validation_indices[i]][0]
  x_validation[i][1]=x[validation_indices[i]][1]
  y_validation[i][0]=y[validation_indices[i]][0]	


# # # # # # # # # # ## 
#simple interpolation#
#                    #

#scipy library

interpol = ip_scipy.LinearNDInterpolator(x_training,y_training) # this algorithm is not stable and gives nan sometimes

y_interpol=interpol(x_validation)

error_interpol=np.sum(np.absolute(np.subtract(y_interpol,y_validation)))

print "total error with interpolation"
print error_interpol

