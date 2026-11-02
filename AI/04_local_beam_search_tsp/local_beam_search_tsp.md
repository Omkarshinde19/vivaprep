# Practical 4: Local Beam Search for the Travelling Salesman Problem

Syllabus reference: Part A, Assignment 7

---

## 1. The Problem and Its Solution

### Diagram 1: The distance table

```
        A    B    C    D    E    F
   A    0   10   15   20   18   12
   B   10    0   35   25   17   28
   C   15   35    0   30   28   20
   D   20   25   30    0   22   16
   E   18   17   28   22    0   14
   F   12   28   20   16   14    0
```

### Diagram 2: The best tour found (distance 100)

```
              15                20
        A ----------> C ----------> F
        ^                           |
     10 |                           | 16
        |                           v
        B <---------- E <---------- D
              17            22

   15 + 20 + 16 + 22 + 17 + 10 = 100
```

### Diagram 3: How local beam search works (k = 4)

```
 Beam (4 tours)          Starting tours from the program, with costs:
 +-----------------+       A C B F E D   cost 134
 | 4 current tours |       A E F D C B   cost 123
 +-----------------+       A B E F C D   cost 111
          |                A F B D C E   cost 141
          v
 +-------------------------------+
 | Swap two cities in every tour |    each tour gives 10 neighbours
 | Remove duplicate tours        |    (a set does this)
 +-------------------------------+
          |
          v
 +-------------------------------+
 | Sort all neighbours by cost   |
 | Keep the best 4 as new beam   |
 +-------------------------------+
          |
          v
 Update the global best, then repeat for the next iteration
```

### Diagram 4: A swap move

```
 Tour:           A  B  E  F  C  D
 Swap E and C:         ^     ^
 New tour:       A  B  C  F  E  D
```

### Explain the problem in words (viva answer)

The Travelling Salesman Problem has a set of cities and the distance between each pair. The salesman starts from a city, visits every other city exactly once and returns to the start. The aim is to find the tour with the smallest total distance. The number of possible tours grows extremely fast with more cities, so checking them all becomes impractical.

### Explain the solution in words (viva answer)

I used local beam search. Each state is a complete tour, and its cost is its total distance, including the return to the start.

The program starts with 4 random tours, called the beam. In each iteration, it creates neighbours of all 4 tours by swapping two cities, removes duplicates, and keeps only the best 4 as the new beam. It also remembers the best tour seen so far, called the global best.

The program found a tour of distance 100. I also checked all 120 possible tours starting from A, and 100 is the true minimum for this table.

### Experiment results

Each beam width was run with random seeds 1 to 10, for 5 iterations each:

| Beam width k | Best cost | Average cost |
|---|---:|---:|
| 1 | 100 | 100 |
| 2 | 100 | 100 |
| 4 | 100 | 100 |

Every run reached the optimum, as this 6-city problem is small. On bigger problems, a larger beam width usually helps more, but this table does not show that.

---

## 2. Code Explanation

```python
import random
```
Used to create the random starting tours.

```python
city_names = "ABCDEF"
```
Converts city numbers 0 to 5 to letters for the output.

```python
distances = [[0, 10, 15, 20, 18, 12],
             [10, 0, 35, 25, 17, 28],
             [15, 35, 0, 30, 28, 20],
             [20, 25, 30, 0, 22, 16],
             [18, 17, 28, 22, 0, 14],
             [12, 28, 20, 16, 14, 0]]
```
The distance table from the lab material. `distances[0][1]` is the distance from A to B.

```python
beam_width = 4
```
This is k, the number of tours kept in each iteration.

```python
total_iterations = 5
```
This is the stopping condition: the search runs for a fixed 5 iterations.

```python
def tour_cost(tour):
```
This is the evaluation function. It returns a tour's total distance, and lower is better.

```python
    cost = 0
```
Starts the total at zero.

```python
    for position in range(6):
```
Goes through all 6 cities in the tour.

```python
        cost = cost + distances[tour[position - 1]][tour[position]]
```
Adds the distance from the previous city to this city. When position is 0, `tour[-1]` is the last city, so this also adds the return trip to the start.

```python
    return cost
```
Returns the total distance.

```python
random.seed(1)
```
Makes the random numbers the same on every run, so the output can be repeated. Changing the seed gives different starting tours.

```python
beam = []
```
The beam starts as an empty list.

```python
for count in range(beam_width):
```
Repeats once for each starting tour.

```python
    beam.append(tuple([0] + random.sample([1, 2, 3, 4, 5], 5)))
```
Creates a random tour. City A (0) stays first, and `random.sample` shuffles the other five. It is a tuple so that duplicates can be removed using a set.

```python
best_tour = min(beam, key=tour_cost)
```
Stores the cheapest starting tour as the first global best. `key=tour_cost` compares tours by cost.

```python
for iteration in range(1, total_iterations + 1):
```
Runs the main search, counting iterations from 1.

```python
    successors = set()
```
Collects neighbouring tours. A set removes duplicates automatically.

```python
    for tour in beam:
```
Generates neighbours from every tour in the beam, not just the best one. This is the main difference from hill climbing.

```python
        for first in range(1, 6):
```
Selects the first city to swap. It starts at 1, so A stays fixed at the start.

```python
            for second in range(first + 1, 6):
```
Selects the second city. Starting after `first` means each pair is used only once.

```python
                new_tour = list(tour)
```
Makes a changeable copy of the tour.

```python
                new_tour[first], new_tour[second] = new_tour[second], new_tour[first]
```
Swaps the two cities. The result is still a valid tour, as each city still appears once.

```python
                successors.add(tuple(new_tour))
```
Stores the neighbour. It is converted to a tuple because sets cannot store lists.

```python
    beam = sorted(successors, key=tour_cost)[:beam_width]
```
Sorts all neighbours from lowest to highest cost and keeps the best k. This is the selection step of beam search.

```python
    if tour_cost(beam[0]) < tour_cost(best_tour):
```
`beam[0]` is the best in the new beam. It is compared with the best tour seen so far.

```python
        best_tour = beam[0]
```
Updates the global best. This record is needed because a later beam can be worse than an earlier one.

```python
    print("Iteration", iteration, "| Beam best:", tour_cost(beam[0]), "| Global best:", tour_cost(best_tour))
```
Shows the progress for each iteration.

```python
route = [city_names[city] for city in best_tour]
```
Converts the city numbers in the best tour to letters.

```python
print("Best tour:", route, "back to A | Distance:", tour_cost(best_tour))
```
Prints the final tour and its total distance.

### Output

```
Iteration 1 | Beam best: 100 | Global best: 100
Iteration 2 | Beam best: 100 | Global best: 100
Iteration 3 | Beam best: 100 | Global best: 100
Iteration 4 | Beam best: 100 | Global best: 100
Iteration 5 | Beam best: 100 | Global best: 100
Best tour: ['A', 'C', 'F', 'D', 'E', 'B'] back to A | Distance: 100
```

---

## 3. Write-up

### Problem Statement

Implement Local Beam Search for the Travelling Salesman Problem (TSP), in which every city is visited exactly once and the salesman returns to the starting city.

### Objectives

1. To understand local search and population-based heuristic search techniques.
2. To implement local beam search using multiple candidate tours at every iteration.
3. To evaluate a TSP tour using total distance and compare the best solution across iterations.

### Theory

**Travelling Salesman Problem:** The objective is to find a minimum-cost Hamiltonian cycle, which is a tour that starts at one city, visits every other city exactly once and returns to the start. The problem is computationally difficult for large inputs, so heuristic methods are often used.

**Local search:** A search that moves from a current complete solution to neighbouring solutions, rather than building a path from a start state.

**Local beam search:** It keeps k states instead of one. In each iteration, successors of all k states are generated, and the best k become the next beam.

**Problem formulation:**

| Component | TSP with local beam search |
|---|---|
| State | A complete order of all cities, with a return to the first city |
| Initial states | k random tours with A fixed first |
| Successor function | Swap two cities |
| Evaluation function | Total length of the closed tour |
| Selection rule | Keep the k lowest-cost unique successors |

**Algorithm:**

1. Define the distance table, the beam width k and the number of iterations.
2. Generate k starting tours and store the lowest-cost one as the global best.
3. Generate neighbours for every tour in the beam.
4. Remove duplicates and sort by cost.
5. Keep the first k as the next beam.
6. Update the global best if the new beam's best is lower.
7. Repeat from step 3 for the set number of iterations.
8. Display the best tour and its distance.

### Conclusion

Local beam search was implemented for the TSP by keeping multiple tours and repeatedly selecting the best successors. On the given 6-city problem it found a tour of distance 100, which an exhaustive check confirmed to be optimal. Because it is a heuristic method, it does not guarantee an optimal tour on every problem.

---

## 4. Viva Questions

**1. What is the Travelling Salesman Problem?**
Finding the shortest tour that visits every city exactly once and returns to the start.

**2. Why is TSP called a combinatorial optimization problem?**
The aim is to find the best arrangement out of a finite but very large number of possible city orders.

**3. How many tours are there for n cities?**
With a fixed start, (n - 1)! ordered tours. For 6 cities that is 120, or 60 distinct tours if a tour and its reverse count as one.

**4. What is local search?**
A method that improves complete solutions by moving to neighbouring solutions, using little memory.

**5. How does local beam search differ from hill climbing?**
Hill climbing keeps one state. Local beam search keeps k states and chooses the next ones from all their successors.

**6. How is local beam search different from running k searches separately?**
Separate searches do not share information. In beam search, all successors compete, so the search focuses on the most promising tours.

**7. What is the role of beam width k?**
It sets how many tours are kept. A larger k explores more but costs more time and memory.

**8. What happens when k = 1?**
It behaves much like hill climbing, except it always moves to its best neighbour, even if that is worse.

**9. Why should duplicate tours be removed?**
Otherwise the same tour can fill several places in the beam, reducing variety.

**10. What neighbourhood operation did you use?**
Swapping two cities. Each tour has 10 neighbours, since there are 10 ways to pick 2 of the 5 movable cities.

**11. What is a 2-opt move and why is it useful?**
It reverses a segment of the tour. It is useful because it can remove crossing edges, which shortens the tour.

**12. Why is the return distance included?**
The tour must end at the starting city, so that edge is part of the real cost.

**13. How does your code include the return distance?**
When position is 0, `tour[position - 1]` becomes `tour[-1]`, the last city, which adds the last-to-first edge.

**14. What is the difference between beam best and global best?**
Beam best is the best in the current iteration. Global best is the best seen in the whole run.

**15. Why is a global best needed?**
The search always moves to the best neighbours, even if they are worse, so a later beam can lose an earlier good tour.

**16. Does local beam search guarantee the optimal solution?**
No. It is a heuristic and can get stuck in a local minimum.

**17. What is a local minimum?**
A tour better than all its neighbours but not the best overall.

**18. How can random restarts or different beam widths improve the result?**
They start the search from different tours or keep more of them, giving more chances to escape poor regions.

**19. Why is `random.seed(1)` used?**
It gives the same random numbers on each run, so the result can be repeated and compared.

**20. What is the time complexity of your program?**
O(i x k x c^2 log(k x c^2)) approximately, where i is iterations, k is beam width and c is cities, because each iteration generates about k x c^2 neighbours and sorts them. Calculating each tour's cost adds another factor of c.
