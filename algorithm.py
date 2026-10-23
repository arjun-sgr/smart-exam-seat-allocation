# algorithm.py
# Main DAA part.
# Algorithm: Randomized Greedy Seat Allocation
# Neighbours are checked in all 8 directions, including diagonals.

import random


def get_neighbours(row, col, rows, cols):
    """Return valid seats in all 8 surrounding directions."""
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # upper-left, up, upper-right
        (0, -1),           (0, 1),   # left, right
        (1, -1),  (1, 0),  (1, 1)    # lower-left, down, lower-right
    ]

    result = []

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < rows and 0 <= new_col < cols:
            result.append((new_row, new_col))

    return result


def seat_score(row, col, student, allocation, rows, cols):
    """
    Lower score is better.
    First minimize same-division neighbours in all 8 directions.
    If tied, prefer seats with fewer occupied neighbours.
    """
    same_division = 0
    occupied = 0

    for seat in get_neighbours(row, col, rows, cols):
        neighbour = allocation.get(seat)

        if neighbour is not None:
            occupied += 1

            if neighbour["division"] == student["division"]:
                same_division += 1

    # Tuple comparison prioritizes same-division conflicts strictly:
    # (0, 8) is preferred over (1, 0).
    return (same_division, occupied)


def allocate_seats(students, rows, cols):
    """
    Randomized Greedy Algorithm.

    1. Give larger divisions priority.
    2. Check all currently empty seats for each student.
    3. Choose a seat with the fewest same-division neighbours.
    4. If tied, prefer fewer occupied neighbours.
    5. Randomly choose among equally good seats.
    """
    if rows < 1 or cols < 1 or len(students) > rows * cols:
        return None

    # Count students in each division.
    division_count = {}

    for student in students:
        division = student["division"]
        division_count[division] = division_count.get(division, 0) + 1

    # Shuffle students, then put larger divisions first.
    # This preserves randomness when division sizes are equal.
    ordered_students = list(students)
    random.shuffle(ordered_students)
    ordered_students.sort(
        key=lambda student: division_count[student["division"]],
        reverse=True
    )

    # Create and shuffle all seats.
    free_seats = [
        (row, col)
        for row in range(rows)
        for col in range(cols)
    ]
    random.shuffle(free_seats)

    allocation = {}

    for student in ordered_students:
        best_score = None
        best_seats = []

        # Score each available seat.
        for row, col in free_seats:
            score = seat_score(
                row, col, student, allocation, rows, cols
            )

            if best_score is None or score < best_score:
                best_score = score
                best_seats = [(row, col)]
            elif score == best_score:
                best_seats.append((row, col))

        # Random tie-break means another click can make a new layout.
        chosen_seat = random.choice(best_seats)
        allocation[chosen_seat] = student
        free_seats.remove(chosen_seat)

    return allocation


def count_same_division_pairs(allocation, rows, cols):
    """
    Count same-division neighbour pairs in 8 directions.
    Each pair is counted exactly once by checking only:
    right, down-left, down, and down-right.
    """
    count = 0
    directions_to_check = [
        (0, 1),    # right
        (1, -1),   # down-left diagonal
        (1, 0),    # down
        (1, 1)     # down-right diagonal
    ]

    for (row, col), student in allocation.items():
        for dr, dc in directions_to_check:
            neighbour = allocation.get((row + dr, col + dc))

            if (
                neighbour is not None
                and neighbour["division"] == student["division"]
            ):
                count += 1

    return count
