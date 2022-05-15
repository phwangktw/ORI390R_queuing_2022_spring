# -*- coding: utf-8 -*-
"""
Created on Fri May  6 22:12:26 2022

@author: phwangk

exogenous rate = 6 lots/hr
class: single class
station J: J=13
Service rate: Hyper exponential [0.9, 0.1], 10% of fast-passed engineering lots

Other characteristics:
    rework situations: x
    inspection stations: x
    BEOL engineering testing lot: x

"""

import ciw
import network_init_13 as init
import numpy as np
import pandas as pd



def get_queue_sum(recs_list, simu_num, maxtime, t1=250): 
    
    time_intervals = 100
    temp_q_length = np.zeros(time_intervals)    
    interval_list = np.linspace(0, maxtime, time_intervals).tolist()
    for loop in range(simu_num):
    # for loop all simulation results
        raw = recs_list[loop]
        
        arrival_date_list = [r.arrival_date for r in raw]
        queue_size_at_arrival_list = [r.queue_size_at_arrival for r in raw]
        node_list = [r.node for r in raw]
        
        
        df = pd.DataFrame(
            {'arrival_date': arrival_date_list,
             'node': node_list,
             'queue_size_at_arrival': queue_size_at_arrival_list,
            })        
        
        # maxtime = df['arrival_date'].max()       
        
        for i in range(time_intervals):
            cur_time = interval_list[i]
            df['time_gap'] = abs(i - df['arrival_date'])
            df_plot_temp = df.loc[df.groupby('node').time_gap.idxmin()]
            cur_queue = df_plot_temp.queue_size_at_arrival.sum()        
            temp_q_length[i] += cur_queue
            
    avg_q_length = temp_q_length/simu_num        
    df_plot = pd.DataFrame(interval_list, columns = ['time'])
        
    df_plot = pd.concat([df_plot, pd.DataFrame(avg_q_length, columns = ['queue_num'])], axis=1)
    
    #select the long-run average timespan t1 to maxtime
    return df_plot[df_plot['time']>=t1].queue_num.mean()
    

def get_queue_individual(recs_list, simu_num, maxtime, t1=250):
    
    time_intervals = 100
    temp_q_length = np.zeros(time_intervals)    
    interval_list = np.linspace(0, maxtime, time_intervals).tolist()
    cur_queue = np.zeros((time_intervals, 13))
    for loop in range(simu_num):
        
    # for loop all simulation results
        raw = recs_list[loop]
        
        arrival_date_list = [r.arrival_date for r in raw]
        queue_size_at_arrival_list = [r.queue_size_at_arrival for r in raw]
        node_list = [r.node for r in raw]
        
        
        df = pd.DataFrame(
            {'arrival_date': arrival_date_list,
             'node': node_list,
             'queue_size_at_arrival': queue_size_at_arrival_list,
            })        
        
        # maxtime = df['arrival_date'].max()       
        station_set = set(np.arange(1, 14, dtype=int).flatten())
        for i in range(time_intervals):
            cur_time = interval_list[i]
            df['time_gap'] = abs(i - df['arrival_date'])
            df_plot_temp = df.loc[df.groupby('node').time_gap.idxmin()][['node','queue_size_at_arrival']]
            
            if (df_plot_temp.shape[0] != 13):                
                
                temp_set = set(df_plot_temp['node'].tolist())
                lst1 = list(station_set-temp_set)
                lst2 = [0]*len(lst1)
                df_set_diff = pd.DataFrame(list(zip(lst1, lst2)), columns =['node','queue_size_at_arrival'])
                
                df_plot_temp = pd.concat([df_plot_temp, df_set_diff], axis=0)
                
            cur_queue[i] += df_plot_temp.queue_size_at_arrival.tolist()
            
    cur_queue = cur_queue/simu_num
    
    index = min(range(len(interval_list)), key=lambda i: abs(interval_list[i]-t1))
    
    #select the long-run average timespan t1 to maxtime
    return cur_queue[index:,:].mean(axis=0)


def cost_evaluation(solution):
    ## Main simulator is here (objective function evaluation)

    ## distribution list (arrival) initialization
    arrival_distributions_input = init.arrival_queue_init()
    service_distributions_input = init.service_distributions_init()
    routing_input = init.routing_init()
    
    # number_of_servers = [3,5,11,8,5,3,6,7,7,3,5,7,8]
    number_of_servers = solution.tolist()
    
    class_change_matrices_input = init.class_change_matrices_init()

    N = ciw.create_network(arrival_distributions=arrival_distributions_input,
                           service_distributions=service_distributions_input,
                           routing=routing_input,
                           class_change_matrices=class_change_matrices_input,
                           number_of_servers = number_of_servers
       )

    # Step2. Simulation (10 times)
    node_result_list = []
    recs_list = []
    simu_num = 10
    max_time = 300
    for trial in range(simu_num):
        ciw.seed(trial)
        Q = ciw.Simulation(N)
        Q.simulate_until_max_time(max_time)
        recs_list.append(Q.get_all_records())
        node_result_list.append(Q.transitive_nodes)
        
    q_each = get_queue_individual(recs_list, simu_num, max_time)
    Q_total = get_queue_sum(recs_list, simu_num, max_time)
    
    cei = [2.63,1.23,9.77,4.01,2.51,0.1,1.29,3.35,5.65,2.64,1.72,9.73,1.5]
    cqi = [0.9,0.55,0.61,0.89,0.84,0.43,0.37,0.29,0.12,0.35,0.72,0.65,0.62]
    total_hold_cost = 1
    
    ce = np.sum(solution*np.array(cei))
    cq = np.sum(q_each*np.array(cqi))
    cQ = total_hold_cost*Q_total
    
    return (ce+cq+cQ)
    
    