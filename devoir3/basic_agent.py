from agent import AlphaBetaAgent
import minimax

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
    return minimax.search(state, self)

  """
  The successors function must return (or yield) a list of
  pairs (a, s) in which a is the action played to reach the
  state s.
  """
  def successors(self, state):
    action = state.get_current_player_actions()
    lst=[]
    for i in action:
        s = state.copy()
        s.apply_action(action)
        lst.append((action, s))
    return lst

  """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """
  def cutoff(self, state, depth):
    return bool(state.game_over() or depth>=1)

  """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """
  def evaluate(self, state):
    r=0
    opponent = 1-self.id
    for i in range(len(state.cur_pos[1])):
          bridge = state.adj_bridges(opponent,i)
          for j in bridge.values():
                if j==False:
                      r+=1
    return r