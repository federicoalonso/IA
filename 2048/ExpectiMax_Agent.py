import sys
from Agent import Agent
from GameBoard import GameBoard
import numpy as np


class ExpectiMax_Agent(Agent):
  def init(self):
    pass

  def play(self, board:GameBoard):
    return self.getBestMove(board)

  def heuristic_utility(self, board: GameBoard):
    return self.max_sq_coef_sum(board, 2)

  def max_sq_coef_sum(self, board: GameBoard, weight: int):
    count = 0
    sum_sq = 0
    sum = 0
    max = 0
    smoothness = 0
    for i in range(4):
      for j in range(4):
        if i < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i + 1][j])
        if j < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i][j + 1])
        sum_sq += board.grid[i][j] ** 2
        sum+= board.grid[i][j]
        if board.grid[i][j] ** 2 > max:
          max = board.grid[i][j] ** 2
        if board.grid[i][j] != 0:
          count += 1
    snoes = int(sum_sq/count)
    smoothness = smoothness ** weight
    return (snoes / smoothness) + (max / (2048**2)) + (sum / 4096)

  def maxi(self, board: GameBoard, d: int):
    (maxChild, maxUtility, moveFrom) = (None, (-1) * sys.maxsize, -1)

    if self.algorithmHasEnded("max", board, d):
      return (None, self.heuristic_utility(board), moveFrom)
    
    d -= 1

    possibleMoves = board.get_available_moves()
    possibleMoves.sort()
    
    for child in possibleMoves:
      grid = board.clone()
      grid.move(child)
      (_, utility) = self.expecti(grid, d)
      if utility > maxUtility:
        (maxChild, maxUtility, moveFrom) = (grid, utility, child)

    return (maxChild, maxUtility, moveFrom)

  def expecti(self, board: GameBoard, d: int):
    (minChild, maxUtility) = (None, sys.maxsize)

    if self.algorithmHasEnded("expecti", board, d):
      return (None, self.heuristic_utility(board))

    d -= 1

    emptyCells = board.get_available_cells()

    ## Cut
    # if len(emptyCells) >= 6 and d <= 3:
    #   return (None, self.heuristic_utility(board))
    if len(emptyCells) >= 6 and d <= 2:
      return (None, self.heuristic_utility(board))

    childrens = []

    for cell in emptyCells:
      childrens.append((cell, 2))
      childrens.append((cell, 4))
    
    childrens.sort()
    tot_utility = 0

    posibility_2 = 0.9 * 1 / len(emptyCells)
    posibility_4 = 0.1 * 1 / len(emptyCells)
    
    for child in childrens:
      grid = board.clone()
      num = child[1]
      grid.insert_tile(child[0], child[1])
      (_, utility, _) = self.maxi(grid, d)
      if num == 2:
        utility = utility * posibility_2
      else:
        utility = utility * posibility_4

      tot_utility += utility

    return (None, tot_utility)

  def getBestMove(self, board: GameBoard, d: int = 5):
    clone = board.clone()
    (child, _, moveFrom) = self.maxi(clone, d)
    return moveFrom
  
  def algorithmHasEnded(self, who: str, board: GameBoard, d: int):
    if d == 0:
      return True
    if who == 'max':
      return len(board.get_available_moves()) == 0
    else:
      return len(board.get_available_cells()) == 0