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


def gantt_generate():
    
    dumy = 1