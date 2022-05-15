# -*- coding: utf-8 -*-
"""
Created on Fri May  6 22:07:41 2022

@author: phwangk

GA optimizer + CIW simulation



"""

import pygad
import numpy

import simulator as sm

# Set cost for deposition to 2, polishing to 1, photo to 8, etch to 5

# function_inputs = [2,1,8,5,2,2,1,8,5,2,1,8,5] #The wieght for each machine type
# desired_output = 500 #The target for obj. function

def fitness_func(solution, solution_idx): #Obj. function, can be modified
    print('Current combination:')
    print(solution)
    output = sm.cost_evaluation(solution)
    print('Cost ='+str(-1*output))
    fitness = 1.0 / output
    
    return fitness

ga_instance = pygad.GA(num_generations=20, #Number of iteration
                       num_parents_mating=4, #Number of parent genes
                       sol_per_pop=50, #Number of offspring per iteration
                       num_genes=13, #Number of genes
                       fitness_func=fitness_func,
                       mutation_type="adaptive", #Increasing mutation to change values
                       mutation_probability=[0.6, 0.2], 

                       init_range_low=1,
                       init_range_high=10,
                       gene_space = [range(1,8),range(1,10),range(6,16),range(3,13),
                                     range(1,10),range(1,8),range(1,11),range(2,12),
                                     range(2,12),range(1,8),range(1,10),range(2,12),
                                     range(3,13)],
                      
                       gene_type=int)

#print(ga_instance.initial_population)
#print(ga_instance.initial_population.shape)
ga_instance.run()
ga_instance.plot_result()
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))