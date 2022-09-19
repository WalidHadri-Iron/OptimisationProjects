import numpy as np
import pandas as pd
import networkx as nx
import argparse
from itertools import groupby
from gurobipy import *

def return_path(steps, root):
    G = nx.DiGraph()
    G.add_edges_from(e for e in steps)
    cycles = list(nx.simple_cycles(G))
    path_out = []
    for cycle in cycles:
        cycle = [element for element in cycle if element!=root]
        path_out += cycle
        path_out.append(root)
    return path_out[:-1]

def main():
    # filename = 'instances 2021/CO_Case2021_01.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="path to file")
    parser.add_argument("time_limit", help="time limit in seconds")
    args = parser.parse_args()
    filename = args.file_name
    time_limit = float(args.time_limit)
    
    ####################   Reading the file    ################################################
    
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
    nbr_days = days
    rmax = matrix_requests.shape[0]
    nbr_nodes = 1 + rmax #We include the depot
    kmax = rmax #Number of vehicules set to rmax, as the numbre of vehicules is illimited, this is sufficient
    s = matrix_technician.shape[0]
    #Setting the R_s graph
    techni_set = dict()
    for i in range(1, nbr_technicians+1):
        techni_set[i] = []
        for j in range(1, nbr_requests+1):
            id_machine = df_matrix_requests[df_matrix_requests.id_request == j].id_machine.values[0]
            if df_matrix_technician.iloc[i-1,id_machine+3] == 1:
                techni_set[i] = techni_set[i] + [j]
                
    ######################## Define decision variables ########################################
                
    model = Model()
    x = model.addVars(nbr_nodes, nbr_nodes, range(1,kmax+1), range(1,nbr_days+1), vtype = GRB.BINARY)
    z = model.addVars(range(nbr_requests + nbr_technicians+1), range(nbr_requests + nbr_technicians+1), range(1,s+1), range(1,nbr_days+1), vtype = GRB.BINARY)
    for techni_id in techni_set:
        list_nodes = [techni_id+nbr_requests]+techni_set[techni_id]
        model.addConstrs(z[i,j,techni_id,t] == 0 for i in range(nbr_requests+nbr_technicians+1) if i not in list_nodes for j in range(nbr_requests+nbr_technicians+1) if j not in list_nodes for t in range(1, nbr_days+1))
    m = model.addVars(range(1,kmax+1), vtype = GRB.BINARY)
    r = model.addVars(range(1,s+1), vtype = GRB.BINARY)
    v = model.addVars(range(1,kmax+1), range(1,nbr_days+1), vtype = GRB.BINARY)
    p = model.addVars(range(1,s+1), range(1,nbr_days+1), vtype = GRB.BINARY)
    q = model.addVars(nbr_nodes, range(1,kmax+1), vtype = GRB.INTEGER)
    g = model.addVars(nbr_nodes + nbr_technicians, range(1,s+1), vtype = GRB.INTEGER)
    b = model.addVars(range(1,nbr_requests+1), vtype = GRB.INTEGER)


    ########################### Define the objective function ##############################################
    alpha = truck_cost
    beta = technician_cost
    gamma = truck_day_cost
    kappa = technician_day_cost
    mu = truck_distance_cost
    nu = technician_distance_cost
    #setting tau
    tau = np.array(pd.merge(df_matrix_requests, df_matrix_machines, left_on="id_machine", right_on="id_machine", how='left')['penalty_machine'])
    #setting capacities
    a = pd.merge(df_matrix_requests, df_matrix_machines, left_on="id_machine", right_on="id_machine", how='left')
    capacities = np.array(a['size_machine']*a['nbr_machine'])
    # setting the distance matrix
    R = [1] + list(df_matrix_requests.id_location) + list(df_matrix_technician.id_location)
    d = []
    for i in range(len(R)):
        distance_row = []
        point_i = float(df_matrix_locations[df_matrix_locations.id_location==R[i]].x), float(df_matrix_locations[df_matrix_locations.id_location==R[i]].y)
        for j in range(len(R)):
            point_j = float(df_matrix_locations[df_matrix_locations.id_location==R[j]].x), float(df_matrix_locations[df_matrix_locations.id_location==R[j]].y)
            distance = np.sqrt((point_i[0]-point_j[0])**2 + (point_i[1]-point_j[1])**2)
            distance_row.append(distance)
        d.append(distance_row)
    d = np.array(d)
    
    objective_function = alpha*quicksum(m) + gamma*quicksum(v)
    objective_function += mu*quicksum(d[i,j]*x[i,j,k,t] for i in range(nbr_nodes) for j in range(nbr_nodes) for k in range(1,kmax+1) for t in range(1,nbr_days+1))
    objective_function += beta*quicksum(r) + kappa*quicksum(p)
    for techni_id in techni_set:
        list_nodes = [techni_id+nbr_requests] + techni_set[techni_id]
        objective_function += mu*quicksum(d[i,j]*z[i,j,techni_id,t] for i in list_nodes for j in list_nodes for t in range(1,nbr_days+1))
    objective_function += quicksum(tau[i-1]*b[i] for i in range(1, nbr_requests+1))
    model.setObjective(objective_function, GRB.MINIMIZE)
    
    
    ######################## Define the constraints ############################################
    # diagonals set to 0
    model.addConstrs(x[i,i,k,t] == 0 for i in range(nbr_nodes) for k in range(1,kmax+1) for t in range(1,nbr_days+1))
    model.addConstrs(z[i,i,s_s,t] == 0 for i in range(nbr_requests+nbr_technicians+1) for s_s in range(1,s+1) for t in range(1,nbr_days+1))

    model.addConstrs(quicksum(x[i,j,k,t] for i in range(nbr_nodes)) == quicksum(x[j,i,k,t] for i in range(nbr_nodes)) for j in range(nbr_nodes) for k in range(1,kmax+1) for t in range(1,nbr_days+1))
    model.addConstrs(quicksum(x[i,j,k,t]*d[i,j] for i in range(nbr_nodes) for j in range(nbr_nodes)) <= truck_max_distance for k in range(1, kmax+1) for t in range(1, nbr_days+1))
    model.addConstrs(q[j,k] <= q[i,k] - x[i,j,k,t]*(truck_capacity + capacities[j-1]) + truck_capacity for i in range(nbr_nodes) for j in range(1, nbr_requests+1) for k in range(1,kmax+1) for t in range(1, nbr_days+1))
    model.addConstrs(q[0,k] == truck_capacity for k in range(1, kmax+1))
    model.addConstrs(v[k,t] <= m[k] for k in range(1, kmax+1) for t in range(1, nbr_days+1))
    model.addConstrs(x[i,j,k,t] <= v[k,t] for i in range(nbr_nodes) for j in range(1, nbr_requests+1) for k in range(1, kmax+1) for t in range(1, nbr_days+1))
    for i in range(1, nbr_requests+1):
        first_day, last_day = df_matrix_requests.iloc[i-1,2], (df_matrix_requests.iloc[i-1,3])
        model.addConstr(quicksum(x[i,j,k,t] for j in range(nbr_nodes) for k in range(1,kmax+1) for t in range(first_day, last_day+1)) == 1)


    for techni_id in techni_set:
        list_nodes = [techni_id+nbr_requests] + techni_set[techni_id]
        d_s = df_matrix_technician.iloc[techni_id-1,2]
        n_s = df_matrix_technician.iloc[techni_id-1,3]
        model.addConstrs(quicksum(z[i,j,techni_id,t] for i in list_nodes) == quicksum(z[j,i,techni_id,t] for i in list_nodes) for j in list_nodes for t in range(1, nbr_days+1))
        model.addConstrs(quicksum(z[techni_id+nbr_requests,j,techni_id,t] for j in list_nodes if j!=techni_id+nbr_requests) == p[techni_id, t] for t in range(1, nbr_days+1))
        model.addConstrs(quicksum(d[i,j]*z[i,j,techni_id,t] for i in list_nodes for j in list_nodes) <= d_s for t in range(1, nbr_days+1))
        model.addConstrs(g[j,techni_id] <= g[i,techni_id] - z[i,j,techni_id,t]*(1+n_s)+n_s for i in list_nodes for j in range(1, nbr_requests+1) if j!=techni_id+nbr_requests for t in range(1, nbr_days+1))
        model.addConstr(g[techni_id+nbr_requests,techni_id] == n_s)
        model.addConstrs(p[techni_id, t] <= r[techni_id] for t in range(1,nbr_days+1))
        model.addConstrs(z[i,j,techni_id,t] <= p[techni_id,t] for i in range(nbr_nodes+nbr_technicians) for j in range(1,nbr_nodes+nbr_technicians) for t in range(1, nbr_days+1))
    for i in range(1, nbr_requests+1):
        first_day, last_day = df_matrix_requests.iloc[i-1,2], (df_matrix_requests.iloc[i-1,3])
        sum_all = 0
        for techni_id in techni_set:
            list_nodes = [techni_id+nbr_requests] + techni_set[techni_id]
            sum_all += quicksum(z[i,j,techni_id,t] for j in list_nodes for t in range(first_day+1, nbr_days+1))
        model.addConstr(sum_all == 1)

    model.addConstrs(quicksum(p[s_s,u] for u in range(t,t+5)) <= 5 - p[s,t+5] for s_s in range(1,s+1) for t in range(1, nbr_days-5+1))
    model.addConstrs(quicksum(p[s_s,u] for u in range(t,t+5)) <= 5 - p[s,t+6] for s_s in range(1,s+1) for t in range(1, nbr_days-6+1))
    for i in range(1, nbr_requests+1):
        first_day, last_day = df_matrix_requests.iloc[i-1,2], (df_matrix_requests.iloc[i-1,3])
        model.addConstrs(quicksum(p[s_s,u] for u in range(first_day+1,nbr_days)) <= 5 - p[s, nbr_days] for s_s in range(1,s+1))
    for i in range(1, nbr_requests+1):
        first_day, last_day = df_matrix_requests.iloc[i-1,2], (df_matrix_requests.iloc[i-1,3])
        sum_1 = 0
        for techni_id in techni_set:
            list_nodes = [techni_id+nbr_requests] + techni_set[techni_id]
            sum_1 += quicksum(z[i,j,techni_id,t]*t for j in list_nodes for t in range(first_day+1, nbr_days+1))
        sum_2 = quicksum(x[i,j,k,t]*t for j in range(nbr_nodes) for k in range(1,kmax) for t in range(first_day, nbr_days+1))
        model.addConstr(sum_1 - sum_2 - 1 == b[i])
        
        
    ##################### Optimizing Algorithm ###########################
    ############# The used algorithm is Branch and cut = branch and bound combined with cutting off planes ###################
    model.setParam('TimeLimit',time_limit)
    model.optimize()

    
    ####################### Writing results to txt file #######################
    lines_write = ['DATASET = '+dataset, 'NAME = '+dataset_name, '']

    for day in range(1, nbr_days+1):
        nbr_of_trucks = len([a for a in v if a[1] == day and v[a].x==1])
        out_trucks = [a for a in x if a[3] == day and x[a].x==1]
        out_trucks = sorted(out_trucks, key=lambda x: x[2])
        res_trucks = [list(v) for i, v in groupby(out_trucks, lambda x: x[2])]
        nbr_of_techni = len([a for a in p if a[1] == day and p[a].x==1])
        out_techni = [a for a in z if a[3] == day and z[a].x==1]
        out_techni = sorted(out_techni , key=lambda x: x[2])
        res_techni = [list(v) for i, v in groupby(out_techni, lambda x: x[2])]
        lines_write.append(f'DAY = {day}')
        lines_write.append(f'NUMBER_OF_TRUCKS = {nbr_of_trucks}')
        if res_trucks:
            for element in res_trucks:
                steps = [(a[0],a[1]) for a in element]
                lines_write.append(str(element[0][2]) +' '+' '.join('{}'.format(k) for k in return_path(steps, 0)))
        lines_write.append(f'NUMBER_OF_TECHNICIANS = {nbr_of_techni}')
        if res_techni:
            for element in res_techni:
                root = element[0][2] + nbr_requests
                steps = [(a[0],a[1]) for a in element]
                lines_write.append(str(element[0][2]) +' '+' '.join('{}'.format(k) for k in return_path(steps, root)))
        lines_write.append('')
    lines_write = lines_write[:-1]
    lines_write = [element+'\n' for element in lines_write]

    with open(filename[:-4]+"sol.txt", "w") as outfile:
        outfile.writelines(lines_write)
    
    
if __name__ == "__main__":
    main()
    
