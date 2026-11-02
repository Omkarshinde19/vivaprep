# Depth First Search for the Water Jug Problem

start = (0, 0)
goal_states = [(2, 0), (0, 2)]

stack = [(start, [start])]
visited = {start}

while stack:
    state, path = stack.pop()
    if state in goal_states:
        print("Solution path:", path)
        print("Moves:", len(path) - 1)
        break
    four_litre, three_litre = state
    pour_to_three = min(four_litre, 3 - three_litre)
    pour_to_four = min(three_litre, 4 - four_litre)
    next_states = [(4, three_litre),
                   (four_litre, 3),
                   (0, three_litre),
                   (four_litre, 0),
                   (four_litre - pour_to_three, three_litre + pour_to_three),
                   (four_litre + pour_to_four, three_litre - pour_to_four)]
    for next_state in next_states:
        if next_state not in visited:
            visited.add(next_state)
            stack.append((next_state, path + [next_state]))
