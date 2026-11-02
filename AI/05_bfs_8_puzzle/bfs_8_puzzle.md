# Practical 5: Breadth First Search for the 8-Puzzle Problem

Syllabus reference: Part B, Assignment 1

---

## 1. The Problem and Its Solution

### Diagram 1: Start and goal boards

```
      START              GOAL
    +---+---+---+     +---+---+---+
    |   | 2 | 3 |     | 1 | 2 | 3 |
    +---+---+---+     +---+---+---+
    | 1 | 4 | 5 |     | 4 | 5 | 6 |
    +---+---+---+     +---+---+---+
    | 7 | 8 | 6 |     | 7 | 8 |   |
    +---+---+---+     +---+---+---+
```

### Diagram 2: BFS explores level by level

```
Depth 0                     0 2 3
                            1 4 5
                            7 8 6
                           /     \
Depth 1            2 0 3             1 2 3
                   1 4 5             0 4 5
                   7 8 6             7 8 6
                  /    \            /     \
Depth 2      2 3 0    2 4 3     1 2 3     1 2 3
             1 4 5    1 0 5     4 0 5     7 4 5
             7 8 6    7 8 6     7 8 6     0 8 6
               ...      ...       |         ...
Depth 3                         1 2 3
                                4 5 0     (and all other depth 3 boards)
                                7 8 6
                                  |
Depth 4                         1 2 3
                                4 5 6     GOAL
                                7 8 0
```

Every board at one depth is explored before any board at the next depth.

### Diagram 3: The queue works first in, first out

```
   add new boards at the back                remove from the front
            |                                         ^
            v                                         |
          +-------+-------+-------+-------+-------+
   back   | board | board | board | board | board |   front
          +-------+-------+-------+-------+-------+
```

### Explain the problem in words (viva answer)

The 8-puzzle is a 3x3 board with eight numbered tiles and one blank. A tile next to the blank can slide into it. I treat this as a planning problem: find a sequence of moves that changes the start board into the goal board.

### Explain the solution in words (viva answer)

I used Breadth First Search. Each board is a state, and each blank movement is an action leading to a new state.

The program puts the start board in a queue. It removes the board at the front, checks if it is the goal, and otherwise creates all boards reachable in one move. New boards go to the back of the queue, and a visited set stops any board being repeated.

Because of the first in, first out order, all boards at one depth are explored before going deeper. So the first time the goal is reached, the path has the minimum number of moves. Here it is 4 moves, with 44 boards visited. A* on the same puzzle explores only 4 boards before reaching the goal, because it has a heuristic and BFS does not.

---

## 2. Code Explanation

```python
from collections import deque
```
`deque` is a queue with fast removal from the front, as BFS requires.

```python
start = "023145786"
```
The starting board as a string read row by row, with 0 as the blank. Strings are easy to compare and can go in a set.

```python
goal = "123456780"
```
The board we want to reach.

```python
blank_moves = {0: [1, 3], 1: [0, 2, 4], 2: [1, 5], 3: [0, 4, 6], 4: [1, 3, 5, 7],
               5: [2, 4, 8], 6: [3, 7], 7: [4, 6, 8], 8: [5, 7]}
```
For each position, this lists where the blank can move. For example, from the centre (4), it can go to 1, 3, 5 or 7.

```python
queue = deque([(start, [start])])
```
The queue starts with the start board. Each entry holds a board and the path taken to reach it.

```python
visited = {start}
```
Remembers boards already seen, so none are explored twice.

```python
while queue:
```
Continues until the queue is empty. An empty queue means every reachable board was tried.

```python
    board, path = queue.popleft()
```
Removes the oldest board from the front. This is what makes the search breadth first.

```python
    if board == goal:
```
This is the goal test.

```python
        print("Solution path:", path)
```
Prints all boards from start to goal.

```python
        print("Moves:", len(path) - 1, "| States visited:", len(visited))
```
The path includes the start board, so moves are one less than its length. States visited shows how much work the search did.

```python
        break
```
Stops as the goal is found.

```python
    blank = board.index("0")
```
Finds the blank's position.

```python
    for new_blank in blank_moves[blank]:
```
Tries each valid blank movement.

```python
        tiles = list(board)
```
Strings cannot be changed, so the board is converted to a list.

```python
        tiles[blank], tiles[new_blank] = tiles[new_blank], tiles[blank]
```
Swaps the blank with its neighbour, which is one move.

```python
        new_board = "".join(tiles)
```
Converts the list back to a string.

```python
        if new_board not in visited:
```
Only new boards are added.

```python
            visited.add(new_board)
```
Marks the board as seen when it is added, so the queue does not hold copies of it.

```python
            queue.append((new_board, path + [new_board]))
```
Adds the board to the back of the queue, with its path extended by one board.

### Output

```
Solution path: ['023145786', '123045786', '123405786', '123450786', '123456780']
Moves: 4 | States visited: 44
```

---

## 3. Write-up

### Problem Statement

Use BFS to solve a planning problem. Examples can be the 8-puzzle problem, robot path planning, blocks world, etc. Here, BFS is implemented for the 8-puzzle problem.

### Objectives

1. To understand the concept of uninformed (blind) search techniques.
2. To understand Breadth First Search for solving a planning problem.
3. To implement BFS for the 8-puzzle problem and obtain the solution path.

### Theory

**Breadth First Search:** An uninformed search that explores a state space level by level. It explores all states at depth 1, then depth 2, and so on. It uses a FIFO queue, and a visited set avoids repeating states.

**Key characteristics:**

- It is uninformed, so it needs no heuristic.
- It is complete when the branching factor is finite.
- It finds the minimum number of steps when all actions have equal cost.

**BFS for the 8-puzzle:** Each board is a node and each blank movement is an edge. Storing how each board was reached allows the sequence of moves to be displayed.

**Advantages:** It is simple and systematic, needs no heuristic, is complete, and finds the shortest solution when all actions have equal cost.

**Limitations:** It needs a lot of memory, becomes expensive for large search spaces, and does not use knowledge to guide the search.

**Algorithm:**

1. Define the start and goal states.
2. Create a queue and a visited set.
3. Insert the start state in the queue and mark it visited.
4. Remove the front state.
5. If it is the goal, display the path and stop.
6. Generate all valid next states by moving the blank.
7. Mark each unvisited state as visited and add it to the back of the queue.
8. Repeat from step 4 until the goal is found or the queue is empty.

### Conclusion

BFS was applied to the 8-puzzle as a planning problem. It explored the states level by level using a FIFO queue and avoided repeated states with a visited set. It found the shortest solution of 4 moves after visiting 44 states.

---

## 4. Viva Questions

**1. What is Breadth First Search?**
An uninformed search that explores all states at one depth before moving to the next depth.

**2. Is BFS informed or uninformed?**
Uninformed, as it uses no heuristic.

**3. What data structure does BFS use?**
A FIFO queue.

**4. What is the difference between BFS and DFS?**
BFS goes level by level with a queue and finds the fewest steps. DFS goes deep along one branch with a stack and may find a longer path.

**5. How is BFS applied to the 8-puzzle?**
Each board is a state and each blank move creates a new state. BFS explores these level by level until it reaches the goal.

**6. Why is a visited set required?**
Without it, the search repeats boards and wastes time, since a move can be immediately undone.

**7. Is BFS complete?**
Yes, when the branching factor is finite. It reaches every depth in order, so it will find a solution if one exists.

**8. When does BFS find the shortest path?**
When all actions have equal cost, as in the 8-puzzle.

**9. What are the applications of BFS?**
Shortest path in unweighted graphs, puzzle solving, robot path planning, web crawling and social network analysis.

**10. What are the main limitations of BFS?**
High memory use and slow performance on large search spaces.

**11. What is the time and space complexity of BFS?**
Both are O(b^d), where b is the branching factor and d is the depth of the solution.

**12. What is a planning problem?**
Finding a sequence of actions that changes an initial state into a goal state.

**13. How many states does the 8-puzzle have?**
9! = 362880 arrangements, but only half, 181440, can be reached from a given board.

**14. What is the maximum number of moves for the blank?**
4 from the centre, 3 from an edge and 2 from a corner.

**15. Why is a dictionary used for blank moves?**
It gives the valid moves for a position directly, so no separate boundary checks are needed.

**16. Why is the board stored as a string?**
It is simple to compare with the goal and can be stored in a set.

**17. Why is a board marked visited when added, not when removed?**
It stops the same board being added to the queue multiple times, saving memory.

**18. What happens if a board cannot be solved?**
BFS explores all reachable boards, the queue becomes empty, and the loop ends without printing a solution.

**19. How does the program remember the solution path?**
Each queue entry stores its full path. The usual alternative is to store each state's parent and follow those back from the goal.

**20. How does BFS compare with A* on this puzzle?**
Both find the 4-move solution. BFS visits 44 boards, while A* explores only 4 before the goal, because it is guided by a heuristic.
