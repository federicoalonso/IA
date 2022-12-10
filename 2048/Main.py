from datetime import datetime
from GameBoard import GameBoard
from Agent import Agent
# from Random_Agent import RandomAgent
from MiniMax_Agent import MiniMaxAgent
from ExpectiMax_Agent import ExpectiMax_Agent
# from MiniMax_Agent_2 import MiniMaxAgent
import logging

def check_win(board: GameBoard):
    return board.get_max_tile() >= 2048


int_to_string = ['UP', 'DOWN', 'LEFT', 'RIGHT']

if __name__ == '__main__':
    
    agent: Agent
    board: GameBoard
    agent = MiniMaxAgent()
    # agent = ExpectiMax_Agent()
    logging.basicConfig(filename="./2048/MMAgent_test-d6.txt", level=logging.INFO)
    results = []
    times = []
    total_moves = []
    for i in range(1):
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
            # print('Next Action: "{}"'.format(int_to_string[action]), ',   Move: {}'.format(moves))
            done = board.play(action)
            done = done or check_win(board)
            # board.render()
            moves += 1
        total_time = datetime.now() - start
        times.append(total_time.total_seconds())
        total_moves.append(moves)
        print('\nTotal time: {}'.format(total_time))
        print('\nTotal Moves: {}'.format(moves))
        logging.info('\nTotal time: {}'.format(total_time))
        logging.info('\nTotal Moves: {}'.format(moves))
        if check_win(board):
            print("WON THE GAME!!!!!!!!")
            results.append(1)
            logging.info('"WON THE GAME!!!!!!!!"\n******************************************************')
        else:
            print("BOOOOOOOOOO!!!!!!!!!")
            results.append(0)
            logging.info('"Loser"\n******************************************************')
        
    logging.info('"Results"******************************************************')
    sum_won = 0
    sum_time = 0
    sum_moves = 0
    
    for i in range(len(results)):
        sum_won += results[i]
        sum_time += times[i]
        sum_moves += total_moves[i]
    
    avg_won = sum_won / len(results)
    avg_time = sum_time / len(results)
    avg_mov = sum_moves / len(results)

    logging.info('\Average Wons: {}%'.format(avg_won * 100))
    logging.info('\Average Moves: {}'.format(avg_mov))
    logging.info('\Average Time: {}'.format(avg_time))

