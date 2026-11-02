# Breadth First Search for the 8-Puzzle Problem
from collections import deque

start = "023145786"
goal = "123456780"
blank_moves = {0: [1, 3], 1: [0, 2, 4], 2: [1, 5], 3: [0, 4, 6], 4: [1, 3, 5, 7],
               5: [2, 4, 8], 6: [3, 7], 7: [4, 6, 8], 8: [5, 7]}

queue = deque([(start, [start])])
visited = {start}

while queue:
    board, path = queue.popleft()
    if board == goal:
        print("Solution path:", path)
        print("Moves:", len(path) - 1, "| States visited:", len(visited))
        break
    blank = board.index("0")
    for new_blank in blank_moves[blank]:
        tiles = list(board)
        tiles[blank], tiles[new_blank] = tiles[new_blank], tiles[blank]
        new_board = "".join(tiles)
        if new_board not in visited:
            visited.add(new_board)
            queue.append((new_board, path + [new_board]))
