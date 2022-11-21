import sys
from Agent import Agent
from GameBoard import GameBoard

class MiniMaxAgent(Agent):
  def init(self):
    pass

  def play(self, board:GameBoard):
    return self.getBestMove(board)

  def heuristic_utility(self, board: GameBoard):
    return self.mixedHeuristic_4(board, 3)
  
  # Sólo favorecemos abajo a la derecha
  def mixedHeuristic_5(self, board: GameBoard, weight: int):
    posVal = 0
    for i in range(4):
      for j in range(4):
        pos = 4 * (i % 4) + j
        if pos < 4:
          pos = 3 - pos
        elif pos > 7 and pos <= 11:
          pos = 11 - pos + 8
        posVal += board.grid[i][j] * pos
    return posVal

  # El mismo mixto, pero favorecemos los valores altos hacia abajo a la derecha
  def mixedHeuristic_4(self, board: GameBoard, weight: int):
    count = 0
    sum = 0
    smoothness = 0
    posVal = 0
    for i in range(4):
      for j in range(4):
        pos = 4 * (i % 4) + j
        if pos < 4:
          pos = 3 - pos
        elif pos > 7 and pos <= 11:
          pos = 11 - pos + 8
        posVal += board.grid[i][j] * pos
        if i < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i + 1][j])
        if j < 3:
          smoothness += abs(board.grid[i][j] - board.grid[i][j + 1])
        sum += board.grid[i][j] ** 2
        if board.grid[i][j] != 0:
          count += 1
    snoes = int(sum/count)
    smoothness = smoothness ** weight
    return (snoes / smoothness) + posVal
  
  # Sin smooth
  def mixedHeuristic_3(self, board: GameBoard, weight: int):
    count = 0
    sum = 0
    for i in range(4):
      for j in range(4):
        sum += board.grid[i][j] ** 2
        if board.grid[i][j] != 0:
          count += 1
    snoes = int(sum/count)
    return snoes

  # Favorecemos el smooth
  def mixedHeuristic_2(self, board: GameBoard, weight: int):
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
    return (-1) * smoothness + snoes

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

  def getBestMove(self, board: GameBoard, d: int = 4):
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