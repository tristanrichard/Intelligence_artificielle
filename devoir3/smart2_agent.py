from agent import AlphaBetaAgent
import minimax
import copy
import math

"""
Agent skeleton. Fill in the gaps.
"""
class MyAgent(AlphaBetaAgent):
        
  """
  This is the skeleton of an agent to play the Tak game.
  """
  def get_action(self, state, last_action, time_left):
    self.last_action = last_action
    self.time_left = time_left
    self.depth = self.dept(state)
    return minimax.search(state, self)

  """
  The successors function must return (or yield) a list of
  pairs (a, s) in which a is the action played to reach the
  state s.
  """
  def successors(self, state):
    actions = state.get_current_player_actions()
    action_sort = sorted(actions,key=lambda action: self.filter1(action,state),reverse=True)
    lst=[]
    for i in action_sort:
        s = copy.deepcopy(state)
        s.apply_action(i)
        lst.append((i, s))
    return lst


  def filter1(self,action,state):
    s=0
    if action[0] is None or action[1] is None or state.is_action_valid(action):
        return s
    x,y = state.cur_pos[self.id][action[0]]
    if action[1] == "EAST":
        x+=1
    if action[1] == "NORTH":
        y+=1
    if action[1] == "SOUTH":
        y-=1
    if action[1] == "WEST":
        x-=1
    val3 = list(state.adj_bridges_pos((x,y)).values())
    val4 = list(state.adj_pawns_pos((x,y)).values())
    for i in range(4):
        if val3[i]==True and val4[i]==False:
            s+=1
    return s




  """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """
  def cutoff(self, state, depth):
    return bool(state.game_over() or depth>=self.depth)

  def dept(self,state):
    s=0
    for i in range(3):
      dic_adj_bridg = state.adj_bridges(self.id,i)
      for key, value in dic_adj_bridg.items():
        if value==True:
          s +=1
    print(s)
    if s<=10:
        return 3
    elif s<=4:
        return 4
    else:
        return 2

  """
  The evaluate function must return an integer value
  representing the utility function of the board.
  idée: maximiser le nombre de pont pres de moi et minimiser le nombre de pont près de lui
  """
  def evaluate(self, state):
    s = 0
    #maximiser le nombre de possibilité de mouvement pres de moi et minimiser le nombre de possibilité de momuvement près de lui, sur deux actions
    for pawn in range(3):
      x,y = state.cur_pos[self.id][pawn]#position du pion
      dic_adj_bridg = state.adj_bridges_pos((x,y))
      dic_adj_pawn = state.adj_pawns_pos((x,y))
      for key,val1 in dic_adj_bridg.items():
        newx,newy=x,y
        val2=dic_adj_pawn[key]
        if val1==False or val2==True:#pas de mouvement possible
            s-=1
        else:
            if key == "EAST":
                newx+=1
            elif key == "NORTH":
                newy+=1
            elif key == "SOUTH":
                newy-=1
            elif key == "WEST":
                newx-=1
            val3 = list(state.adj_bridges_pos((x,y)).values())
            val4 = list(state.adj_pawns_pos((x,y)).values())
            for i in range(4):
                if val3[i]==True and val4[i]==False:
                    s+=0.5

    for pawn in range(3):
        x,y = state.cur_pos[1-self.id][pawn]#position du pion
        dic_adj_bridg = state.adj_bridges_pos((x,y))
        dic_adj_pawn = state.adj_pawns_pos((x,y))
        for key,val1 in dic_adj_bridg.items():
            newx,newy=x,y
            val2=dic_adj_pawn[key]
            if val1==False or val2==True:#pas de mouvement possible
                s+=3
            else:
                if key == "EAST":
                    newx+=1
                elif key == "NORTH":
                    newy+=1
                elif key == "SOUTH":
                    newy-=1
                elif key == "WEST":
                    newx-=1
                val3 = list(state.adj_bridges_pos((x,y)).values())
                val4 = list(state.adj_pawns_pos((x,y)).values())
                for i in range(4):
                    if val3[i]==True and val4[i]==False:
                        s-=1.4
    return s