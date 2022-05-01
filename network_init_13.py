# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 17:42:13 2022

@author: phwangk
"""

import ciw
import pandas as pd
import numpy as np

def arrival_queue_init():
    
    # manually read the data here
    para_df = pd.read_csv('./parameters_raw_test.csv')
    
    arrival_distributions = {}
    classNum = ['Class 0', 'Class 1']
    # create the corresponding ciw distribution object
    # N = len(para_df)
    
    for i in classNum:
        class_0_list = []
        
        if i == 'Class 0':
            for index, row in para_df.iterrows():
                
                if row.Exogenous_rate != 0:
                    temp_dist_obj = ciw.dists.Exponential(rate=row.Exogenous_rate)
                else:
                    temp_dist_obj = ciw.dists.NoArrivals()       
                
                
                class_0_list.append(temp_dist_obj)
        
            arrival_distributions[i] = class_0_list
        else:
            for index, row in para_df.iterrows():
                temp_dist_obj = ciw.dists.NoArrivals()
                class_0_list.append(temp_dist_obj)
            arrival_distributions[i] = class_0_list
            
    return arrival_distributions


def service_distributions_init():
    
    # manually read the data here
    para_df = pd.read_csv('./parameters_raw_test.csv')
    
    service_distributions = {}
    
    # create the corresponding ciw distribution object
    # N = len(para_df)
    
    probs_list = [0.9, 0.1]
    
    classNum = ['Class 0', 'Class 1']
    changepoint = 9
    for i in classNum:
        class_0_list = []
        if i == 'Class 0':
            for index, row in para_df.iterrows():
                if row.Node <= changepoint:
                    temp_rate_list = []
                    temp_rate_list.append(row.Service_rate_1)
                    temp_rate_list.append(row.Service_rate_2)
                    
                    Hx_temp = ciw.dists.HyperExponential(rates=temp_rate_list, probs=probs_list)                
                    class_0_list.append(Hx_temp)
                else:
                    norate = ciw.dists.Deterministic(value=0.0)
                    class_0_list.append(norate)
            service_distributions[i] = class_0_list
            
        else:
            for index, row in para_df.iterrows():
                #TODO: temporarily add
                if row.Node == 5:
                    temp_rate_list = []
                    temp_rate_list.append(row.Service_rate_1)
                    temp_rate_list.append(row.Service_rate_2)
                    
                    Hx_temp = ciw.dists.HyperExponential(rates=temp_rate_list, probs=probs_list)                
                    class_0_list.append(Hx_temp)
                
                elif row.Node < changepoint:
                    norate = ciw.dists.Deterministic(value=0.0)
                    class_0_list.append(norate)
                else:
                    temp_rate_list = []
                    temp_rate_list.append(row.Service_rate_1)
                    temp_rate_list.append(row.Service_rate_2)
                    
                    Hx_temp = ciw.dists.HyperExponential(rates=temp_rate_list, probs=probs_list)                
                    class_0_list.append(Hx_temp)
            service_distributions[i] = class_0_list
        
        service_distributions[i] = class_0_list
        
    return service_distributions

def routing_init():
    
    classNum = ['Class 0', 'Class 1']
    # manually read the data here
    path1 = './class1_transition.csv'
    array1 = np.loadtxt(open(path1), delimiter=",", skiprows=1)
    
    path2 = './class2_transition.csv'
    array2 = np.loadtxt(open(path2), delimiter=",", skiprows=1)
    
    routing_input = {}
    for i in classNum:
        if i == 'Class 0':
            routing_input[i] = array1.tolist()
            
        else:
            routing_input[i] = array2.tolist()
    
    return routing_input


def class_change_matrices_init():
    
    # manually read the data here
    para_df = pd.read_csv('./parameters_raw_test.csv')
    class_change_matrices_input = {}
    changepoint = 8
    for i in range(len(para_df)):
        tempKey = "Node "+str(i+1)
        if i == changepoint:
            class_change_matrices_input[tempKey] = [[0.0, 1.0],[0.0, 1.0]]
        else:
            class_change_matrices_input[tempKey] = [[1.0, 0.0],[0.0, 1.0]]
    
    return class_change_matrices_input