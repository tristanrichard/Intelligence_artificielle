from search import *
from copy import copy
import time


#################
# Problem class #
#################

class SoftFlow(Problem):

    def __init__(self, initial):
        self.initial=initial
        self.goal_t=initial.goal#permet de verifier que le state est le meilleur state, autrement dit des qu'on a trouvé un cable on itere que sur les states avec ce cable resolu
        
    def cityblock(self,a,b):
        """
        

        Parameters
        ----------
        a : vecteur1
            
        b : vecteur2

        Returns
        -------
        la distance entre les deux vecteurs

        """
        return sum(abs(pi - qi) for pi, qi in zip(a, b))
        
        
    def actions(self, state):
        if(self.goal_t!=state.goal):#verifie que le state est le meilleur state
            return []
        mouvement = [[1,0],[0,-1],[0,1],[-1,0]]
        state.pos_cable
        action = []
        state.i+=1
        for k in range(len(state.pos_cable)):
            if(state.goal[k]==True):#on ne fait plus d'action sur un cable fini
                pass
            (x,y) = state.pos_cable[k]
            for [i, j] in mouvement:
                new_x = x + i
                new_y = y + j
                if ((state.grid[new_x][new_y] == ' ' or state.grid[new_x][new_y]==state.cable[k]) and new_x < state.nbr and new_y < state.nbc):#permet de verfiier si la nouvelle position est valide
                    if(state.i>1 and (new_x == state.old_pos[k][0] and new_y == state.old_pos[k][1])):#ici on verifie qu'on ne revient pas sur nos pas
                        pass
                    else:
                        action.append((new_x, new_y,k,x,y))
        return action
    
    def result(self, state, action):
        new_grid = []
        pos_cable=copy(state.pos_cable)
        old_pos=copy(state.old_pos)
        goal=copy(state.goal)
        #cope de la grille
        for i in range(len(state.grid)):
            new_grid.append([])
            for j in range(len(state.grid[0])):
                new_grid[i].append(state.grid[i][j])
                
        new_row, new_column, cable_num, old_x, old_y = action
        (i,j) = state.sol.get(str(state.cable[cable_num]))
        #on verifie que la cable est pas lié
        for [k,l] in  [[1,0],[0,-1],[0,1],[-1,0]]:
            if(state.i>1 and not(new_row+k == state.old_pos[cable_num][0] and new_column+l == state.old_pos[cable_num][1])):
                if new_row+k==i and new_column+l==j:#fini
                    #print("fini" + str(state.cable[cable_num]))
                    new_grid[old_x][old_y]=state.cable[cable_num]
                    new_grid[new_row][new_column]=state.cable[cable_num]
                    goal[cable_num]=True
                    self.goal_t[cable_num]=True 
                    return State(new_grid,state.cable,pos_cable,old_pos,goal,state.sol,state.i)
        #si pas fini on continue alors
        char = state.grid[old_x][old_y]
        new_grid[old_x][old_y] = state.cable[cable_num]
        new_grid[new_row][new_column]=char
        pos_cable[cable_num]=(new_row,new_column)
        old_pos[cable_num]=(old_x,old_y)
        return State(new_grid,state.cable,pos_cable,old_pos,goal,state.sol,state.i)    
                                
        
    def goal_test(self, state):
        #il faut que tous les cables soient termimnés
        for i in range(len(state.goal)):
            if(state.goal[i]==False):
                return False
        return True

    def h(self, node):
        h=0
        #for k in range(len(node.state.cable)):
            #h+=self.cityblock(node.state.pos_cable[k],node.state.sol.get(str(node.state.cable[k])))#simple distance entre vecteurs
        return h
        

    def load(path):
        with open(path, 'r') as f:
            lines = f.readlines()
            
        state = State.from_string(''.join(lines))
        return SoftFlow(state)



###############
# State class #
###############

class State:

    def __init__(self, grid,cable,pos_cable,old_pos,goal,sol,i=0):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.cable = cable#contient tous les cables qu'il y a sur la map
        self.pos_cable = pos_cable
        self.old_pos = old_pos
        self.goal = goal
        self.i=i
        self.sol=sol
        
    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)
    
    def lst_tuple(self):
        list = []
        for i in range(len(self.grid)):
            list.append(tuple(self.grid[i]))
        return tuple(list)

    def __eq__(self, other_state):
        return  self.lst_tuple() == other_state.lst_tuple() and isinstance(other_state, State)

    def __hash__(self):
        return hash(self.lst_tuple())
    
    def __lt__(self, other):
        return hash(self) < hash(other)

    def from_string(string):
        lines = string.strip().splitlines()
        init = list(map(lambda x: list(x.strip()), lines))
        num=0
        pos_cable=[]
        goal=[]
        cable=[]
        old_pos=[]
        sol={}
        for i in range(len(init)):
            for j in range(len(init[0])):
                if (init[i][j] != " " and init[i][j]!= "#" and (init[i][j].isalpha())):
                    pos_cable.append((i,j))
                    old_pos.append((i,j))
                    num+=1
                    goal.append(False)
                    code_ascii_a = ord('a')
                    code_ascii_caractere = ord(init[i][j])
                    nombre_equivalent = code_ascii_caractere - code_ascii_a
                    code_ascii_0 = ord('0')
                    code_ascii_caractere_nombre = code_ascii_0 + nombre_equivalent
                    caractere_nombre = chr(code_ascii_caractere_nombre)
                    cable.append(caractere_nombre)
                elif (init[i][j] != " " and init[i][j]!= "#" and (init[i][j].isdigit())):
                    sol[init[i][j]]=(i,j)
        return State(init,cable,pos_cable,old_pos,goal,sol)






#####################
# Launch the search #
#####################

problem = SoftFlow.load(sys.argv[1])

t0 = time.time()
node,l = astar_search(problem)
t1=time.time()



path = node.path()


for n in path:
    print(n.state)  # assuming that the _str_ function of state outputs the correct format
    print()
print('Number of moves: ', str(node.depth))
print("Temps d'exécution : ", t1 - t0, "s")
print('Number of nodes: ',l )