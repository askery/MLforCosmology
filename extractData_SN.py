#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:52:58 2018

@author: askery
"""
from datetime import datetime
start=datetime.now()

import numpy as np
import pandas as pd
import re
import os

path = '/home/data/research/IIP/ML/colab/luciano/rawdata/SIMGEN_PUBLIC_DES'
files = [f for f in os.listdir(path) if f.endswith('.DAT')]

frames = []
for file in files:
    with open(path + '/' + file, 'r') as infile:
        line = infile.readlines()
        
    data = []    
    for i in line:
        if 'Type' in i:
            sntype = i
        if 'VARLIST' in i:
            header = i
        if 'OBS:' in i:
            data.append(i)
            
    for i in data:
        if 'NOBS' in i:
            data.remove(i)
    
    typeSN = sntype[sntype.find("=")+1:sntype.find(",")]
    typeSN = typeSN.strip()
    
    features = header[header.find(":")+1:header.find("_")+4]
    features = features.strip()
    features = re.sub('\s+',',', features)
    features = features.split(",")
    #features = features.split("  ")
    
    #features = ['MJD','FLT','FIELD','FLUXCAL','FLUXCALERR','SNR','MAG','MAGERR','SIM_MAG']
    
    data = [i.rstrip('\n') for i in data]
    data = [i.lstrip('OBS:') for i in data]
    data = [i.strip() for i in data]
    data = [re.sub('\s+',',', i) for i in data]
    data = [i.split(",") for i in data]
    type_list =  len(data)*[typeSN]
    type_list = [[i] for i in type_list]
    
    type_array = np.array(type_list)
    data_array = np.array(data)
    features = features + ['TYPE']
    fulldata = np.concatenate((data_array,type_array), axis=1)
    
    df_data = pd.DataFrame(fulldata, columns = features)
    frames.append(df_data)

df_fulldata = pd.concat(frames)
print (   df_fulldata.describe(include='all')  )
print( '# of files in the folder: ', len(files))
      
print ('job duration in s: ', datetime.now() - start)