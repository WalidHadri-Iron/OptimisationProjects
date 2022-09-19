#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose:
    Preparing the dataset for implemetation of an algorithm which solves the VeRoLog problem. 
Date:
    2019/1/31
"""
###########################################################
### imports
import pandas as pd
import numpy as np
import numpy.random as rnd
import scipy.stats as stats
import timeit as ti
import matplotlib.pyplot as plt
from networkx import nx
import csv as csv
###########################################################
###
def calculateEucdist(locations,numberLocations):
    """
        Purpose
            calculate euclidean distance between the different locations by using x and y coordinates
        Input
            locations, np.array with in each line a location (index 0), a x coordinate (index 1) and y coordinate (index 2)
            numberLocations, a integer with the number of locations for the instance
        Output
            graph, a matrix with the distance between every point
    """
    graph = np.zeros((numberLocations,numberLocations))
    for location1 in locations:
        i = location1[0]-1
        x1 = location1[1]
        y1 = location1[2]
        for location2 in locations:
            j = location2[0]-1
            x2 = location2[1]
            y2 = location2[2]
            graph[i][j] = graph[j][i] = np.ceil(np.sqrt((x1-x2)**2+(y1-y2)**2))
            
    return graph

def loadfile(filename):
    """
        Purpose
            import the data for the given filename
        Input
            filename, name of file that has to be given
            seperator, the seperator of the file, ';' for csv, '\s+' for txt
        Output
            tuple with all the necessary input for the instance in the file
    """
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    dataset = content[0].split('=')[1].strip()
    dataset_name = content[1].split('=')[1].strip()
    days = int(content[3].split('=')[1])
    truck_capacity = int(content[4].split('=')[1])
    truck_max_distance = int(content[5].split('=')[1])
    truck_distance_cost = int(content[7].split('=')[1])
    truck_day_cost = int(content[8].split('=')[1])
    truck_cost = int(content[9].split('=')[1])
    technician_distance_cost = int(content[10].split('=')[1])
    technician_day_cost = int(content[11].split('=')[1])
    technician_cost = int(content[12].split('=')[1])

    nbr_machines = int(content[14].split('=')[1])
    matrix_machines = []
    for i in range(nbr_machines):
        line = content[15+i]
        list_split = line.split()
        list_split = line.split()
        list_split = [int(i) for i in list_split]
        matrix_machines.append(list_split)
    matrix_machines = np.array(matrix_machines)
    df_matrix_machines = pd.DataFrame(matrix_machines, columns=['id_machine','size_machine','penalty_machine'])

    current_line_index = 15 + nbr_machines + 1
    nbr_locations = int(content[current_line_index].split('=')[1])
    matrix_locations = []
    for i in range(nbr_locations):
        line = content[current_line_index+ 1 +i]
        list_split = line.split()
        list_split = [int(i) for i in list_split]
        matrix_locations.append(list_split)
    matrix_locations = np.array(matrix_locations)
    df_matrix_locations = pd.DataFrame(matrix_locations, columns=['id_location','x','y'])

    current_line_index = current_line_index + nbr_locations + 2
    nbr_requests = int(content[current_line_index].split('=')[1])
    matrix_requests = []
    for i in range(nbr_requests):
        line = content[current_line_index+ 1 +i]
        list_split = line.split()
        list_split = [int(i) for i in list_split]
        matrix_requests.append(list_split)
    matrix_requests = np.array(matrix_requests)
    df_matrix_requests = pd.DataFrame(matrix_requests, columns=['id_request','id_location','first_day','last_day','id_machine','nbr_machine'])

    current_line_index = current_line_index + nbr_requests + 2
    nbr_technicians = int(content[current_line_index].split('=')[1])
    matrix_technician = []
    for i in range(nbr_technicians):
        line = content[current_line_index+ 1 +i]
        list_split = line.split()
        list_split = [int(i) for i in list_split]
        matrix_technician.append(list_split)
    matrix_technician = np.array(matrix_technician)
    out = []
    for i in range(nbr_machines):
        out.append(f'skill_machine_{i+1}')
    df_matrix_technician = pd.DataFrame(matrix_technician, columns=['id_technician','id_location','max_distance_technician','max_nbr_installation']+out)
    dict_1 = {'DAYS':days, 'TRUCK_CAPACITY':truck_capacity, 'TRUCK_MAX_DISTANCE':truck_max_distance}
    dict_2 = {'TRUCK_DISTANCE_COST':truck_distance_cost, 'TRUCK_DAY_COST':truck_day_cost, 'TRUCK_COST':truck_cost,
         'TECHNICIAN_DISTANCE_COST':technician_distance_cost,'TECHNICIAN_DAY_COST':technician_day_cost,'TECHNICIAN_COST':technician_cost}
    return dict_1, dict_2, nbr_machines,matrix_machines,nbr_locations,matrix_locations,nbr_requests,matrix_requests,nbr_technicians,matrix_technician


###########################################################
### main
def main():
  
    return

if __name__ == '__main__':
    main()