from datetime import datetime
from GameBoard import GameBoard
from Agent import Agent
# from Random_Agent import RandomAgent
from MiniMax_Agent import MiniMaxAgent
# from MiniMax_Agent_2 import MiniMaxAgent
import logging

def check_win(board: GameBoard):
    return board.get_max_tile() >= 2048


int_to_string = ['UP', 'DOWN', 'LEFT', 'RIGHT']

if __name__ == '__main__':
    
    agent: Agent
    board: GameBoard
    agent = MiniMaxAgent()
    logging.basicConfig(filename="./2048/RandomAgentMixedHeur-d6.txt", level=logging.INFO)
    for i in range(10):
        board = GameBoard()
        done = False
        moves = 0
        board.render()
        start = datetime.now()

        logging.info('\n\nRound number "{}"'.format(i + 1))
        while not done:
            if moves % 100 == 0:
                cent = 0
            action = agent.play(board)
            print('Next Action: "{}"'.format(
                int_to_string[action]), ',   Move: {}'.format(moves))
            done = board.play(action)
            done = done or check_win(board)
            board.render()
            moves += 1

        print('\nTotal time: {}'.format(datetime.now() - start))
        print('\nTotal Moves: {}'.format(moves))
        logging.info('\nTotal time: {}'.format(datetime.now() - start))
        logging.info('\nTotal Moves: {}'.format(moves))
        if check_win(board):
            print("WON THE GAME!!!!!!!!")
            logging.info('"WON THE GAME!!!!!!!!"\n******************************************************')
        else:
            print("BOOOOOOOOOO!!!!!!!!!")
            logging.info('"Loser"\n******************************************************')
