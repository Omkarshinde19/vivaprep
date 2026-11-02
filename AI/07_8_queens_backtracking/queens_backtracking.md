# Practical 7: Backtracking Search for the 8-Queens Problem

Syllabus reference: Part B, Assignment 3

---

## 1. The Problem and Its Solution

### Diagram 1: How a queen attacks

```
    1 2 3 4 5 6 7 8
 1  \ . . | . . / .
 2  . \ . | . / . .
 3  . . \ | / . . .
 4  - - - Q - - - -      A queen attacks along its row,
 5  . . / | \ . . .      its column and both diagonals.
 6  . / . | . \ . .
 7  / . . | . . \ .
 8  . . . | . . . \
```

### Diagram 2: The solution found

```
          Columns
         1 2 3 4 5 6 7 8
 Row 1   Q . . . . . . .
 Row 2   . . . . Q . . .
 Row 3   . . . . . . . Q
 Row 4   . . . . . Q . .
 Row 5   . . Q . . . . .
 Row 6   . . . . . . Q .
 Row 7   . Q . . . . . .
 Row 8   . . . Q . . . .

 Solution list: [1, 5, 8, 6, 3, 7, 2, 4]
```

### Diagram 3: How backtracking works

```
 Row 1: place Q at column 1
    |
 Row 2: columns 1, 2 unsafe -> column 3 is safe -> place Q
    |
 Row 3: try the safe columns -> place Q
    |
   ...
    |
 Row k: every column is unsafe  --> DEAD END
    |
    v
 BACKTRACK: remove the queen in row k - 1 and try its next column
    |
    v
 Continue forward again, until all 8 rows have a queen
```

### Diagram 4: The safety check

```
 New queen at (row, column), old queen at (old_row, old_column)

 Same column:    column == old_column
 Same diagonal:  |old_column - column| == |row - old_row|

 Example: old queen (1, 1), new queen (3, 3)
          |1 - 3| = 2 and |3 - 1| = 2, so they share a diagonal: UNSAFE
```

### Explain the problem in words (viva answer)

We have to place eight queens on an 8x8 chessboard so that no two attack each other. A queen attacks along its row, column and diagonals. So no two queens may share a row, a column or a diagonal.

### Explain the solution in words (viva answer)

I modelled it as a Constraint Satisfaction Problem. There is one variable for each row, its domain is the columns 1 to 8, and the constraints are no shared column and no shared diagonal. Having one queen per row automatically handles the row constraint.

I solved it using recursive backtracking. For the current row, the program tries each column in order and checks whether it is safe. If it is, the queen is placed and the function moves to the next row. If no column works, the function returns False, the previous queen is removed, and that row tries its next column. When all eight queens are placed, the solution is printed.

The result is [1, 5, 8, 6, 3, 7, 2, 4].

---

## 2. Code Explanation

```python
def is_safe(queens, column):
```
Checks if a queen can go in this column of the next row. `queens` holds the column of the queen in each row so far.

```python
    row = len(queens)
```
The number of queens placed gives the index of the current row.

```python
    for old_row in range(row):
```
Compares the new position with every queen already placed.

```python
        if queens[old_row] == column or abs(queens[old_row] - column) == row - old_row:
```
The first part is the column constraint. The second is the diagonal constraint: two queens share a diagonal if their column and row distances are equal. Rows need no check, as there is one queen per row.

```python
            return False
```
One conflict is enough to reject this column, so it stops checking.

```python
    return True
```
No queen conflicted, so the position is safe.

```python
def place_queens(queens):
```
The recursive backtracking function. Each call handles one row.

```python
    if len(queens) == 8:
```
The base case: when eight queens are placed, the problem is solved.

```python
        return True
```
Reports success to the previous call.

```python
    for column in range(1, 9):
```
Tries the domain values, columns 1 to 8.

```python
        if is_safe(queens, column):
```
Only explores positions that obey the constraints. This rejects bad partial solutions early.

```python
            queens.append(column)
```
Places the queen, assigning a value to this row's variable.

```python
            if place_queens(queens):
```
Recursively solves the remaining rows.

```python
                return True
```
If the rest succeeded, it passes success upward and keeps the queens in place.

```python
            queens.pop()
```
This is the backtracking step. The rest could not be solved, so this queen is removed and the next column is tried.

```python
    return False
```
No column works for this row, which tells the previous row to change its queen.

```python
queens = []
```
Starts with an empty board.

```python
place_queens(queens)
```
Starts the search. The list is changed inside the function, so it holds the solution afterwards.

```python
print("Solution (column of the queen in each row):", queens)
```
Prints the solution as a list.

```python
for column in queens:
```
Goes through the rows to draw the board.

```python
    print("." * (column - 1) + "Q" + "." * (8 - column))
```
Prints one row: dots before the queen, the queen, then dots after it.

### Output

```
Solution (column of the queen in each row): [1, 5, 8, 6, 3, 7, 2, 4]
Q.......
....Q...
.......Q
.....Q..
..Q.....
......Q.
.Q......
...Q....
```

---

## 3. Write-up

### Problem Statement

Implement backtracking search to solve the 8-Queens constraint satisfaction problem. The program should place eight queens on an 8x8 chessboard such that no two queens attack each other.

### Objectives

1. To understand the concept of Constraint Satisfaction Problems.
2. To understand the backtracking search technique for solving a CSP.
3. To formulate the 8-Queens problem using variables, domains and constraints.
4. To implement backtracking search and obtain a valid 8-Queens solution.

### Theory

**Constraint Satisfaction Problem:** A problem in which variables must be assigned values from their domains while satisfying a set of constraints.

**CSP representation of 8-Queens:**

| Component | 8-Queens |
|---|---|
| Variables | Q1 to Q8, where Qi is the queen in row i |
| Domain | {1, 2, 3, 4, 5, 6, 7, 8}, the column number |
| Row constraint | Automatically met, as each variable is one row |
| Column constraint | No two queens have the same column |
| Diagonal constraint | For queens Qi and Qj, \|Qi - Qj\| is not equal to \|i - j\| |

**Backtracking search:** It assigns a value to one variable at a time. If a value violates a constraint, another value is tried. If no value is possible, the algorithm returns to the previous variable and changes it.

**Advantages:** It is systematic, rejects invalid partial assignments early, is simple to write using recursion, and applies to N-Queens, Sudoku, graph colouring and other CSPs.

**Limitations:** The worst-case search can be large, performance depends on the order of variables and values, and larger problems may need forward checking or MRV.

**Algorithm:**

1. Start with an empty solution list at row 1.
2. Try each column from 1 to 8 for the current row.
3. Check whether the position is safe.
4. If safe, place the queen and move to the next row.
5. If all eight rows are assigned, a solution is found.
6. If no column is safe, remove the queen from the previous row and try its next column.
7. Display the solution and chessboard.

### Conclusion

The 8-Queens problem was formulated as a Constraint Satisfaction Problem. Backtracking search placed queens row by row, checked the column and diagonal constraints, and went back whenever a partial assignment could not continue. It produced the valid arrangement [1, 5, 8, 6, 3, 7, 2, 4].

---

## 4. Viva Questions

**1. What is a Constraint Satisfaction Problem?**
A problem where variables must get values from their domains while satisfying all constraints.

**2. What are the variables and domains in 8-Queens?**
The variables are Q1 to Q8, one per row. The domain of each is columns 1 to 8.

**3. What are the constraints?**
No two queens may share a column or a diagonal. Rows are handled by the representation.

**4. What is backtracking search?**
A search that builds a solution step by step and undoes the last choice when it cannot continue.

**5. Why is backtracking required here?**
An early queen placement can make a later row impossible, so that earlier choice must be changed.

**6. How do you check whether a queen can be placed safely?**
Compare it with all earlier queens. It is unsafe if any has the same column or an equal row and column distance.

**7. What is the diagonal constraint?**
|Qi - Qj| must not equal |i - j|, as equal distances mean they share a diagonal.

**8. Why is no row check needed?**
Exactly one queen is placed for each row.

**9. What is the difference between backtracking and brute force?**
Brute force tests complete arrangements. Backtracking rejects a partial arrangement as soon as it breaks a constraint, skipping everything that would follow from it.

**10. Why is recursion used?**
Each row is the same smaller problem, and returning from a call naturally goes back to the previous row.

**11. Which line performs the backtracking?**
`queens.pop()` removes the queen after the remaining rows fail.

**12. What is the base case?**
`len(queens) == 8`, when all queens are placed.

**13. How many solutions does 8-Queens have?**
92 in total, or 12 if rotations and reflections are treated as the same.

**14. Why does your program print only one solution?**
It returns True as soon as the first solution is found. It would need to continue instead of returning to find all 92.

**15. How does `queens` represent the board?**
Its index is the row and its value is the column, so one list is enough.

**16. What is the time and space complexity?**
Time is about O(N!) in the worst case, since each row has fewer columns available. Space is O(N) for the list and the recursion.

**17. What are forward checking and MRV?**
Forward checking removes values that conflict with an assignment from the future variables' domains. MRV (Minimum Remaining Values) picks the variable with the fewest legal values next.

**18. Is 8-Queens solvable for all N?**
No. Solutions exist for N = 1 and for all N of 4 or more, but not for N = 2 or N = 3.

**19. What search does backtracking resemble?**
Depth First Search, because it goes deep on one assignment before returning.

**20. What are some applications of backtracking in AI?**
Sudoku, graph colouring, scheduling, crosswords and other constraint problems.
