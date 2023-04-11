#!/usr/bin/env python3
"""
Name of the author(s):
- Auguste Burlats <auguste.burlats@uclouvain.be>
"""
import time
import sys
from copy import deepcopy
from search import *


#################
# Problem class #
#################
class TowerSorting(Problem):
    
    def actions(self, state):
        
        """Return the actions that can be executed in the given state"""

        actions = []
        for nb_old_tower in range(len(state.grid)):
            tower = state.grid[nb_old_tower]
            if(len(tower) != 0) :
                for nb_new_tower in range(len(state.grid)) :
                    othertower = state.grid[nb_new_tower]
                    if(tower != othertower and len(othertower) != state.size):
                        actions.append(tuple([nb_old_tower,nb_new_tower,tower[len(tower)-1]])) #tuple avec (ancienne_tour,nouvelle_tour,valeur)
        return actions

    def result(self, state, action):

        """Return the state that results from executing the given
        action in the given state."""
                
        new_state = [[] for i in range(state.number)]
        for i in range(len(state.grid)) :
            for j in range(len(state.grid[i])) :
                new_state[i].append(state.grid[i][j])

        new_state[action[0]].pop()
        new_state[action[1]].append(action[2])

        #----------- Changement en tuple ---------------#

        new_tuple = []
        for tower in new_state :
            new_tuple.append(tuple(tower))

        return State(state.number,state.size,tuple(new_tuple),"tower {0} -> tower {1}".format(action[0], action[1]))

    def goal_test(self, state):
        
        """Return True if the state is a goal."""
        
        return state == self.goal

        


###############
# State class #
###############
class State:

    def __init__(self, number, size, grid, move="Init"):
        self.number = number
        self.size = size
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for i in reversed(range(self.size)):
            for tower in self.grid:
                if len(tower) > i:
                    s += "".join(tower[i]) + " "
                else:
                    s += ". "
            s += "\n"
        return s

    def __eq__(self, other):
        return hash(self)==hash(other) #compare les deux hash, retourne true s'ils sont identiques

    def __hash__(self):
        sorted_grid = sorted(self.grid) #on trie les colonnes dans l'ordre

         #----------- Changement en tuple ---------------#
         # On a besoin d'un élement hashable pour créer un hash, sauf qu'une liste ne l'est pas,
         # donc on transforme le tout en tuple qui lui est hashable

        tuple_grid = []
        for tower in sorted_grid :
            tuple_grid.append(tuple(tower))

        return hash(tuple(sorted_grid))


######################
# Auxiliary function #
######################
def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    number_tower, size_tower = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = [[] for i in range(number_tower)] 
    for row in lines[1:size_tower+1]:
        elems = row.split(" ")
        for index in range(number_tower):
            if elems[index] != '.':
                initial_grid[index].append(elems[index])

    initial_grid2 = []
    for tower in initial_grid:
        tower.reverse()
        initial_grid2.append(tuple(tower))

    return number_tower, size_tower, initial_grid2 

def final_state(state,number,max_size,title = "Goal"): # Fonction qui retourne l'état final
    new_list = []
    for tower in state.grid :
        for elem in tower :
            new_list.append(elem) # On crée une liste de tous les éléments

    sorted_list = sorted(new_list) # On trie cette liste

    goal_state = [[] for i in range(number)]

    actual_size = 0
    current_tower = 0
    for elem in range (0,len(sorted_list)):
        goal_state[current_tower].append(sorted_list[elem]) # on ajoute les éléments dans les tours
        actual_size += 1                                    # puisqu'ils sont triés, on aura bien
        if (actual_size == max_size):                       # les mêmes éléments dans une même tour
            current_tower += 1
            actual_size = 0

    #----------- Changement en tuple ---------------#

    tuple_goal_state = []
    for tower in goal_state :
        tuple_goal_state.append(tuple(tower))

    return State(number,max_size,tuple(tuple_goal_state),title)


if _name_ == "_main_":
    if len(sys.argv) != 2:
        print(f"Usage: ./sort_tower.py <path_to_instance_file>")
    filepath = sys.argv[1]

    number, size, initial_grid = read_instance_file(filepath)

    init_state = State(number, size, tuple(initial_grid), "Init")
    goal_state = final_state(init_state,number,size) #on ajoute l'objectif final
    problem = TowerSorting(init_state,goal_state)
    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the _str_ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)