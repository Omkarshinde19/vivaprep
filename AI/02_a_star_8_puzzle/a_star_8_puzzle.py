# A* Search for the 8-Puzzle Problem
import heapq

start = "023145786"
goal = "123456780"
blank_moves = {0: [1, 3], 1: [0, 2, 4], 2: [1, 5], 3: [0, 4, 6], 4: [1, 3, 5, 7],
               5: [2, 4, 8], 6: [3, 7], 7: [4, 6, 8], 8: [5, 7]}


def misplaced_tiles(board):
    count = 0
    for position in range(9):
        if board[position] != "0" and board[position] != goal[position]:
            count = count + 1
    return count


open_list = [(misplaced_tiles(start), 0, start, [start])]
closed_list = set()

while open_list:
    f_score, g_score, board, path = heapq.heappop(open_list)
    if board == goal:
        print("Solution path:", path)
        print("Moves:", g_score, "| States explored:", len(closed_list))
        break
    closed_list.add(board)
    blank = board.index("0")
    for new_blank in blank_moves[blank]:
        tiles = list(board)
        tiles[blank], tiles[new_blank] = tiles[new_blank], tiles[blank]
        new_board = "".join(tiles)
        if new_board not in closed_list:
            new_g_score = g_score + 1
            new_f_score = new_g_score + misplaced_tiles(new_board)
            heapq.heappush(open_list, (new_f_score, new_g_score, new_board, path + [new_board]))
