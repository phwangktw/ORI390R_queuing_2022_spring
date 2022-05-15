# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 17:08:57 2022

@author: phwangk

exogenous rate = 6 lots/hr
class: single class
station J: J=26
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
import matplotlib.pyplot as plt
import seaborn as sns
import stat_vis as vis
sns.set_style("whitegrid")



# Step1. Network Initialization

## distribution list (arrival) initialization
arrival_distributions_input = init.arrival_queue_init()
service_distributions_input = init.service_distributions_init()
routing_input = init.routing_init()
number_of_servers = [3,5,11,8,5,3,6,7,7,3,5,7,8]
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
max_time = 360
for trial in range(simu_num):
    ciw.seed(trial)
    Q = ciw.Simulation(N)
    Q.simulate_until_max_time(max_time)
    recs_list.append(Q.get_all_records())
    node_result_list.append(Q.transitive_nodes)
    
# Step3. Analytical plot from the simulation results
## 3-4 Queue length
vis.overall_queue_plot(recs_list, simu_num, max_time)

## 3-1 Utilization
vis.plot_util(Q.transitive_nodes)

## 3-2 Single station Gantt plot
nodeStation = 3
vis.gantt_generate(recs_list, nodeStation)

## 3-3 Queue length
vis.queue_plot(recs_list)

# Results summary
## all records change to df
# customer_class_list = [r.customer_class for r in recs]
# node_list = [r.node for r in recs]
# arrival_date_list = [r.arrival_date for r in recs]
# waiting_time_list = [r.waiting_time for r in recs]
# service_time_list = [r.service_time for r in recs]
# service_end_date_list = [r.service_end_date for r in recs]
# time_blocked_list = [r.time_blocked for r in recs]
# exit_date_list = [r.exit_date for r in recs]
# destination_list = [r.destination for r in recs]
# queue_size_at_arrival_list = [r.queue_size_at_arrival for r in recs]
# queue_size_at_departure_list = [r.queue_size_at_departure for r in recs]
# server_id_list = [r.server_id for r in recs]

# df = pd.DataFrame(
#     {'customer_class': customer_class_list,
#      'node': node_list,
#      'arrival_date': arrival_date_list,
#      'waiting_time': waiting_time_list,
#      'service_time': service_time_list,
#      'service_end_date': service_end_date_list,
#      'time_blocked': time_blocked_list,
#      'exit_date': exit_date_list,
#      'destination': destination_list,
#      'queue_size_at_arrival': queue_size_at_arrival_list,
#      'queue_size_at_departure': queue_size_at_departure_list,
#      'server_id': server_id_list
#     })

