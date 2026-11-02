# Practical 6: Depth First Search for the Water Jug Problem

Syllabus reference: Part B, Assignment 2

---

## 1. The Problem and Its Solution

### Diagram 1: The problem

```
      |     |          |     |
      |     |          |     |          Goal: exactly 2 litres
      |     |          |     |          in one jug, the other empty.
      |     |          +-----+
      +-----+          3 litres
      4 litres

   State = (water in 4-litre jug, water in 3-litre jug)
   Start = (0, 0)         Goal = (2, 0) or (0, 2)
```

### Diagram 2: The six possible actions

```
   (x, y)  --- Fill 4-litre jug ------->  (4, y)
   (x, y)  --- Fill 3-litre jug ------->  (x, 3)
   (x, y)  --- Empty 4-litre jug ------>  (0, y)
   (x, y)  --- Empty 3-litre jug ------>  (x, 0)
   (x, y)  --- Pour 4-litre into 3 ---->  as much as fits in the 3-litre jug
   (x, y)  --- Pour 3-litre into 4 ---->  as much as fits in the 4-litre jug
```

### Diagram 3: The path DFS takes in this program

The newest state on the stack is explored first, so the search goes deep before trying the other branches.

```
                 (0,0)
                /     \
           (4,0)       (0,3)  <- explored first
      not explored     /    \
                  (4,3)      (3,0)  <- explored first
           not explored        |
                             (3,3)   Fill the 3-litre jug
                               |
                             (4,2)   Pour 3-litre into 4-litre
                               |
                             (0,2)   Empty the 4-litre jug: GOAL
```

| Step | Action | State |
|---|---|---|
| Start | | (0, 0) |
| 1 | Fill the 3-litre jug | (0, 3) |
| 2 | Pour the 3-litre jug into the 4-litre jug | (3, 0) |
| 3 | Fill the 3-litre jug | (3, 3) |
| 4 | Pour into the 4-litre jug until full, leaving 2 litres | (4, 2) |
| 5 | Empty the 4-litre jug | (0, 2) |

### Explain the problem in words (viva answer)

There are a 4-litre jug and a 3-litre jug, both empty, with no measuring marks and an unlimited water supply. We have to get exactly 2 litres in one jug. The only actions are filling a jug, emptying a jug and pouring one jug into the other.

### Explain the solution in words (viva answer)

I represented each state as (x, y), where x and y are the water in the 4-litre and 3-litre jugs, and solved it using Depth First Search with a stack.

The program takes the top state from the stack and checks if it is the goal. Otherwise, it generates all six possible next states, and pushes the unvisited ones on the stack. Since the last one pushed is taken next, the search keeps going deeper along one branch. If a branch has no new states, the next state on the stack comes from an earlier point, which is the backtracking.

The solution found takes 5 moves and ends at (0, 2). DFS does not guarantee the shortest path in general.

---

## 2. Code Explanation

```python
start = (0, 0)
```
The initial state, with both jugs empty. A tuple can be stored in a set.

```python
goal_states = [(2, 0), (0, 2)]
```
The two states that count as success.

```python
stack = [(start, [start])]
```
A Python list used as a stack. Each entry holds a state and the path taken to reach it.

```python
visited = {start}
```
Remembers states already seen. This stops the search from going round in circles.

```python
while stack:
```
Continues while states remain. An empty stack would mean no solution exists.

```python
    state, path = stack.pop()
```
`pop` removes the last item added. Last in, first out is what makes the search depth first.

```python
    if state in goal_states:
```
Checks whether this state is a goal.

```python
        print("Solution path:", path)
```
Prints the states from start to goal.

```python
        print("Moves:", len(path) - 1)
```
The path includes the start state, so moves are one less than its length.

```python
        break
```
Stops as a solution has been found.

```python
    four_litre, three_litre = state
```
Splits the state into two clearly named amounts.

```python
    pour_to_three = min(four_litre, 3 - three_litre)
```
Calculates how much can be poured into the 3-litre jug. It is limited by the water available and the space left, so the smaller value is taken.

```python
    pour_to_four = min(three_litre, 4 - four_litre)
```
The same calculation for pouring into the 4-litre jug.

```python
    next_states = [(4, three_litre),
```
Action 1: fill the 4-litre jug.

```python
                   (four_litre, 3),
```
Action 2: fill the 3-litre jug.

```python
                   (0, three_litre),
```
Action 3: empty the 4-litre jug.

```python
                   (four_litre, 0),
```
Action 4: empty the 3-litre jug.

```python
                   (four_litre - pour_to_three, three_litre + pour_to_three),
```
Action 5: pour from the 4-litre jug into the 3-litre jug.

```python
                   (four_litre + pour_to_four, three_litre - pour_to_four)]
```
Action 6: pour from the 3-litre jug into the 4-litre jug.

```python
    for next_state in next_states:
```
Checks each state produced by the six actions.

```python
        if next_state not in visited:
```
Skips states already seen, including actions that changed nothing.

```python
            visited.add(next_state)
```
Marks the state as seen when it is pushed, so it is not pushed twice.

```python
            stack.append((next_state, path + [next_state]))
```
Pushes the new state on the stack with its extended path.

### Output

```
Solution path: [(0, 0), (0, 3), (3, 0), (3, 3), (4, 2), (0, 2)]
Moves: 5
```

---

## 3. Write-up

### Problem Statement

Use DFS for problem solving. Examples can be the water jug problem, Missionaries and Cannibals, maze solving, blocks world, etc. Here, DFS is implemented for the water jug problem.

### Objectives

1. To understand the concept of uninformed (blind) search techniques.
2. To understand Depth First Search for solving a problem.
3. To implement DFS for a problem-solving task and obtain the solution path.

### Theory

**Depth First Search:** An uninformed search that goes as deep as possible along one branch before backtracking to try another. It uses a LIFO stack or recursion. A visited set avoids repeating states when the state space has cycles.

**Water jug formulation:**

| Component | Water jug problem |
|---|---|
| State | (x, y), water in the 4-litre and 3-litre jugs |
| Initial state | (0, 0) |
| Goal state | (2, 0) or (0, 2) |
| Actions | Fill, empty or pour between jugs |

**Advantages:** It is simple to implement, often needs less memory than BFS, can reach deep solutions quickly, and is useful for maze solving and state space exploration.

**Limitations:** It may not find the shortest solution, can get stuck in a deep branch without visited checks or a depth limit, and depends on the order in which states are explored.

**Algorithm:**

1. Define the initial state and goal states.
2. Create a stack and a visited set.
3. Push the initial state and mark it visited.
4. Pop the top state.
5. If it is a goal, display the path and stop.
6. Generate all next states using the six actions.
7. Mark each unvisited state as visited and push it on the stack.
8. Repeat from step 4 until a goal is found or the stack is empty.

### Conclusion

DFS was implemented for the water jug problem as a state space search. It explored one branch deeply using a stack, avoided repeated states with a visited set, and reached the goal (0, 2) in 5 moves.

---

## 4. Viva Questions

**1. What is Depth First Search?**
An uninformed search that explores as deep as possible along a branch before backtracking.

**2. Is DFS informed or uninformed?**
Uninformed, as it uses no heuristic.

**3. Which data structure does DFS use?**
A LIFO stack, or recursion, which uses the call stack.

**4. What is the difference between DFS and BFS?**
DFS goes deep with a stack and may not find the shortest path. BFS goes level by level with a queue and finds the fewest steps.

**5. How is DFS applied to the water jug problem?**
Each (x, y) is a state and the six actions give the next states. DFS follows one sequence deeply until it reaches the goal or runs out of new states.

**6. What is backtracking in DFS?**
Returning to an earlier state to try another option when the current branch cannot continue.

**7. Where does backtracking happen in your code?**
No explicit step is written. When a state adds nothing new, the next `pop` returns an older state that was waiting on the stack.

**8. Does DFS always find the shortest path?**
No. It returns the first path it reaches, which depends on the order states are explored.

**9. Why is a visited set required?**
States repeat in this problem, such as filling and then emptying a jug. Without the set, DFS could loop forever.

**10. What are the applications of DFS in AI?**
Maze solving, puzzle solving, state space exploration, planning and game tree search.

**11. What are the limitations of DFS?**
It may give a longer path, and without visited checks or a depth limit it can get stuck in deep or endless branches.

**12. What is the time and space complexity of DFS?**
Time is O(b^m), where b is the branching factor and m is the maximum depth. Space is usually lower than BFS: O(bm) for a plain DFS, though my visited set can hold every state seen.

**13. Is DFS complete?**
It is complete on a finite state space with visited checking. Without this, it may not terminate.

**14. How many states are possible in this problem?**
At most 5 x 4 = 20 combinations, since x is 0 to 4 and y is 0 to 3. Not all of them can be reached.

**15. Why is `min` used in the pour calculation?**
Poured water is limited by the water available and the space left, so the smaller of the two is used.

**16. Give an example of the pour calculation.**
At (3, 3), pouring into the 4-litre jug gives min(3, 4 - 3) = 1 litre, resulting in (4, 2).

**17. Why does (0, 3) get explored before (4, 0)?**
(4, 0) is pushed first and (0, 3) next. The stack gives the most recently pushed state first.

**18. How can you tell if a solution exists?**
A target is reachable if it is no larger than the bigger jug and divides evenly by the GCD of the jug sizes. Here GCD(4, 3) = 1, and 2 is divisible by 1.

**19. What is a state space?**
The set of all states reachable from the initial state by applying the actions.

**20. What other problems can DFS solve?**
Missionaries and Cannibals, maze solving and blocks world.
