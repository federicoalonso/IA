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
    ## La suma de todos los números, sobre el número de lugares no vacíos.
    # sumNumbersOverEmptySpaces = self.sumNumbersOverEmptySpaces(board)
    # smoothness = self.smoothness(board, 2)
    # highestTile = self.highestTile(board)
    # print('\nsumNumbersOverEmptySpaces: "{}"'.format(sumNumbersOverEmptySpaces),
    #       '\nsmoothness: "{}"'.format(smoothness),
    #       '\nhighestTile: "{}"'.format(highestTile))

    # return 100 * sumNumbersOverEmptySpaces + 1 * smoothness # + 5000 * highestTile
    return self.mixedHeuristic(board, 2)

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
  
  def sumNumbersOverEmptySpaces(self, board: GameBoard):
    """
    Favorece la mayor suma, penalizando por los lugares vacíos
    """
    count = 0
    sum = 0
    for i in range(4):
      for j in range(4):
        sum += board.grid[i][j]
        if board.grid[i][j] != 0:
          count += 1
    return int(sum/count)
  
  def smoothness(self, board: GameBoard, weight: int):
    """
    - Calcular el \"smoothness\" del tablero. Esto es porque cuanto mas \"smooth\" el tablero, mas facil es juntar fichas. Para ello debemos:
        - Aplicar la raiz cuadrada al tablero
                - Sumar la diferencia entre cada casilla y la de abajo
                - Sumar la diferencia entre cada casilla y la de la derecha
                - Elevar este resultado a un smoothness_weight a determinar
                - Multiplicar por -1
    """
    smoothness = 0
    for i in range(4):
      for j in range(4):
        smoothness += np.sqrt(board.grid[i][j])
        if i < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i + 1][j])
        if j < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i][j + 1])
    smoothness ** weight
    return smoothness * (-1)
  
  def highestTile(self, board: GameBoard):
    """
    Prefiere que el númer aumente ante el resto
    """
    return board.get_max_tile()

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

  def getBestMove(self, board: GameBoard, d: int = 6):
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