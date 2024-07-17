import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Management System")
        self.geometry("400x200")  # Set the window size

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
            button = tk.Button(self.button_frame, text=text, command=command)
            button.grid(row=0, column=i, padx=10, pady=10)  # Arrange buttons in a row

        # Center the window on the screen
        self.center_window()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.winfo_reqwidth()) // 2
        y = (screen_height - self.winfo_reqheight()) // 2
        self.geometry(f"+{x}+{y}")

    def student_screen(self):
        self.button_frame.pack_forget()  # Hide the main menu buttons
        self.student_frame = tk.Frame(self)
        self.student_frame.pack(pady=20)

        tk.Label(self.student_frame, text="Student Screen").pack()

        # Create a frame to hold the Regular/Irregular buttons
        regular_frame = tk.Frame(self.student_frame)
        regular_frame.pack(pady=10)

        tk.Button(regular_frame, text="Regular", command=lambda: self.year_screen("Regular")).pack(side=tk.LEFT)
        tk.Button(regular_frame, text="Irregular", command=lambda: self.year_screen("Irregular")).pack(side=tk.LEFT)

    def year_screen(self, status):
        # Create a frame to hold the year buttons
        year_frame = tk.Frame(self.student_frame)
        year_frame.pack(pady=10)

        years = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
        for year in years:
            button = tk.Button(year_frame, text=year, command=lambda year=year, status=status: self.student_list_screen(year, status))
            button.pack(side=tk.LEFT)

    def student_list_screen(self, year, status):
        # Create a frame to hold the student list
        student_frame = tk.Frame(self.student_frame)
        student_frame.pack(pady=10)

        tk.Label(student_frame, text=f"{year} {status} Students").pack()

        # Create a listbox to display the student list
        student_list = tk.Listbox(student_frame, width=40)
        student_list.pack()

        # Add some sample student data
        students = [
            "John Doe (Section A)",
            "Jane Doe (Section B)",
            "Bob Smith (Section C)",
            "Alice Johnson (Section D)",
        ]
        for student in students:
            student_list.insert(tk.END, student)

        # Add a Back button
        tk.Button(student_frame, text="Back", command=self.show_main_menu).pack()

    def grade_screen(self):
        self.button_frame.pack_forget()  # Hide the main menu buttons
        grade_frame = tk.Frame(self)
        grade_frame.pack(pady=20)

        tk.Label(grade_frame, text="Grade Screen").pack()
        tk.Button(grade_frame, text="Back", command=self.show_main_menu).pack()

    def curriculum_screen(self):
        self.button_frame.pack_forget()  # Hide the main menu buttons
        curriculum_frame = tk.Frame(self)
        curriculum_frame.pack(pady=20)

        tk.Label(curriculum_frame, text="Curriculum Screen").pack()
        tk.Button(curriculum_frame, text="Back", command=self.show_main_menu).pack()

    def archive_screen(self):
        self.button_frame.pack_forget()  # Hide the main menu buttons
        archive_frame = tk.Frame(self)
        archive_frame.pack(pady=20)

        tk.Label(archive_frame, text="Archive Screen").pack()
        tk.Button(archive_frame, text="Back", command=self.show_main_menu).pack()

    def show_main_menu(self):
        for widget in self.winfo_children():
            if widget!= self.button_frame:
                widget.destroy()
        self.button_frame.pack(pady=20)  # Show the main menu buttons again

if __name__ == "__main__":
    app = Application()
    app.mainloop()