from datetime import datetime
from GameBoard import GameBoard
from Agent import Agent
from Random_Agent import RandomAgent
from MiniMax_Agent import MiniMaxAgent
from ExpectiMax_Agent import ExpectiMax_Agent
import logging
from csv_logger import CsvLogger

def check_win(board: GameBoard):
    return board.get_max_tile() >= 2048


int_to_string = ['UP', 'DOWN', 'LEFT', 'RIGHT']

if __name__ == '__main__':

    filename = './log.csv'
    delimiter = ','
    level = logging.INFO
    custom_additional_levels = ['log2']
    fmt = f'%(asctime)s{delimiter}%(levelname)s{delimiter}%(message)s'
    datefmt = '%Y/%m/%d %H:%M:%S'
    max_size = 1000000  # 1 megabyte
    max_files = 4  
    header = ['date', 'level', 'time', 'result', 'depth', 'moves', 'heuristic', 'agent']
    depth = 5
    heuristic = 'mixed'
    agent_name = 'expectimax'

    csvlogger = CsvLogger(filename=filename,
                        delimiter=delimiter,
                        level=level,
                        add_level_names=custom_additional_levels,
                        add_level_nums=None,
                        fmt=fmt,
                        datefmt=datefmt,
                        max_size=max_size,
                        max_files=max_files,
                        header=header)
    
    agent: Agent
    board: GameBoard
    # agent = MiniMaxAgent()
    agent = ExpectiMax_Agent()
    logging.basicConfig(filename="./EMAgent-d5.txt", level=logging.INFO)
    results = []
    times = []
    total_moves = []
    for i in range(3):
        board = GameBoard()
        done = False
        moves = 0
        # board.render()
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
            csvlogger.log2([total_time, 1, depth, moves, heuristic, agent_name])
            logging.info('"WON THE GAME!!!!!!!!"\n******************************************************')
        else:
            print("BOOOOOOOOOO!!!!!!!!!")
            csvlogger.log2([total_time, 0, depth, moves, heuristic, agent_name])
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

