# gui.py
# User interface.

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

from data import get_sample_students, find_student
from algorithm import allocate_seats, count_same_division_pairs

students = []
allocation = {}
rows = 4
cols = 5


def refresh_students():
    """Show students in the table."""
    for item in student_table.get_children():
        student_table.delete(item)

    for student in students:
        student_table.insert(
            "", "end",
            values=(
                student["roll"],
                student["name"],
                student["division"]
            )
        )


def draw_seats():
    """Draw the current seating arrangement."""
    canvas.delete("all")

    width = max(canvas.winfo_width(), 450)
    height = max(canvas.winfo_height(), 350)

    margin = 25
    cell_w = (width - 2 * margin) / cols
    cell_h = (height - 2 * margin) / rows

    for row in range(rows):
        for col in range(cols):
            x1 = margin + col * cell_w
            y1 = margin + row * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h

            student = allocation.get((row, col))

            if student:
                text = (
                    student["roll"] + "\n" +
                    student["name"] + "\n" +
                    student["division"]
                )
                fill = "#dceeff"
            else:
                text = "EMPTY"
                fill = "white"

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=fill,
                outline="#777777"
            )

            canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=text,
                font=("Arial", 9)
            )


def generate_allocation():
    """Run the DAA algorithm."""
    global rows, cols, allocation

    try:
        rows = int(rows_box.get())
        cols = int(cols_box.get())
    except ValueError:
        messagebox.showerror("Error", "Rows and columns must be numbers.")
        return

    if rows < 1 or cols < 1:
        messagebox.showerror("Error", "Rows and columns must be positive.")
        return

    if not students:
        messagebox.showwarning("Warning", "Add students first.")
        return

    allocation = allocate_seats(students, rows, cols)

    if allocation is None:
        messagebox.showerror(
            "Error",
            "Not enough seats for all students."
        )
        return

    draw_seats()

    pairs = count_same_division_pairs(allocation, rows, cols)

    status.config(
        text=(
            f"New allocation generated | Students: {len(students)} | "
            f"Seats: {rows * cols} | Same-division neighbouring pairs (8 directions): {pairs}"
        )
    )


def load_sample():
    """Load sample students."""
    global students
    students = get_sample_students()
    refresh_students()
    clear_allocation()
    status.config(text="Sample students loaded.")


def add_student():
    """Add one student."""
    roll = roll_box.get().strip()
    name = name_box.get().strip()
    division = division_box.get().strip()

    if not roll or not name or not division:
        messagebox.showwarning(
            "Missing data",
            "Enter Roll, Name and Division."
        )
        return

    if any(s["roll"] == roll for s in students):
        messagebox.showerror("Error", "Roll number already exists.")
        return

    students.append({
        "roll": roll,
        "name": name,
        "division": division
    })

    refresh_students()

    roll_box.delete(0, tk.END)
    name_box.delete(0, tk.END)

    status.config(text=f"Student {roll} added.")


def delete_selected():
    """Delete the selected student."""
    selected = student_table.selection()

    if not selected:
        messagebox.showinfo(
            "Select student",
            "Select a student first."
        )
        return

    roll = student_table.item(
        selected[0], "values"
    )[0]

    global students
    students = [s for s in students if s["roll"] != roll]

    refresh_students()
    clear_allocation()
    status.config(text=f"Student {roll} deleted.")


def clear_allocation():
    """Clear the current seating arrangement."""
    global allocation
    allocation = {}
    draw_seats()


def find_seat():
    """Find the seat of a student."""
    roll = search_box.get().strip()

    if not roll:
        messagebox.showwarning("Search", "Enter a roll number.")
        return

    student = find_student(students, roll)

    if student is None:
        messagebox.showerror("Not found", "Student not found.")
        return

    for (row, col), assigned in allocation.items():
        if assigned["roll"] == roll:
            messagebox.showinfo(
                "Seat Found",
                f"Name: {student['name']}\n"
                f"Roll: {student['roll']}\n"
                f"Division: {student['division']}\n"
                f"Seat: Row {row + 1}, Column {col + 1}"
            )
            return

    messagebox.showinfo(
        "No allocation",
        "Generate allocation first."
    )


def export_csv():
    """Export the current seating arrangement."""
    if not allocation:
        messagebox.showwarning(
            "Export",
            "Generate allocation first."
        )
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV file", "*.csv")]
    )

    if not path:
        return

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Hall", "Row", "Column",
            "Roll No", "Name", "Division"
        ])

        for (row, col), student in sorted(allocation.items()):
            writer.writerow([
                "Main Hall",
                row + 1,
                col + 1,
                student["roll"],
                student["name"],
                student["division"]
            ])

    messagebox.showinfo(
        "Success",
        "Allocation exported successfully."
    )


def start_app():
    """Create and run the main window."""
    global roll_box, name_box, division_box
    global rows_box, cols_box, student_table
    global canvas, status, search_box

    root = tk.Tk()
    root.title("Exam Hall Seat Allocation System")
    root.geometry("1100x720")

    tk.Label(
        root,
        text="Exam Hall Seat Allocation System",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    # Hall setup
    hall = ttk.LabelFrame(root, text="Hall Setup")
    hall.pack(fill="x", padx=15, pady=5)

    ttk.Label(hall, text="Rows:").pack(side="left", padx=5)
    rows_box = ttk.Entry(hall, width=5)
    rows_box.insert(0, "4")
    rows_box.pack(side="left", padx=5)

    ttk.Label(hall, text="Columns:").pack(side="left", padx=5)
    cols_box = ttk.Entry(hall, width=5)
    cols_box.insert(0, "5")
    cols_box.pack(side="left", padx=5)

    # Student input
    input_box = ttk.LabelFrame(root, text="Student")
    input_box.pack(fill="x", padx=15, pady=5)

    ttk.Label(input_box, text="Roll:").pack(side="left", padx=5)
    roll_box = ttk.Entry(input_box, width=10)
    roll_box.pack(side="left", padx=5)

    ttk.Label(input_box, text="Name:").pack(side="left", padx=5)
    name_box = ttk.Entry(input_box, width=15)
    name_box.pack(side="left", padx=5)

    ttk.Label(input_box, text="Division:").pack(side="left", padx=5)
    division_box = ttk.Entry(input_box, width=10)
    division_box.insert(0, "IT-A")
    division_box.pack(side="left", padx=5)

    ttk.Button(
        input_box, text="Add Student",
        command=add_student
    ).pack(side="left", padx=5)

    ttk.Button(
        input_box, text="Delete Selected",
        command=delete_selected
    ).pack(side="left", padx=5)

    ttk.Button(
        input_box, text="Load Sample",
        command=load_sample
    ).pack(side="left", padx=5)

    # Main area
    main = ttk.Frame(root)
    main.pack(fill="both", expand=True, padx=15, pady=5)

    left = ttk.LabelFrame(main, text="Students")
    left.pack(side="left", fill="both", expand=True, padx=(0, 5))

    student_table = ttk.Treeview(
        left,
        columns=("roll", "name", "division"),
        show="headings"
    )

    student_table.heading("roll", text="Roll")
    student_table.heading("name", text="Name")
    student_table.heading("division", text="Division")
    student_table.pack(fill="both", expand=True, padx=5, pady=5)

    right = ttk.LabelFrame(main, text="Seating Arrangement")
    right.pack(side="left", fill="both", expand=True, padx=(5, 0))

    canvas = tk.Canvas(right, bg="white")
    canvas.pack(fill="both", expand=True, padx=5, pady=5)
    canvas.bind("<Configure>", lambda event: draw_seats())

    # Actions
    actions = ttk.Frame(root)
    actions.pack(fill="x", padx=15, pady=5)

    ttk.Button(
        actions,
        text="Generate Allocation",
        command=generate_allocation
    ).pack(side="left", padx=5)

    ttk.Label(
        actions,
        text="Click Generate again for a new random arrangement."
    ).pack(side="left", padx=5)

    ttk.Label(actions, text="Search Roll:").pack(
        side="left", padx=(20, 5)
    )

    search_box = ttk.Entry(actions, width=10)
    search_box.pack(side="left", padx=5)

    ttk.Button(
        actions,
        text="Find Seat",
        command=find_seat
    ).pack(side="left", padx=5)

    ttk.Button(
        actions,
        text="Export CSV",
        command=export_csv
    ).pack(side="left", padx=5)

    status = ttk.Label(
        root,
        text="Ready. Click Load Sample.",
        relief="sunken",
        anchor="w"
    )
    status.pack(fill="x", padx=15, pady=(2, 10))

    load_sample()
    root.mainloop()
