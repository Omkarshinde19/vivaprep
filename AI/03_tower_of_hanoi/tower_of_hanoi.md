# Practical 3: Tower of Hanoi using State Space Search

Syllabus reference: Part A, Assignment 5

---

## 1. The Problem and Its Solution

### Diagram 1: Start and goal

```
        START                              GOAL

     |      |      |                 |      |      |
    =1=     |      |                 |      |     =1=
   ==2==    |      |                 |      |    ==2==
  ===3===   |      |                 |      |   ===3===
 ---------------------           ---------------------
     A      B      C                 A      B      C
```

### Diagram 2: All 7 moves of the solution

```
State format: (peg A, peg B, peg C). The last number in a peg is its top disk.

((3,2,1), (),    ())       Start
        | Move disk 1 from A to C
((3,2),   (),    (1))
        | Move disk 2 from A to B
((3),     (2),   (1))
        | Move disk 1 from C to B
((3),     (2,1), ())
        | Move disk 3 from A to C
((),      (2,1), (3))
        | Move disk 1 from B to A
((1),     (2),   (3))
        | Move disk 2 from B to C
((1),     (),    (3,2))
        | Move disk 1 from A to C
((),      (),    (3,2,1))  Goal
```

### Diagram 3: First levels of the state space

```
                         ((3,2,1),(),())
                          /            \
              disk 1 to B                disk 1 to C
                  /                            \
        ((3,2),(1),())                    ((3,2),(),(1))
            /      \                         /      \
     disk 2 to C   disk 1 to C        disk 2 to B   disk 1 to B
          /            \                  /             \
((3),(1),(2))    ((3,2),(),(1))    ((3),(2),(1))    ((3,2),(1),())
                  already visited                    already visited
```

BFS explores this tree level by level and skips any state it has already seen.

### Explain the problem in words (viva answer)

There are three pegs and three disks of different sizes, all stacked on peg A with the largest at the bottom. All the disks must move to peg C. Only one disk can move at a time, only a top disk can move, and a larger disk can never go on a smaller one.

### Explain the solution in words (viva answer)

I treated this as a state space search. A state is the arrangement of disks on the three pegs, and a legal move is an operator that produces a new state.

I searched using BFS with a queue. The program takes a state, checks if it is the goal, and otherwise tries moving a top disk between every pair of pegs. Each legal move that gives a new state is added to the queue with its list of moves. As BFS works level by level and every move costs 1, the first solution found is the shortest. For 3 disks that is 2^3 - 1 = 7 moves.

---

## 2. Code Explanation

```python
from collections import deque
```
`deque` is a queue that removes from the front efficiently, which BFS needs.

```python
start = ((3, 2, 1), (), ())
```
The initial state: pegs A, B and C. All disks are on A, and the last number in each peg is its top disk. Tuples are used so that a state can be stored in a set.

```python
goal = ((), (), (3, 2, 1))
```
The goal state, with all disks on C in the same order.

```python
peg_names = "ABC"
```
Converts peg numbers 0, 1 and 2 to letters for the output.

```python
queue = deque([(start, [])])
```
The queue starts with the start state and an empty list of moves.

```python
visited = {start}
```
Remembers states already seen, which prevents endless cycles.

```python
while queue:
```
Continues as long as states are waiting.

```python
    state, moves = queue.popleft()
```
Takes the oldest state from the front. First in, first out is what makes this BFS.

```python
    if state == goal:
```
This is the goal test.

```python
        print("Start:", start)
```
Prints the initial state.

```python
        for move in moves:
```
Goes through the stored moves in order.

```python
            print(move)
```
Prints each move with its resulting state.

```python
        print("Total moves:", len(moves))
```
Prints the path cost, which should be 7.

```python
        break
```
Stops as the goal is found.

```python
    for source in range(3):
```
Tries every peg as the peg to move from.

```python
        for destination in range(3):
```
Tries every peg as the peg to move to.

```python
            if source != destination and state[source]:
```
A disk cannot move to the same peg, and the source peg must have a disk. An empty tuple counts as false.

```python
                disk = state[source][-1]
```
Takes the top disk, which is the last item.

```python
                if not state[destination] or disk < state[destination][-1]:
```
The main rule: the destination must be empty or have a larger top disk.

```python
                    new_state = list(state)
```
Tuples cannot be changed, so a list copy is made.

```python
                    new_state[source] = state[source][:-1]
```
Removes the top disk from the source peg.

```python
                    new_state[destination] = state[destination] + (disk,)
```
Places the disk on the destination. `(disk,)` is a tuple with one item.

```python
                    new_state = tuple(new_state)
```
Converts it back to a tuple, so it can be stored in `visited`.

```python
                    if new_state not in visited:
```
Only new states are explored.

```python
                        visited.add(new_state)
```
Marks it as seen at once, so it is not queued twice.

```python
                        move = f"Move disk {disk} from {peg_names[source]} to {peg_names[destination]}: {new_state}"
```
Creates readable text for this move and the state it leads to.

```python
                        queue.append((new_state, moves + [move]))
```
Adds the new state to the back of the queue, with the moves used to reach it.

### Output

```
Start: ((3, 2, 1), (), ())
Move disk 1 from A to C: ((3, 2), (), (1,))
Move disk 2 from A to B: ((3,), (2,), (1,))
Move disk 1 from C to B: ((3,), (2, 1), ())
Move disk 3 from A to C: ((), (2, 1), (3,))
Move disk 1 from B to A: ((1,), (2,), (3,))
Move disk 2 from B to C: ((1,), (), (3, 2))
Move disk 1 from A to C: ((), (), (3, 2, 1))
Total moves: 7
```

---

## 3. Write-up

### Problem Statement

Implement Tower of Hanoi by State Space Search and display the sequence of legal moves from the initial state to the goal state.

### Objectives

1. To understand problem formulation using states, operators, initial state, goal state and path cost.
2. To represent the Tower of Hanoi as a state space search problem.
3. To implement a search that generates only legal successor states and finds a solution path.

### Theory

**State space search:** A problem-solving method in which every possible configuration is a state. Operators are applied to states to generate successors, until a state satisfying the goal is reached. The solution is the sequence of operators from the initial state to the goal.

**Problem formulation:**

| Component | Tower of Hanoi |
|---|---|
| Initial state | All disks on peg A, largest at the bottom |
| Goal state | All disks on peg C in the same order |
| Operators | Move a top disk to another peg, if it obeys the size rule |
| Path cost | 1 for each legal move |

**Minimum moves:** n disks need 2^n - 1 moves, so 3 disks need 7.

**Search strategy:** BFS guarantees the shortest sequence, because every move has equal cost. A visited set avoids repeating states.

**Algorithm:**

1. Create the initial state and goal state.
2. Insert the initial state in a queue and mark it visited.
3. Remove the next state from the queue.
4. If it is the goal, display the moves and stop.
5. For every pair of pegs, check whether the move is legal.
6. Generate the new state. If it is unvisited, mark it visited and add it to the queue.
7. Repeat from step 3.

### Conclusion

The Tower of Hanoi was formulated and solved as a state space search using BFS. The program generated only legal moves, avoided repeated states and found the optimal solution of 7 moves for 3 disks.

---

## 4. Viva Questions

**1. What is a state space?**
The set of all states that can be reached from the initial state by applying operators.

**2. What are the initial and goal states here?**
Initial: all disks on A. Goal: all disks on C in the same order.

**3. Which moves are legal?**
One top disk moves at a time, and it can only go on an empty peg or a larger disk.

**4. Why is cycle checking useful?**
Without it, the search can repeat states forever, such as moving a disk back and forth.

**5. How is the path cost calculated?**
Each legal move costs 1, so the path cost is the number of moves.

**6. What is the minimum number of moves for n disks?**
2^n - 1.

**7. Why does BFS find an optimal solution here?**
It explores states by increasing number of moves, and all moves cost the same, so the first goal reached uses the fewest moves.

**8. What is the difference between a state and an operator?**
A state is a configuration of the problem. An operator is an action that changes one state into another.

**9. How can parent pointers reconstruct the path?**
Each state stores the state it came from, and following them back from the goal gives the path. My program instead stores the move list with each state, which does the same job.

**10. What is the complexity of the recursive solution?**
Time is O(2^n), because it makes 2^n - 1 moves. Space is O(n) for the recursion depth.

**11. How many states exist for n disks?**
3^n, since each disk can be on any of 3 pegs and the order on a peg is fixed by size. For 3 disks that is 27.

**12. What is the complexity of your BFS?**
Time and space are O(3^n), because in the worst case it visits every state.

**13. Why did you use BFS and not recursion?**
The syllabus asks for state space search. Recursion uses the known formula for the solution, whereas BFS searches through states.

**14. Why are tuples used for the state?**
Tuples cannot be changed, so they can be stored in a set. Lists cannot.

**15. How does the code stop a large disk going on a small disk?**
The check `disk < state[destination][-1]` allows the move only if the disk is smaller than the top disk there.

**16. Why is a queue used?**
First in, first out makes the search go level by level.

**17. Could DFS solve this problem?**
Yes, with cycle checking, but its solution may be longer than 7 moves.

**18. Is this search informed or uninformed?**
Uninformed, because it uses no heuristic.

**19. Why does the code use `state[source][-1]`?**
Index -1 gives the last item, which is the top disk in this representation.

**20. What is the recurrence for the number of moves?**
T(n) = 2T(n - 1) + 1, which solves to 2^n - 1. Move n - 1 disks aside, move the largest, then move n - 1 disks on top of it.
