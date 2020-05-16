import pickle
from heapq import heappush, heappop
from time import sleep
# import numpy as np

# --------------------------------------
# --------------------------------------
# SLIDING PUZZLE IMPORTS (REPEATED CODE)
# --------------------------------------
# --------------------------------------


def tuple_puzzle_to_list(puzzle):
    '''Converts a board matrix from a tuple of tuples to a list of lists'''
    return list(list(row) for row in puzzle)


def list_puzzle_to_tuple(puzzle):
    '''Converts a board matrix from a list of lists to a tuple of tuples'''
    return tuple(tuple(row) for row in puzzle)


def is_solved(puzzle):
    '''Returns a boolean indicating whether a board is solved or not'''
    # if the zero isnt in the bottom left corner dont search the whole board
    if puzzle[-1][-1] != 0:
        return False
    for x in range(len(puzzle)):
        for y in range(len(puzzle[-1])):
            if x == len(puzzle) - 1 and y == len(puzzle[-1]) - 1:
                continue
            if puzzle[x][y] != (x*len(puzzle[-1])) + (y + 1):
                return False
    return True


def find_zero(puzzle):
    '''Given a board, returns a tuple with the x,y coordinates of the zero.
    NOTE: This can be improved by keeping track of the 0 instead of searching
    for it every time'''
    for x in range(len(puzzle)):
        for y in range(len(puzzle[-1])):
            if puzzle[x][y] == 0:
                return x, y


def find_next_moves(puzzle):
    '''Given a puzzle this will find the coordinates of the 0 and return
    a tuple with x,y coordinates and a list of four new x,y coordinates or
    None if the 0 is in a corner or on an edge'''
    x, y = find_zero(puzzle)
    left = (x - 1, y) if x > 0 else None
    right = (x + 1, y) if x < len(puzzle) - 1 else None
    up = (x, y - 1) if y > 0 else None
    down = (x, y + 1) if y < len(puzzle[-1]) - 1 else None
    return (x, y), [left, right, up, down]


def swap(puzzle, start, next_move):
    '''Given a puzzle, a tuple with x,y 0 (start) coordinates, and the x,y
    coordinates of the next move, '''
    lst_pzl = tuple_puzzle_to_list(puzzle)
    sx, sy, nx, ny = *start, *next_move
    lst_pzl[sx][sy], lst_pzl[nx][ny] = lst_pzl[nx][ny], lst_pzl[sx][sy]
    return list_puzzle_to_tuple(lst_pzl)


def moves(puzzle):
    '''Given a puzzle this will find the next 2-4 possible moves, create
    2-4 new game boards, then returns a list of them. '''
    start, next_moves = find_next_moves(puzzle)
    new_boards = []
    for move in next_moves:
        if move is not None:
            new_board = swap(puzzle, start, move)
            new_boards.append((new_board, move))
    return new_boards


def manhattan_dist(puzzle):
    '''returns the manhattan distance of a board to its solved state
    This is the sum of the manhattan distances (aka l1 distance/ taxicab
    distance) from each number to its desired location.
    '''

    # return num_inversions(puzzle)[0]
    dist = 0
    for x in range(len(puzzle)):
        for y in range(len(puzzle[0])):
            if puzzle[x][y] != 0:
                val = puzzle[x][y]
                des_x, des_y = divmod(val - 1, len(puzzle[0]))
                dist += abs(x - des_x) + abs(y - des_y)
    return dist


def display_solution(board, all_moves, sleep_len=1):
    '''prints the solution with fancy colors and dramatic pauses'''
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    END = '\033[0m'
    RED = '\033[91m'
    # YELLOW = '\033[93m'
    print('Start:')
    for row in board:
        print(f'\t{row}')
    print()
    num_moves = len(all_moves)
    zero_loc = find_zero(board)
    for itr, move in zip(range(1, num_moves + 1), all_moves):
        sleep(sleep_len)
        print(f'Move {itr}: {BLUE}{zero_loc}{END} <-> {RED}{move}{END}')
        board_str = ''
        for i, row in enumerate(board):
            board_str += '\t('
            for j, col in enumerate(row):
                if j != 0:
                    board_str += ', '
                if zero_loc == (i, j):
                    board_str += f'{BLUE}{col}{END}'
                elif move == (i, j):
                    board_str += f'{RED}{col}{END}'
                else:
                    board_str += f'{col}'
            board_str += ')\n'
        board = swap(board, zero_loc, move)
        print(board_str)
        zero_loc = move
    sleep(sleep_len)
    print(f'Done in {num_moves} moves:{GREEN}')
    for row in board:
        print(f'\t{row}')
    print(END)


# --------------------------------------
# --------------------------------------
# --------------DONE--------------------
# --------------------------------------
# --------------------------------------


# the model will predict the number of moves required from a starting position
model = pickle.load(open('best_states.pkl', 'rb'))


def flatten(board):
    flat = []
    for row in board:
        for item in row:
            flat.append(item)
    return flat


def predict_num_moves(board):
    man_dist = manhattan_dist(board)
    if man_dist <= 3:
        return man_dist
    # flat_board = np.array(board).flatten()
    flat_board = flatten(board)
    return model.predict([flat_board])[0]


def solve(original_puzzle):
    '''Uses A* method with an heuristic for how solved a given puzzle  state
    is. Uses manhattan distance as the heuristic.'''
    if type(original_puzzle) == list:
        original_puzzle = list_puzzle_to_tuple(original_puzzle)
    # if not is_solveable(original_puzzle):
    #     return -1, None
    if is_solved(original_puzzle):
        return 0, []
    # TODO: Plot what the min heap's min is every time
    min_heap = []
    dist = predict_num_moves(original_puzzle)
    min_heap.append((dist, original_puzzle, []))
    # create a set of seen boards to make sure we dont follow the same path
    # more than once
    seen = set()
    seen.add(original_puzzle)
    while len(min_heap) > 0:
        # remove the next board from the queue, alone w num moves, and allmoves
        _, curr_board, all_moves = heappop(min_heap)
        # find the next possible board moves
        next_board_moves = moves(curr_board)
        # loop through the new boards
        for board, move in next_board_moves:
            # ensure the board has not been seen
            if board not in seen:
                # if so check if the board is solved
                if is_solved(board):
                    # if it is return the board and the moves
                    return all_moves + [move]
                # add the board, num_moves + 1, and all_moves +[move] to the q
                dist = predict_num_moves(board) + len(all_moves) + 1
                board_obj = dist, board, all_moves + [move]
                heappush(min_heap, board_obj)
                # add the board to seen
                seen.add(board)
    # if the queue is empty it means all possible perms have been seen and none
    # were solved. no solution, return -1
    return None


# def display_solution(moves):
#     for iteration, board in enumerate(moves):
#         print(f'Move no. {iteration}')
#         for row in board:
#             print(f'\t{row}')


puzzle = (
    (0, 2, 3),
    (1, 4, 6),
    (7, 5, 8)
)

puzzle = (
    (4, 1, 0),
    (2, 6, 3),
    (7, 5, 8)
)

puzzle = (
    (0, 8, 1),
    (5, 4, 7),
    (3, 2, 6)
)

puzzle = (
    (7, 6, 8),
    (2, 0, 1),
    (3, 5, 4)
)

if __name__ == '__main__':

    all_moves = solve(puzzle)

    display_solution(puzzle, all_moves, 0.3)
