#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Auguste Burlats <auguste.burlats@uclouvain.be>"""
from search import *
import time


class AtomPlacement(Problem):

    #retourne les états possibles
    def successor(self, state):
        new_state = []
        for i in range(len(state.sites)):
            for j in range(i+1, len(state.sites)):
                new_lst = state.sites.copy()
                new_lst[i], new_lst[j] = new_lst[j], new_lst[i]
                new_state.append((0,State(state.n_sites,state.n_types,state.edges,state.energy_matrix,sites=new_lst)))#modifier state.edge pas que sites car les edges bougent
        return new_state

    #calcule la somme des edges
    def value(self, state):
        s=0
        #print(state.sites)
        for i in range(state.n_edges):
            noeud1=state.sites[state.edges[i][0]]
            noeud2=state.sites[state.edges[i][1]]
            s+=state.energy_matrix[noeud1][noeud2]
        #print(s)
        return s


class State:

    def __init__(self, n_sites, n_types, edges, energy_matrix, sites=None):
        self.k = len(n_types)
        self.n_types = n_types
        self.n_sites = n_sites
        self.n_edges = len(edges)
        self.edges = edges
        self.energy_matrix = energy_matrix
        if sites is None:
            self.sites = self.build_init()
        else:
            self.sites = sites

    # an init state building is provided here but you can change it at will
    def build_init(self):
        sites = []
        for atom_type, quantity in enumerate(self.n_types):
            for i in range(quantity):
                sites.append(atom_type)

        return sites

    def __str__(self):
        s = ''
        for v in self.sites:
            s += ' ' + str(v)
        return s


def read_instance(instanceFile):
    file = open(instanceFile)
    line = file.readline()
    n_sites = int(line.split(' ')[0])
    k = int(line.split(' ')[1])
    n_edges = int(line.split(' ')[2])
    edges = []
    file.readline()

    n_types = [int(val) for val in file.readline().split(' ')]
    if sum(n_types) != n_sites:
        print('Invalid instance, wrong number of sites')
    file.readline()

    energy_matrix = []
    for i in range(k):
        energy_matrix.append([int(val) for val in file.readline().split(' ')])
    file.readline()

    for i in range(n_edges):
        edges.append([int(val) for val in file.readline().split(' ')])

    return n_sites, n_types, edges, energy_matrix


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100,callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    beststep=0
    for i in range(100):
        if callback is not None:
            callback(current)
        voisins = []
        for s in list(current.expand()):
            voisins.append(s)
        voisins = sorted(voisins, key=lambda node: node.value())[:5]
        noeud = voisins[0]
        if noeud.value() < best.value():
            best = noeud
            beststep=i
        current=noeud
    return best,beststep


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=200,callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    beststep=0
    for i in range(100):
        #print(best)
        #print(best.value())
        if callback is not None:
            callback(current)
        voisins = []
        for s in list(current.expand()):
            voisins.append(s)
        voisins = sorted(voisins, key=lambda node: node.value())[:5]
        noeud = random.choice(voisins)#on choisit un aléatoire
        #print("noeud= "+ str(noeud))
        #print(noeud.value(),best.value())
        if noeud.value() < best.value():
            best = noeud
            beststep=i
        #print("best= "+str(best))
        current=noeud
    return best,beststep


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1], info[2], info[3])
    ap_problem = AtomPlacement(init_state)
    step_limit = 100


    start = time.perf_counter()
    node,step_max = maxvalue(ap_problem, step_limit)
    end = time.perf_counter()
    time_maxval = end-start
    val_maxval = node.value()


    total_time= 0
    total_steps= 0
    total_value = 0
    for i in range(10):

        start = time.perf_counter()
        node,step = randomized_maxvalue(ap_problem, step_limit)
        end = time.perf_counter()
        time_spent = end - start
        total_time += time_spent
        total_value += node.value()
        total_steps += step

    total_time = total_time / 10
    total_value = int(total_value / 10)
    total_steps = total_steps/10

    total_time_2 = 0
    total_steps_2 = 0
    total_value_2 = 0
    for i in range(10):
        start = time.perf_counter()
        node,step = random_walk(ap_problem, step_limit)
        end = time.perf_counter()
        time_spent = end - start
        total_time_2 += time_spent
        total_value_2 += node.value()
        total_steps_2 += step

    total_time_2 = total_time_2 / 10
    total_value_2 = total_value_2 / 10
    total_steps_2 = total_steps_2 / 10
    print(" max: time=  " + str(time_maxval) + " val= "+ str(val_maxval) + " step= "+ str(step_max)  + " random_max: time= " + str(total_time) + " val= " + str(total_value) + " step= " + str(total_steps) +  "random_walk:time= " + str(total_time_2) + "val= " + str(total_value_2) + " step= " + str(total_steps_2) +"\\\\")
