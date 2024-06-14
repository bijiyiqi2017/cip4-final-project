import tkinter as tk
import mss

'''
CiP 4 Final Project by William D. Miller Jr.

    A weekly classroom leaderboard app~ This program is to take imput from the user when 
asked for the class week start date, class week end date, student's test grade (in floats),
names of students that need to improve (in spelling, grammar, and English speaking) the 
test grades will be sorted the highest grade ranked number 1. Any student with the grade 90
or above will automatically be put into an English Rockstar list. The information will be 
displayed via tkinter window graphics medal rankings from 1st place to 10th place. You can
take a screenshot via the mss library when you click on the screenshot button. A popup window 
will ask for a file name, then it saves the screenshot. 
'''

def take_screenshot():
    # Create a new window for entering the filename
    filename_window = tk.Toplevel(root)
    filename_window.title("Enter Filename")
    
    tk.Label(filename_window, text="Enter filename for screenshot:").pack(pady=10)
    filename_entry = tk.Entry(filename_window)
    filename_entry.pack(pady=5)
    
    def save_filename():
        filename = filename_entry.get()
        if filename:
            with mss.mss() as sct:
                sct.shot(output=filename + '.png')
            print(f"Screenshot taken and saved as '{filename}.png'")
        filename_window.destroy()

    tk.Button(filename_window, text="Save", command=save_filename).pack(pady=10)

def draw_medal(canvas, x, y, color, place, name, grade):
    # Draw the outer circle
    canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=color, outline=color)
    # Draw the inner circle with white color
    canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white", outline="white")
    # Draw the place number aligned with the center of the medal
    canvas.create_text(x, y, text=str(place), font=('Arial', 20), fill='black')
    # Draw the name and grade beside the medal
    canvas.create_text(x + 60, y, text=f"{name} {grade}", font=('Arial', 15), fill='black', anchor='w')

def main():
    # Initialize the student names without grades
    students_grades = {
        "Alice": 0.0,
        "Bob": 0.0,
        "Charlie": 0.0,
        "David": 0.0,
        "Eva": 0.0,
        "Frank": 0.0,
        "Grace": 0.0,
        "Hannah": 0.0,
        "Ivy": 0.0,
        "Jack": 0.0
    }

    # Prompt the user to enter grades for each student
    for student in students_grades.keys():
        grade = float(input(f"Enter the grade for {student}: "))
        students_grades[student] = grade

    # Prompt the user for the week's start and end dates
    start_date = input("Enter the week's start date (e.g., YYYY-MM-DD): ")
    end_date = input("Enter the week's end date (e.g., YYYY-MM-DD): ")

    # Prompt the user for names for the different improvement lists
    improve_spelling = input("Enter names of students who need to improve spelling, separated by commas: ").split(',')
    improve_grammar = input("Enter names of students who need to improve English grammar, separated by commas: ").split(',')
    improve_speaking = input("Enter names of students who need to improve English speaking, separated by commas: ").split(',')

    # Convert the grades to a sorted list of tuples for ranking
    sorted_students = sorted(students_grades.items(), key=lambda item: item[1], reverse=True)

    # Initialize the main window
    global root
    root = tk.Tk()
    root.title("Classroom Leaderboard")

    # Create a frame to hold the canvas and scrollbar
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas
    canvas = tk.Canvas(frame, width=600, height=800)  # Increased height
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a scrollbar
    scrollbar = tk.Scrollbar(frame, command=canvas.yview, width=30)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Draw the leaderboard title
    canvas.create_text(300, 20, text='Classroom Leaderboard', font=('Arial', 20), fill='blue')
    # Draw the week's start and end dates below the title on one line with a smaller font size
    canvas.create_text(300, 60, text=f"Week: {start_date} - {end_date}", font=('Arial', 12), fill='black')

    # Colors for the medals using RGB codes for bronze
    colors = ['gold', 'silver', '#CD7F32', 'blue', 'green', 'orange', 'purple', 'pink', 'cyan', 'magenta']

    # Draw medals and names with grades for 1st to 10th place
    for i, ((name, grade), color) in enumerate(zip(sorted_students[:10], colors)):
        draw_medal(canvas, 200, 140 + i * 60, color, i + 1, name, grade)

    # Draw the English Rockstar list
    canvas.create_text(300, 140 + 10 * 60, text='English Rockstars:', font=('Arial', 16), fill='green', anchor='w')
    y_position = 140 + 10 * 60 + 40
    for student, grade in sorted_students:
        if grade >= 90:
            canvas.create_text(300, y_position, text=f"{student}: {grade}", font=('Arial', 12), fill='black', anchor='w')
            y_position += 20

    # Add extra space after English Rockstars list
    y_position += 40

    # Draw the 'Needs to improve spelling' list
    canvas.create_text(300, y_position, text='Needs to improve spelling:', font=('Arial', 16), fill='red', anchor='w')
    y_position += 20
    for student in improve_spelling:
        canvas.create_text(300, y_position, text=student.strip(), font=('Arial', 12), fill='black', anchor='w')
        y_position += 20

    # Add extra space after the spelling list
    y_position += 40

    # Draw the 'Needs to improve English grammar' list
    canvas.create_text(300, y_position, text='Needs to improve English grammar:', font=('Arial', 16), fill='red', anchor='w')
    y_position += 20
    for student in improve_grammar:
        canvas.create_text(300, y_position, text=student.strip(), font=('Arial', 12), fill='black', anchor='w')
        y_position += 20

    # Add extra space after the grammar list
    y_position += 40

    # Draw the 'Needs to improve English speaking' list
    canvas.create_text(300, y_position, text='Needs to improve English speaking:', font=('Arial', 16), fill='red', anchor='w')
    y_position += 20
    for student in improve_speaking:
        canvas.create_text(300, y_position, text=student.strip(), font=('Arial', 12), fill='black', anchor='w')
        y_position += 20

    # Add extra space at the bottom
    y_position += 40
    canvas.configure(scrollregion=(0, 0, 600, y_position + 40))

    # Create top screenshot button
    screenshot_button_top = tk.Button(frame, text="Take Screenshot", command=take_screenshot)
    screenshot_button_top.pack(side=tk.TOP, anchor='e')

    root.mainloop()
if __name__ == "__main__":
    main()
