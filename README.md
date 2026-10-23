# Exam Hall Seat Allocation System

A Python-based DAA mini-project that generates examination seating arrangements using a **Randomized Greedy Algorithm**. The system aims to minimize adjacent students from the same division by checking all eight directions, including diagonals.

## Features

* Automatic seat allocation
* Add and delete students
* Configure hall rows and columns
* Find a student's seat using roll number
* Export seating arrangements to CSV
* Generate alternative seating arrangements

## Technologies Used

* Python 3
* Tkinter
* Randomized Greedy Algorithm

## Project Structure

```text
smart-exam-seat-allocation/
├── main.py
├── gui.py
├── algorithm.py
├── data.py
├── README.md
└── .gitignore
```

## How to Run

Make sure Python 3 is installed.

```bash
python main.py
```

No external Python packages are required.

## Algorithm

The algorithm evaluates available seats and prioritizes those with fewer same-division neighbours. If multiple seats have the same score, it selects one randomly.

The algorithm checks horizontal, vertical, and diagonal neighbours. Randomization can produce different seating arrangements, but a globally optimal arrangement is not guaranteed.

## Complexity Analysis

Let `S` be the number of students and `H` be the total number of seats.

* **Time Complexity:** O(SH + S log S + H)
* **Space Complexity:** O(S + H)
