import tkinter as tk
from tkinter import ttk, filedialog

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Computer Science Department System")
        self.geometry("800x600")  # Set the window size

        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=20)  # Add some padding around the frame

        # Create the buttons
        buttons = [
            ("Student", self.student_screen),
            ("Grade", self.grade_screen),
            ("Curriculum", self.curriculum_screen),
            ("Archive", self.archive_screen),
        ]

        for i, (text, command) in enumerate(buttons):
            button = ttk.Button(self.button_frame, text=text, command=command)
            button.grid(row=0, column=i, padx=10, pady=10)  # Arrange buttons in a row

        # Center the window on the screen
        self.center_window()

        # Keep track of the current frame
        self.current_frame = self.button_frame

        # Variable to store the currently searched student details
        self.current_student = None

    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(pos) for pos in self.geometry().split('+')[0].split('x'))
        x = (screen_width // 2) - (size[0] // 2)
        y = (screen_height // 2) - (size[1] // 2)
        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

    def student_screen(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.student_frame = tk.Frame(self)
        self.student_frame.pack(pady=20)

        tk.Label(self.student_frame, text="Student").pack()

        # Create a frame to hold the Regular/Irregular buttons
        self.regular_frame = tk.Frame(self.student_frame)
        self.regular_frame.pack(pady=10)

        ttk.Button(self.regular_frame, text="Regular", command=lambda: self.show_search_bar("Regular")).pack(side=tk.LEFT)
        ttk.Button(self.regular_frame, text="Irregular", command=lambda: self.show_search_bar("Irregular")).pack(side=tk.LEFT)

        # Create a frame to hold the search bar, buttons, and student list
        self.search_frame = tk.Frame(self.student_frame)
        self.search_frame.pack(pady=10)

        self.student_list_frame = tk.Frame(self.student_frame)
        self.student_list_frame.pack(pady=10)

        # Add a Back button to return to the main menu
        ttk.Button(self.student_frame, text="Back", command=self.show_main_menu).pack(pady=10)

        # Update the current frame
        self.current_frame = self.student_frame

    def show_search_bar(self, status):
        # Clear the search frame before showing the search bar
        self.clear_frame(self.search_frame)
        self.clear_frame(self.student_list_frame)

        tk.Label(self.search_frame, text=f"Search {status} Students by ID:").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(self.search_frame, text="Search", command=lambda: self.search_student(self.search_var.get(), status))
        search_button.pack(side=tk.LEFT, padx=5)

        info_button = ttk.Button(self.search_frame, text="Student Information", command=self.show_student_info)
        info_button.pack(side=tk.LEFT, padx=5)

        subject_button = ttk.Button(self.search_frame, text="Subject", command=self.show_subject_info)
        subject_button.pack(side=tk.LEFT, padx=5)

        # Bind the Enter key to trigger the search function
        self.search_entry.bind("<Return>", lambda event: self.search_student(self.search_var.get(), status))

    def search_student(self, student_id, status):
        # Clear only the student list frame before showing the search results
        self.clear_frame(self.student_list_frame)

        tk.Label(self.student_list_frame, text=f"Search Results for {status} Students with ID {student_id}:").pack(anchor='w')

        # Create a frame to display the student details
        student_details_frame = tk.Frame(self.student_list_frame)
        student_details_frame.pack(anchor='w', padx=10, pady=5)

        # Sample student data (replace with actual search logic)
        students = {
            "123456": {"name": "John Doe", "year": "1st Year", "id": "123456", "info": "CS Student", "subjects": ["Math", "Physics", "Programming"]},
            "654321": {"name": "Jane Doe", "year": "2nd Year", "id": "654321", "info": "CS Student", "subjects": ["Algorithms", "Data Structures", "Database"]},
            "112233": {"name": "Bob Smith", "year": "3rd Year", "id": "112233", "info": "CS Student", "subjects": ["Networking", "Operating Systems", "AI"]},
            "332211": {"name": "Alice Johnson", "year": "4th Year", "id": "332211", "info": "CS Student", "subjects": ["Machine Learning", "Software Engineering", "Cyber Security"]},
        }

        # Check if student ID exists in the sample data
        if student_id in students:
            self.current_student = students[student_id]
            student = self.current_student
            tk.Label(student_details_frame, text=f"Name: {student['name']}").pack(anchor='w')
            tk.Label(student_details_frame, text=f"Year Level: {student['year']}").pack(anchor='w')
            tk.Label(student_details_frame, text=f"ID Number: {student['id']}").pack(anchor='w')
        else:
            tk.Label(student_details_frame, text="Student not found.").pack(anchor='w')
            self.current_student = None

    def show_student_info(self):
        if self.current_student:
            self.clear_frame(self.student_list_frame)
            student_info_frame = tk.Frame(self.student_list_frame)
            student_info_frame.pack(anchor='w', padx=10, pady=5)
            tk.Label(student_info_frame, text=f"Student Information for {self.current_student['name']}").pack(anchor='w')
            tk.Label(student_info_frame, text=f"Year Level: {self.current_student['year']}").pack(anchor='w')
            tk.Label(student_info_frame, text=f"ID Number: {self.current_student['id']}").pack(anchor='w')
            tk.Label(student_info_frame, text=f"Info: {self.current_student['info']}").pack(anchor='w')
        else:
            self.show_error("No student selected. Please search for a student first.")

    def show_subject_info(self):
        if self.current_student:
            self.clear_frame(self.student_list_frame)
            subject_info_frame = tk.Frame(self.student_list_frame)
            subject_info_frame.pack(anchor='w', padx=10, pady=5)
            tk.Label(subject_info_frame, text=f"Subject Information for {self.current_student['name']}").pack(anchor='w')
            for subject in self.current_student['subjects']:
                tk.Label(subject_info_frame, text=subject).pack(anchor='w')
        else:
            self.show_error("No student selected. Please search for a student first.")

    def show_error(self, message):
        error_window = tk.Toplevel(self)
        error_window.title("Error")
        tk.Label(error_window, text=message, padx=20, pady=20).pack()
        ttk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)

    def grade_screen(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        grade_frame = tk.Frame(self)
        grade_frame.pack(pady=20)

        tk.Label(grade_frame, text="Grade").pack()

        # Create buttons for each year level
        years = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
        for year in years:
            year_frame = tk.Frame(grade_frame)
            year_frame.pack(pady=5)
            tk.Label(year_frame, text=f"{year} Grading Sheet:").pack(side=tk.LEFT)

            # Add semester selection
            semester_var = tk.StringVar()
            semester_var.set("1st Semester")  # default value
            semester_label = tk.Label(year_frame, text="Semester:")
            semester_label.pack(side=tk.LEFT)
            semester_option = ttk.OptionMenu(year_frame, semester_var, "1st Semester", "1st Semester", "2nd Semester")
            semester_option.pack(side=tk.LEFT, padx=5)

            import_button = ttk.Button(year_frame, text="Import", command=lambda year=year, semester=semester_var: self.import_grading_sheet(year, semester.get()))
            import_button.pack(side=tk.LEFT, padx=5)

        # Add a Back button to return to the main menu
        ttk.Button(grade_frame, text="Back", command=self.show_main_menu).pack(pady=10)

        # Update the current frame
        self.current_frame = grade_frame

    def import_grading_sheet(self, year, semester):
        file_path = filedialog.askopenfilename(title=f"Import Grading Sheet for {year} {semester}", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
        if file_path:
            # Implement the logic to handle the imported grading sheet file
            print(f"Imported {year} {semester} grading sheet from {file_path}")

    def curriculum_screen(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        curriculum_frame = tk.Frame(self)
        curriculum_frame.pack(pady=20)

        tk.Label(curriculum_frame, text="Curriculum").pack()

        # Create a frame to hold the import buttons
        import_frame = tk.Frame(curriculum_frame)
        import_frame.pack(pady=10)

        ttk.Button(import_frame, text="Existing Curriculum (CSV)", command=self.import_existing_curriculum).pack(side=tk.LEFT, padx=5)
        ttk.Button(import_frame, text="New Curriculum (CSV)", command=self.import_new_curriculum).pack(side=tk.LEFT, padx=5)

        # Add a Back button to return to the main menu
        ttk.Button(curriculum_frame, text="Back", command=self.show_main_menu).pack(pady=10)

        # Update the current frame
        self.current_frame = curriculum_frame

    def import_existing_curriculum(self):
        file_path = filedialog.askopenfilename(title="Import Existing Curriculum (CSV)", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
        if file_path:
            # Implement the logic to handle the imported CSV file for existing curriculum data
            print(f"Imported existing curriculum from {file_path}")

    def import_new_curriculum(self):
        file_path = filedialog.askopenfilename(title="Import New Curriculum (CSV)", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
        if file_path:
            # Implement the logic to handle the imported CSV file for new curriculum data
            print(f"Imported new curriculum from {file_path}")

    def archive_screen(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        archive_frame = tk.Frame(self)
        archive_frame.pack(pady=20)

        tk.Label(archive_frame, text="Archive").pack()
        ttk.Button(archive_frame, text="Back", command=self.show_main_menu).pack()

        # Create a frame to hold the import buttons
        import_frame = tk.Frame(archive_frame)
        import_frame.pack(pady=10)

        ttk.Button(import_frame, text="Regular Archive", command=lambda: self.import_archive("Regular")).pack(side=tk.LEFT)
        ttk.Button(import_frame, text="Irregular Archive", command=lambda: self.import_archive("Irregular")).pack(side=tk.LEFT)

        # Update the current frame
        self.current_frame = archive_frame

    def show_main_menu(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.button_frame.pack(pady=20)  # Show the main menu buttons again
        self.current_frame = self.button_frame

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    app = Application()
    app.mainloop()