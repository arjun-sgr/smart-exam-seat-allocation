# Exam Hall Seat Allocation System

## Main DAA Algorithm
**Randomized Greedy Algorithm**

### Files
- `main.py` -> starts the program
- `gui.py` -> screen and buttons
- `data.py` -> student data
- `algorithm.py` -> DAA algorithm

### Important feature
Each time **Generate Allocation** is clicked, the program can create a different valid seating arrangement.

It does this by:
1. Randomly shuffling students with equal priority.
2. Randomly shuffling free seats.
3. Randomly choosing between equally good seats.

It is still a **Greedy Algorithm** because each student gets the best current seat according to the score.

### Run
```bash
python main.py
```

No external package is required.

### Viva line
"Our project uses a randomized greedy algorithm. For every student, we calculate a score for each free seat. Same-division neighbours get a high penalty. We choose the best current seat. Random tie-breaking gives a different valid arrangement when Generate is clicked again."

### Complexity
For `S` students and `H` seats:
- Time: **O(S × H)**
- Space: **O(S + H)**
