# Practical 2: A* Search for the 8-Puzzle Problem

Syllabus reference: Part A, Assignment 3

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

In the code, a board is a string read row by row, with 0 as the blank. The start is `"023145786"`.

### Diagram 2: The A* search tree for this program

`g` is moves made so far, `h` is misplaced tiles, and `f = g + h`. A* always expands the lowest `f`.

```
                         0 2 3
                         1 4 5      g=0 h=4 f=4   (expanded 1st)
                         7 8 6
                        /      \
                 2 0 3            1 2 3
                 1 4 5            0 4 5     g=1 h=3 f=4   (expanded 2nd)
                 7 8 6            7 8 6
              g=1 h=5 f=6         /     \
             (never expanded)    /       \
                          1 2 3            1 2 3
                          4 0 5            7 4 5
                          7 8 6            0 8 6
                     g=2 h=2 f=4        g=2 h=4 f=6
                   (expanded 3rd)     (never expanded)
                    /      |     \
              1 0 3      1 2 3      1 2 3
              4 2 5      4 5 0      4 8 5
              7 8 6      7 8 6      7 0 6
            g=3 h=3    g=3 h=1    g=3 h=3
              f=6        f=4        f=6
                      (expanded 4th)
                           |
                         1 2 3
                         4 5 6      g=4 h=0 f=4   GOAL
                         7 8 0
```

### Diagram 3: How the algorithm flows

```
   Put start in open list
            |
            v
   Take board with lowest f  <----------------+
            |                                 |
            v                                 |
       Is it the goal? --Yes--> Print path    |
            | No                              |
            v                                 |
   Add board to closed list                   |
            |                                 |
            v                                 |
   Slide blank to make new boards             |
   Calculate g, h, f for each                 |
   Add those not closed to open list ---------+
```

### Explain the problem in words (viva answer)

The 8-puzzle is a 3x3 board with eight numbered tiles and one blank. A tile next to the blank can slide into it. We must reach the goal arrangement from the start arrangement using as few moves as possible.

### Explain the solution in words (viva answer)

I used A* search, which scores each board using f(n) = g(n) + h(n). Here g(n) is the number of moves made so far, and h(n) is the number of misplaced tiles, which estimates the moves left.

The program keeps an open list of boards waiting to be explored and a closed list of boards already explored. It always picks the lowest f from the open list. If that board is the goal, it prints the path. Otherwise it slides the blank to create new boards and adds them to the open list.

For this start, the solution takes 4 moves and only 4 boards are explored before reaching the goal. BFS explores far more on the same puzzle, as Practical 5 shows.

---

## 2. Code Explanation

```python
import heapq
```
`heapq` is a priority queue. It always gives the smallest item first, which is the board with the lowest f score.

```python
start = "023145786"
```
The starting board as a string, with 0 as the blank. A string is easy to compare and can be stored in a set.

```python
goal = "123456780"
```
The board we want to reach.

```python
blank_moves = {0: [1, 3], 1: [0, 2, 4], 2: [1, 5], 3: [0, 4, 6], 4: [1, 3, 5, 7],
               5: [2, 4, 8], 6: [3, 7], 7: [4, 6, 8], 8: [5, 7]}
```
For each position 0 to 8, this lists the positions the blank can move to. It keeps the blank on the board without writing separate up, down, left and right checks.

```python
def misplaced_tiles(board):
```
This is the heuristic function h(n). It estimates how far a board is from the goal.

```python
    count = 0
```
Starts the count of misplaced tiles at zero.

```python
    for position in range(9):
```
Goes through all 9 positions on the board.

```python
        if board[position] != "0" and board[position] != goal[position]:
```
Checks if the tile differs from the goal. The blank is skipped because it is not a tile, and skipping it means h never overestimates.

```python
            count = count + 1
```
Counts this misplaced tile.

```python
    return count
```
Returns the value of h(n).

```python
open_list = [(misplaced_tiles(start), 0, start, [start])]
```
The open list starts with the start board. Each entry is (f, g, board, path). The heap compares f first, so that is why f is placed first. At the start, g is 0, so f = h.

```python
closed_list = set()
```
Stores boards already explored. A set is used because checking membership is fast.

```python
while open_list:
```
Continues as long as boards are waiting to be explored.

```python
    f_score, g_score, board, path = heapq.heappop(open_list)
```
Removes the board with the lowest f. This choice is the main idea of A*.

```python
    if board == goal:
```
This is the goal test. It is done when a board is removed from the list, because only then is its path known to be the best.

```python
        print("Solution path:", path)
```
Prints every board from start to goal.

```python
        print("Moves:", g_score, "| States explored:", len(closed_list))
```
Prints the path cost and how many boards were explored, which shows how efficient the search was.

```python
        break
```
Stops the search as the goal has been found.

```python
    closed_list.add(board)
```
Marks this board as explored, so it is not expanded again.

```python
    blank = board.index("0")
```
Finds the position of the blank.

```python
    for new_blank in blank_moves[blank]:
```
Tries every position the blank can move to.

```python
        tiles = list(board)
```
Strings cannot be changed in Python, so the board is converted to a list.

```python
        tiles[blank], tiles[new_blank] = tiles[new_blank], tiles[blank]
```
Swaps the blank with the neighbouring tile, which is one move.

```python
        new_board = "".join(tiles)
```
Converts the list back to a string.

```python
        if new_board not in closed_list:
```
Skips boards already explored, so the search does not go round in cycles.

```python
            new_g_score = g_score + 1
```
Each move costs 1, so the new board is one move further from the start.

```python
            new_f_score = new_g_score + misplaced_tiles(new_board)
```
Calculates f(n) = g(n) + h(n).

```python
            heapq.heappush(open_list, (new_f_score, new_g_score, new_board, path + [new_board]))
```
Adds the new board to the open list. `path + [new_board]` stores the route, so no separate parent pointers are needed.

### Output

```
Solution path: ['023145786', '123045786', '123405786', '123450786', '123456780']
Moves: 4 | States explored: 4
```

---

## 3. Write-up

### Problem Statement

Implement A* Search for the 8-puzzle problem.

### Objectives

1. To understand the concept of informed search techniques.
2. To implement the A* algorithm for the 8-puzzle problem.
3. To understand the use of the evaluation function f(n) = g(n) + h(n).

### Theory

**Informed search:** A search that uses problem-specific knowledge, called a heuristic, to choose which state to explore next.

**A* algorithm:** A best-first search that selects the state with the lowest value of:

f(n) = g(n) + h(n)

- g(n) is the cost from the start to the current state.
- h(n) is the estimated cost from the current state to the goal.

**Open and closed lists:** The open list holds generated states waiting to be explored. The closed list holds states already explored.

**Heuristics for the 8-puzzle:** The two common options are the number of misplaced tiles, used in this program, and the Manhattan distance, which adds up how far each tile is from its goal position.

**Admissible heuristic:** A heuristic that never overestimates the true remaining cost. A* with an admissible heuristic finds the optimal path. Misplaced tiles is admissible, since each misplaced tile needs at least one move.

**Algorithm:**

1. Define the start and goal states.
2. Calculate h for the start, set g = 0, and insert it in the open list.
3. Remove the state with the lowest f.
4. If it is the goal, display the path and stop.
5. Otherwise, add it to the closed list and generate new states by moving the blank.
6. Calculate g, h and f for each new state and add it to the open list.
7. Repeat from step 3.

### Conclusion

A* search was implemented for the 8-puzzle using the misplaced tiles heuristic. It found the optimal 4-move solution after exploring only 4 states, which shows how a heuristic directs the search towards the goal.

---

## 4. Viva Questions

**1. What are informed and uninformed search techniques?**
Informed search uses a heuristic to guide the search, such as A*. Uninformed search uses no such knowledge, such as BFS and DFS.

**2. What are the differences between them?**
Informed search uses problem knowledge and usually explores fewer states. Uninformed search explores blindly and usually needs more time and memory.

**3. What is the evaluation function of A*?**
f(n) = g(n) + h(n).

**4. What do g(n) and h(n) mean?**
g(n) is the actual cost from the start to the state. h(n) is the estimated cost from the state to the goal.

**5. Is A* informed or uninformed?**
Informed, because it uses a heuristic.

**6. What is a heuristic?**
A rule or estimate that tells how close a state is to the goal, helping the search choose better states first.

**7. What heuristic did you use?**
The number of misplaced tiles, not counting the blank.

**8. What is Manhattan distance?**
For each tile, the sum of its row and column distance from its goal position, added over all tiles.

**9. What is an admissible heuristic?**
One that never overestimates the true remaining cost.

**10. Does A* always find the shortest path?**
It does when the heuristic is admissible. If the heuristic overestimates, it may return a longer path.

**11. What are the open and closed lists?**
The open list holds states waiting to be explored. The closed list holds states already explored.

**12. Why is heapq used?**
It is a priority queue, so it returns the lowest f quickly.

**13. Why is the blank not counted as a misplaced tile?**
The blank is not a tile. Counting it could overestimate the remaining moves and make the heuristic inadmissible.

**14. What happens when h(n) = 0 for every state?**
A* becomes uniform cost search, which here behaves like BFS because every move costs 1.

**15. What is Best First Search?**
A search that expands the most promising state according to an evaluation function. Greedy best first uses only h(n), while A* uses g(n) + h(n).

**16. Can every 8-puzzle be solved?**
No. Only half of all arrangements can reach a given goal. Solvability is checked by counting inversions, and for a standard goal the count must be even.

**17. What is a problem-solving agent?**
An agent that formulates a goal and a problem, then searches for a sequence of actions that reaches the goal.

**18. Where are search techniques applied in AI?**
In path finding, games, robot navigation, planning and scheduling.

**19. What are the applications of A*?**
Maps and navigation, game path finding, robot motion planning and network routing.

**20. What is the time and space complexity of A*?**
Both are O(b^d) in the worst case, where b is the branching factor and d is the solution depth. A good heuristic reduces this in practice.
