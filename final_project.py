import sqlite3
import matplotlib.pyplot as plt


# ============================================================
# STUDENT PERFORMANCE & ANALYTICS SYSTEM
# ============================================================

DB_NAME = "final_student_performance.db"


# ------------------------------------------------------------
# 1. DATABASE SETUP
# ------------------------------------------------------------

def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        python_marks INTEGER NOT NULL,
        sql_marks INTEGER NOT NULL,
        dsa_marks INTEGER NOT NULL,
        total INTEGER NOT NULL,
        percentage REAL NOT NULL,
        result TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()


# ------------------------------------------------------------
# 2. ADD 10 DEMO STUDENTS
# ------------------------------------------------------------

def add_demo_students():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    # Students are added only once
    if count == 0:

        students = [
            ("Vinit", 92, 88, 95),
            ("Sataym", 78, 82, 75),
            ("Rohit", 85, 90, 88),
            ("Aryan", 72, 76, 80),
            ("Rajnish", 88, 84, 91),
            ("Aman", 81, 79, 86),
            ("Ankit", 94, 91, 89),
            ("Vishal", 69, 74, 71),
            ("Yash", 87, 93, 85),
            ("Sonu", 76, 80, 73)
        ]

        for name, python_marks, sql_marks, dsa_marks in students:

            total = python_marks + sql_marks + dsa_marks
            percentage = total / 3

            if percentage >= 40:
                result = "Pass"
            else:
                result = "Fail"

            cursor.execute("""
            INSERT INTO students
            (name, python_marks, sql_marks, dsa_marks,
             total, percentage, result)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                python_marks,
                sql_marks,
                dsa_marks,
                total,
                percentage,
                result
            ))

        connection.commit()

    connection.close()


# ------------------------------------------------------------
# 3. DISPLAY STUDENTS
# ------------------------------------------------------------

def display_students():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, name, python_marks, sql_marks,
           dsa_marks, total, percentage, result
    FROM students
    """)

    students = cursor.fetchall()
    connection.close()

    print("\n" + "=" * 95)
    print("                 STUDENT PERFORMANCE REPORT")
    print("=" * 95)

    print(
        f"{'ID':<5}"
        f"{'Name':<15}"
        f"{'Python':<10}"
        f"{'SQL':<10}"
        f"{'DSA':<10}"
        f"{'Total':<10}"
        f"{'%':<10}"
        f"{'Result':<10}"
    )

    print("-" * 95)

    for student in students:

        print(
            f"{student[0]:<5}"
            f"{student[1]:<15}"
            f"{student[2]:<10}"
            f"{student[3]:<10}"
            f"{student[4]:<10}"
            f"{student[5]:<10}"
            f"{student[6]:<10.2f}"
            f"{student[7]:<10}"
        )

    print("=" * 95)


# ------------------------------------------------------------
# 4. SEARCH STUDENT
# ------------------------------------------------------------

def search_student():

    try:
        student_id = int(input("\nEnter Student ID to search: "))
    except ValueError:
        print("Please enter a valid ID.")
        return

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, name, python_marks, sql_marks,
           dsa_marks, total, percentage, result
    FROM students
    WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()
    connection.close()

    if student:

        print("\n" + "=" * 45)
        print("              STUDENT FOUND")
        print("=" * 45)

        print("ID         :", student[0])
        print("Name       :", student[1])
        print("Python     :", student[2])
        print("SQL        :", student[3])
        print("DSA        :", student[4])
        print("Total      :", student[5])
        print("Percentage :", f"{student[6]:.2f}%")
        print("Result     :", student[7])

        print("=" * 45)

    else:
        print("\nStudent not found!")


# ------------------------------------------------------------
# 5. UPDATE STUDENT
# ------------------------------------------------------------

def update_student():

    try:
        student_id = int(input("\nEnter Student ID to update: "))
    except ValueError:
        print("Please enter a valid ID.")
        return

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if not student:
        print("\nStudent not found!")
        connection.close()
        return

    print("\nStudent:", student[0])

    try:
        python_marks = int(input("Enter new Python marks: "))
        sql_marks = int(input("Enter new SQL marks: "))
        dsa_marks = int(input("Enter new DSA marks: "))
    except ValueError:
        print("Marks must be numbers.")
        connection.close()
        return

    total = python_marks + sql_marks + dsa_marks
    percentage = total / 3

    result = "Pass" if percentage >= 40 else "Fail"

    cursor.execute("""
    UPDATE students
    SET python_marks = ?,
        sql_marks = ?,
        dsa_marks = ?,
        total = ?,
        percentage = ?,
        result = ?
    WHERE id = ?
    """, (
        python_marks,
        sql_marks,
        dsa_marks,
        total,
        percentage,
        result,
        student_id
    ))

    connection.commit()
    connection.close()

    print("\nStudent updated successfully!")


# ------------------------------------------------------------
# 6. DELETE STUDENT
# ------------------------------------------------------------

def delete_student():

    try:
        student_id = int(input("\nEnter Student ID to delete: "))
    except ValueError:
        print("Please enter a valid ID.")
        return

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT name, python_marks, sql_marks, dsa_marks
    FROM students
    WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if not student:

        print("\nStudent not found!")
        connection.close()
        return

    print("\n" + "=" * 40)
    print("          STUDENT DETAILS")
    print("=" * 40)

    print("Name   :", student[0])
    print("Python :", student[1])
    print("SQL    :", student[2])
    print("DSA    :", student[3])

    print("=" * 40)

    confirm = input("Delete this student? (yes/no): ")

    if confirm.lower() == "yes":

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        connection.commit()

        print("\nStudent deleted successfully!")

    else:

        print("\nDeletion cancelled!")

    connection.close()


# ------------------------------------------------------------
# 7. ANALYTICS + GRAPHS
# ------------------------------------------------------------

def show_analytics():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT name, python_marks, sql_marks,
           dsa_marks, total, percentage
    FROM students
    """)

    students = cursor.fetchall()
    connection.close()

    if not students:
        print("\nNo student data available.")
        return

    names = [student[0] for student in students]

    python_marks = [student[1] for student in students]
    sql_marks = [student[2] for student in students]
    dsa_marks = [student[3] for student in students]

    totals = [student[4] for student in students]
    percentages = [student[5] for student in students]

    # Averages
    python_average = sum(python_marks) / len(python_marks)
    sql_average = sum(sql_marks) / len(sql_marks)
    dsa_average = sum(dsa_marks) / len(dsa_marks)

    # Topper
    topper_index = percentages.index(max(percentages))

    # Statistics
    average_percentage = sum(percentages) / len(percentages)

    highest_percentage = max(percentages)
    lowest_percentage = min(percentages)

    print("\n" + "=" * 60)
    print("             PERFORMANCE ANALYTICS")
    print("=" * 60)

    print(f"Total Students       : {len(students)}")
    print(f"Average Percentage   : {average_percentage:.2f}%")
    print(f"Highest Percentage   : {highest_percentage:.2f}%")
    print(f"Lowest Percentage    : {lowest_percentage:.2f}%")

    print(
        f"Topper               : "
        f"{names[topper_index]} "
        f"({percentages[topper_index]:.2f}%)"
    )

    print(f"Python Average       : {python_average:.2f}")
    print(f"SQL Average          : {sql_average:.2f}")
    print(f"DSA Average          : {dsa_average:.2f}")

    print("=" * 60)

    # --------------------------------------------------------
    # GRAPH 1 - Subject Average
    # --------------------------------------------------------

    subjects = ["Python", "SQL", "DSA"]
    averages = [
        python_average,
        sql_average,
        dsa_average
    ]

    plt.figure(figsize=(8, 5))

    bars = plt.bar(subjects, averages)

    plt.title("Subject-wise Average Marks")
    plt.xlabel("Subjects")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)

    for bar, value in zip(bars, averages):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1,
            f"{value:.1f}",
            ha="center"
        )

    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # GRAPH 2 - Student Percentage
    # --------------------------------------------------------

    plt.figure(figsize=(11, 5))

    bars = plt.bar(names, percentages)

    plt.title("Student Percentage Comparison")
    plt.xlabel("Students")
    plt.ylabel("Percentage")
    plt.ylim(0, 100)

    plt.xticks(rotation=30)

    for bar, value in zip(bars, percentages):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1,
            f"{value:.1f}%",
            ha="center"
        )

    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # GRAPH 3 - Subject Performance
    # --------------------------------------------------------

    x = range(len(names))

    plt.figure(figsize=(11, 6))

    plt.plot(
        x,
        python_marks,
        marker="o",
        label="Python"
    )

    plt.plot(
        x,
        sql_marks,
        marker="o",
        label="SQL"
    )

    plt.plot(
        x,
        dsa_marks,
        marker="o",
        label="DSA"
    )

    plt.xticks(x, names, rotation=30)

    plt.title("Student Subject Performance")
    plt.xlabel("Students")
    plt.ylabel("Marks")
    plt.ylim(0, 100)

    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 8. MAIN MENU
# ------------------------------------------------------------

def main():

    create_database()
    add_demo_students()

    while True:

        print("\n")
        print("=" * 60)
        print("       STUDENT PERFORMANCE & ANALYTICS SYSTEM")
        print("=" * 60)

        print("1. Display All Students")
        print("2. Search Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. View Analytics & Graphs")
        print("6. Exit")

        print("=" * 60)

        choice = input("Enter your choice: ")

        if choice == "1":
            display_students()

        elif choice == "2":
            search_student()

        elif choice == "3":
            update_student()

        elif choice == "4":
            delete_student()

        elif choice == "5":
            show_analytics()

        elif choice == "6":
            print("\nThank you for using Student Performance System!")
            break

        else:
            print("\nInvalid choice! Please select 1-6.")


# ------------------------------------------------------------
# START PROGRAM
# ------------------------------------------------------------

if __name__ == "__main__":
    main()