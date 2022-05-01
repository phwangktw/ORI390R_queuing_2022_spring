# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 17:42:13 2022

@author: phwangk
"""

import ciw
import pandas as pd

def arrival_queue_init():
    
    # manually read the data here
    para_df = pd.read_csv('./parameters_raw.csv')
    
    arrival_distributions = {}
    
    # create the corresponding ciw distribution object
    # N = len(para_df)
    class_0_list = []
    
    for index, row in para_df.iterrows():
        
        if row.Exogenous_rate != 0:
            temp_dist_obj = ciw.dists.Exponential(rate=row.Exogenous_rate)
        else:
            temp_dist_obj = ciw.dists.NoArrivals()       
        
        
        class_0_list.append(temp_dist_obj)
    
    arrival_distributions['Class 0'] = class_0_list
    return arrival_distributions


def service_distributions_init():
    
    # manually read the data here
    para_df = pd.read_csv('./parameters_raw.csv')
    
    service_distributions = {}
    
    # create the corresponding ciw distribution object
    # N = len(para_df)
    class_0_list = []
    probs_list = [0.9, 0.1]
    
    for index, row in para_df.iterrows():
        temp_rate_list = []
        temp_rate_list.append(row.Service_rate_1)
        temp_rate_list.append( row.Service_rate_2)
        
        Hx_temp = ciw.dists.HyperExponential(rates=temp_rate_list, probs=probs_list)
        
        class_0_list.append(Hx_temp)
    
    service_distributions['Class 0'] = class_0_list
    # Hx = ciw.dists.HyperExponential(rates=[9, 5, 6, 1], probs=[0.2, 0.1, 0.6, 0.1])
    return service_distributions

def routing_init():
    
    # manually read the data here
    para_df = pd.read_csv('./parameters_raw.csv')
    
    arrival_distributions = {}
    
    # create the corresponding ciw distribution object
    # N = len(para_df)
    class_0_list = []
    probs_list = [0.9, 0.1]
    
    for index, row in para_df.iterrows():
        temp_rate_list = []
        temp_rate_list.append(row.Service_rate_1)
        temp_rate_list.append( row.Service_rate_2)
        
        Hx_temp = ciw.dists.HyperExponential(rates=temp_rate_list, probs=probs_list)
        
        class_0_list.append(Hx_temp)
    
    arrival_distributions['Class 0'] = class_0_list
    # Hx = ciw.dists.HyperExponential(rates=[9, 5, 6, 1], probs=[0.2, 0.1, 0.6, 0.1])
    return arrival_distributions