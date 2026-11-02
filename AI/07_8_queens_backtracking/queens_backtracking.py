# Backtracking Search for the 8-Queens Problem


def is_safe(queens, column):
    row = len(queens)
    for old_row in range(row):
        if queens[old_row] == column or abs(queens[old_row] - column) == row - old_row:
            return False
    return True


def place_queens(queens):
    if len(queens) == 8:
        return True
    for column in range(1, 9):
        if is_safe(queens, column):
            queens.append(column)
            if place_queens(queens):
                return True
            queens.pop()
    return False


queens = []
place_queens(queens)
print("Solution (column of the queen in each row):", queens)
for column in queens:
    print("." * (column - 1) + "Q" + "." * (8 - column))
