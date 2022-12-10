import sys
from Agent import Agent
from GameBoard import GameBoard
import numpy as np


class MiniMaxAgent(Agent):
  def init(self):
    pass

  def play(self, board:GameBoard):
    return self.getBestMove(board)

  def heuristic_utility(self, board: GameBoard):
    return self.mixedHeuristic(board, 2)
    # return self.max_sq_coef_sum(board, 2)

  def mixedHeuristic(self, board: GameBoard, weight: int):
    count = 0
    sum = 0
    smoothness = 0
    for i in range(4):
      for j in range(4):
        if i < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i + 1][j])
        if j < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i][j + 1])
        sum += board.grid[i][j] ** 2
        if board.grid[i][j] != 0:
          count += 1
    snoes = int(sum/count)
    smoothness = smoothness ** weight
    return snoes / smoothness
  
  def max_coef(self, board: GameBoard, weight: int):
    count = 0
    sum = 0
    max = 0
    smoothness = 0
    for i in range(4):
      for j in range(4):
        if i < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i + 1][j])
        if j < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i][j + 1])
        sum += board.grid[i][j] ** 2
        if board.grid[i][j] > max:
          max = board.grid[i][j]
        if board.grid[i][j] != 0:
          count += 1
    snoes = int(sum/count)
    smoothness = smoothness ** weight
    return (snoes / smoothness) + (max / 2048)
  
  def max_sq_coef(self, board: GameBoard, weight: int):
    count = 0
    sum = 0
    max = 0
    smoothness = 0
    for i in range(4):
      for j in range(4):
        if i < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i + 1][j])
        if j < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i][j + 1])
        sum += board.grid[i][j] ** 2
        if board.grid[i][j] ** 2 > max:
          max = board.grid[i][j] ** 2
        if board.grid[i][j] != 0:
          count += 1
    snoes = int(sum/count)
    smoothness = smoothness ** weight
    return (snoes / smoothness) + (max / (2048**2))

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
  
  def max_sq_coef_sum_col(self, board: GameBoard, weight: int):
    count = 0
    sum_sq = 0
    sum = 0
    max = 0
    pos = []
    smoothness = 0
    for i in range(4):
      for j in range(4):
        if i < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i + 1][j])
        if j < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i][j + 1])
        sum_sq += board.grid[i][j] ** 2
        sum+= board.grid[i][j]
        pos.append(board.grid[i][j])
        if board.grid[i][j] ** 2 > max:
          max = board.grid[i][j] ** 2
        if board.grid[i][j] != 0:
          count += 1
    snoes = int(sum_sq/count)
    smoothness = smoothness ** weight
    fil0 = (pos[0] >= pos[4] and pos[4] >= pos[8] and pos[8] >= pos[12]) or (pos[0] <= pos[4] and pos[4] <= pos[8] and pos[8] <= pos[12])
    fil1 = (pos[1] >= pos[5] and pos[5] >= pos[9] and pos[9] >= pos[13]) or (pos[1] <= pos[5] and pos[5] <= pos[9] and pos[9] <= pos[13])
    fil2 = (pos[2] >= pos[6] and pos[6] >= pos[10] and pos[10] >= pos[14]) or (pos[2] <= pos[6] and pos[6] <= pos[10] and pos[10] <= pos[14])
    fil3 = (pos[3] >= pos[7] and pos[7] >= pos[11] and pos[11] >= pos[15]) or (pos[3] <= pos[7] and pos[7] <= pos[11] and pos[11] <= pos[15])
    col0 = (pos[0] >= pos[1] and pos[1] >= pos[2] and pos[2] >= pos[3]) or (pos[0] <= pos[1] and pos[1] <= pos[2] and pos[2] <= pos[3])
    col1 = (pos[4] >= pos[5] and pos[5] >= pos[6] and pos[6] >= pos[7]) or (pos[4] <= pos[5] and pos[5] <= pos[6] and pos[6] <= pos[7])
    col2 = (pos[8] >= pos[9] and pos[9] >= pos[10] and pos[10] >= pos[11]) or (pos[8] <= pos[9] and pos[9] <= pos[10] and pos[10] <= pos[11])
    col3 = (pos[12] >= pos[13] and pos[13] >= pos[14] and pos[14] >= pos[15]) or (pos[12] <= pos[13] and pos[13] <= pos[14] and pos[14] <= pos[15])
    ordered = 0
    if fil0: ordered += 1
    if fil1: ordered += 1
    if fil2: ordered += 1
    if fil3: ordered += 1
    if col0: ordered += 1
    if col1: ordered += 1
    if col2: ordered += 1
    if col3: ordered += 1

    return (snoes / smoothness) + (max / (2048**2)) + (sum / 4096) + (ordered / 64)

  def maxi(self, board: GameBoard, a: int, b: int, d: int):
    (maxChild, maxUtility, moveFrom) = (None, (-1) * sys.maxsize, -1)

    if self.algorithmHasEnded("max", board, d):
      return (None, self.heuristic_utility(board), moveFrom)
    
    d -= 1

    possibleMoves = board.get_available_moves()
    possibleMoves.sort()
    
    for child in possibleMoves:
      grid = board.clone()
      grid.move(child)
      (_, utility) = self.mini(grid, a, b, d)
      if utility > maxUtility:
        (maxChild, maxUtility, moveFrom) = (grid, utility, child)
      if maxUtility >= b:
        break
      if maxUtility > a:
        a = maxUtility

    return (maxChild, maxUtility, moveFrom)

  def mini(self, board: GameBoard, a: int, b: int, d: int):
    (minChild, minUtility) = (None, sys.maxsize)

    if self.algorithmHasEnded("min", board, d):
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
    
    for child in childrens:
      grid = board.clone()
      grid.insert_tile(child[0], child[1])
      (_, utility, _) = self.maxi(grid, a, b, d)
      if utility < minUtility:
        (minChild, minUtility) = (grid, utility)
      if minUtility <= a:
        break
      if minUtility < b:
        b = minUtility

    return (minChild, minUtility)

  def getBestMove(self, board: GameBoard, d: int = 7):
    clone = board.clone()
    (child, _, moveFrom) = self.maxi(clone, (-1) * sys.maxsize, sys.maxsize, d)
    return moveFrom
  
  def algorithmHasEnded(self, who: str, board: GameBoard, d: int):
    if d == 0:
      return True
    if who == 'max':
      return len(board.get_available_moves()) == 0
    else:
      return len(board.get_available_cells()) == 0