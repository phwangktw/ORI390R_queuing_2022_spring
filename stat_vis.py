# -*- coding: utf-8 -*-
"""
Created on Sun May  1 10:58:38 2022

@author: phwangk

1. Visualize utilization of each station

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

def plot_util(node_object_list):
    df_plot = pd.DataFrame()
    for j in range(len(node_object_list)):
        raw_dict = {}     
        for i in node_object_list:    
            keyName = str(i.id_number)
            raw_dict[keyName] = round(i.server_utilisation, 3)
        df_plot_temp = pd.DataFrame.from_dict(raw_dict, orient='index', columns=['utilization'])
        if j ==0:
            df_plot = df_plot_temp
        else:
            df_plot = pd.concat([df_plot, df_plot_temp])
    
    
    df_plot.reset_index(inplace=True)
    
    fig, ax = plt.subplots()
    ax = sns.barplot(x="index", y="utilization", data=df_plot,
                 palette="Blues_d")
    
    # ax.set_xlim(0, 0.35)
    # ax.set_ylim(0, 0.3)
    ax.set_xlabel('Node #')
    ax.set_ylabel('Utilization')
    
    ax.bar_label(ax.containers[0])
    # ax.legend(loc='lower right')
    plt.title('Utilizations of each node')
    plt.show()


def gantt_generate(recs_list, nodeNumber):
    
    raw = recs_list[0]
    
    arrival_date_list = [r.arrival_date for r in raw]
    waiting_time_list = [r.waiting_time for r in raw]
    service_time_list = [r.service_time for r in raw]
    service_end_date_list = [r.service_end_date for r in raw]
    exit_date_list = [r.exit_date for r in raw]
    node_list = [r.node for r in raw]
    server_id_list = [r.server_id for r in raw]
    
    df = pd.DataFrame(
        {'arrival_date': arrival_date_list,
         'waiting_time': waiting_time_list,
         'service_time': service_time_list,
         'service_end_date': service_end_date_list,
         'exit_date': exit_date_list,
         'node': node_list,
         'server_id': server_id_list,
        })
    
    df['service_start'] = df['arrival_date'] + df['waiting_time'] 
    df_station = df[df['node']==nodeNumber].sort_values(by = ['server_id', 'service_start']).reset_index(drop=True)
    del df
    dum = 1
    
    fig, ax = plt.subplots()
    ax.barh(df_station.server_id, df_station.service_time, left=df_station.service_start)
    plt.gca().invert_yaxis()
    ax.set_yticks(np.arange(1, 12, 1, dtype=int))
    ax.set_xlabel('time (hr)')
    ax.set_ylabel('server_id')
    
    plt.show()
    

def queue_plot(recs_list):
    raw = recs_list[0]
    
    arrival_date_list = [r.arrival_date for r in raw]
    queue_size_at_arrival_list = [r.queue_size_at_arrival for r in raw]
    node_list = [r.node for r in raw]
    
    df = pd.DataFrame(
        {'arrival_date': arrival_date_list,
         'node': node_list,
         'queue_size_at_arrival': queue_size_at_arrival_list,
        })
    
    fig, axes = plt.subplots(1, 3, figsize=(14,5))
    # figurecount = 1
    plot_time = 0
    for fig_i in range(3):
        maxtime = df['arrival_date'].max()
        plot_interval = maxtime/3
        plot_time = plot_interval*(fig_i+1)
        
        # extract the time close to current plot-time for each node
        df['time_gap'] = abs(plot_time - df['arrival_date'])
        df_plot_temp = df.loc[df.groupby('node').time_gap.idxmin()]
        
        sns.barplot(ax=axes[fig_i], x='node', y='queue_size_at_arrival', data=df_plot_temp)
        #subplot >2 rows: https://dev.to/thalesbruno/subplotting-with-matplotlib-and-seaborn-5ei8
        axes[fig_i].set_title('time='+str(round(plot_time,0)))
        
        
        # figurecount += 1
    plt.show()
    
    
def overall_queue_plot(recs_list, simu_num, maxtime):
    
    time_intervals = 300
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
    
    fig, ax = plt.subplots()
    sns.lineplot(x="time", y="queue_num", markers=True, data=df_plot)
    # ax.set_yticks(np.arange(1, 12, 1, dtype=int))
    ax.set_xlabel('time (hr)')
    ax.set_ylabel('queue_num in the system')
    
    plt.show()
    
def overall_queue_plot2(expt_result_all, simu_num, maxtime):
    expt = 3
    fig, ax = plt.subplots()
    for expt_i in range(expt):
        recs_list = expt_result_all[expt_i]
        time_intervals = 300
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
        
        
        sns.lineplot(x="time", y="queue_num", markers=True, data=df_plot, legend='brief', label="Expt_"+str(expt_i+1))
        # ax.set_yticks(np.arange(1, 12, 1, dtype=int))
    ax.set_xlabel('time (hr)')
    ax.set_ylabel('queue_num in the system')
    ax.legend()
    plt.show()