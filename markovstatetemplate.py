from collections import namedtuple
from random import choice, choices


# TODO : Change cnn_observation_space, fcn_observation_space, action_space, players
# TODO : fill in all "Your Code Here"


class MarkovState(namedtuple("MarkovStateTemplate", 
field_names=("cnn","fcn","info","turn","terminal","winners"), 
defaults=([[]], [], [], 0, False, []))):
  """
  A class that inherits namedtuple and uses itself as a state,
  added functions are for handling state

  A stochastic process has the Markov property
  if the conditional probability distribution of future states of the process
  depends only upon the present state;
  that is, given the present, the future does not depend on the past.

  ex) in world of super mario
  if env(or state) is composed only of coordinate data it does not have a Markov property!
  if env(or state) is composed coordinate + speed data it has Markov property!
  (Coordinate alone cannot predict the result of the current action & Speed embeds data of past accelerations)
  """

  # for Neural Network (Deep Q-Network?)
  # cnn_observation_space = cnn input size = (depth, height, width)
  #   ex) rgb 720p = (depth = 3, height = 720, width = 1280)
  # fcn_observation_space = fcn input size
  # action_space = output size
  cnn_observation_space = (1, 17, 17)
  fcn_observation_space = 12
  action_space = 0

  # for reinforcement learning
  # players = number of agents
  players = 0

  def get_cnn_observation(self):
    """from self.env make cnn input for nn"""
    # cnn_observations = [[] for __ in range(MarkovState.players)]
    cnn_observations = []
    # ========== Your Code Here ==========#
    curr_env = self.cnn
    # ====================================#
    return cnn_observations

  def get_fcn_observation(self):
    """from self.env make fcn input for nn"""
    # fcn_observations = [[] for __ in range(MarkovState.players)]
    fcn_observations = []
    # ========== Your Code Here ==========#
    curr_env = self.fcn
    # ====================================#
    return fcn_observations

  def get_actions(self):
    """Actions that curr agent can take"""
    actions = []
    # ========== Your Code Here ==========#
    actions = [1, 3, 5, 7, 9]
    # ====================================#
    return actions

  def _get_roll(self, action, all_roll=False):
    """Returns the probabilistic outcome of action"""
    """
    if all_roll == True : return all roll
    else : return random roll
    """
    if action not in range(MarkovState.action_space):
      raise ValueError
    roll_prob = []
    # ========== Your Code Here ==========#
    roll_prob = [[1, 2, 3, 4, 5, 6], [1, 1, 1, 1, 1, 1]]
    # ====================================#
    if all_roll:
      return roll_prob[0]
    else:
      return choices(population=roll_prob[0], weights=roll_prob[1])

  def _step(self, action, roll):
    """Returns the next MrokovState that is the result of action and roll"""
    # Action = The smallest unit of movement that the agent can select
    # roll = Probabilistic outcome of agent's Action
    # ex) Action = CoinToss, roll = (front, back)
    next_environment = []
    next_turn = 0
    next_terminal = False
    next_winners = []
    # ========== Your Code Here ==========#

    # ====================================#
    return MarkovState(set(next_environment), next_turn, next_terminal, next_winners)

  def get_children(self):
    """Return all MrokovState that is the result of action"""
    # in deterministic world, action can have only one outcome.
    # in stochastic world, action can have multiple outcome.
    # The action of rolling the dice has a result of 1-6.
    children = dict()
    for action in self.get_actions():
      rolls = self._get_roll(action, all_roll=True)
      children[action] = {roll: self._step(action, roll) for roll in rolls}
    return children

  def take_action(self, action):
    """get next state that is the result of action"""
    # get next state in stochastic world
    actions = self.get_actions()
    if action not in actions:
      action = choice(actions)
    return self._step(action, self._get_roll(action, all_roll=False))

  def get_turn(self):
    """return turn"""
    return self.turn

  def is_terminal(self):
    """return True if terminal (game over) else False"""
    return self.terminal

  def get_rewards(self):
    """return reward for each player"""
    """
    Reward Clipping
      The rewards obtained from the environment vary in scale depending on the environment. 
      For example, in the Atari game Pong, you score 1 point for each freeze, 
      and in Space Invaders, you score 10 to 30 points for each enemy you defeat.
      
      In DQN, to compensate for this, the parent scale is fixed at -1, 0, and 1 in all environments. 
      This allows learning to be performed using the same hyperparameters regardless of the environment.
        
    because of this reward should be -1, 0 or 1.
    """
    # game over and not draw
    if self.terminal and self.winners:
      return (1 if pidx in self.winners else -1 for __ in range(MarkovState.players))
    else:
      return (0 for __ in range(MarkovState.players))
