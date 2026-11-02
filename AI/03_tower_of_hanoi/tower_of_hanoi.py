# Tower of Hanoi using State Space Search (BFS)
from collections import deque

start = ((3, 2, 1), (), ())
goal = ((), (), (3, 2, 1))
peg_names = "ABC"

queue = deque([(start, [])])
visited = {start}

while queue:
    state, moves = queue.popleft()
    if state == goal:
        print("Start:", start)
        for move in moves:
            print(move)
        print("Total moves:", len(moves))
        break
    for source in range(3):
        for destination in range(3):
            if source != destination and state[source]:
                disk = state[source][-1]
                if not state[destination] or disk < state[destination][-1]:
                    new_state = list(state)
                    new_state[source] = state[source][:-1]
                    new_state[destination] = state[destination] + (disk,)
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        visited.add(new_state)
                        move = f"Move disk {disk} from {peg_names[source]} to {peg_names[destination]}: {new_state}"
                        queue.append((new_state, moves + [move]))
