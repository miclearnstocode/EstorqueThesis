import tkinter as tk
from tkinter import ttk

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

        tk.Label(self.student_frame, text="Student Screen").pack()

        # Create a frame to hold the Regular/Irregular buttons
        self.regular_frame = tk.Frame(self.student_frame)
        self.regular_frame.pack(pady=10)

        ttk.Button(self.regular_frame, text="Regular", command=lambda: self.year_screen("Regular")).pack(side=tk.LEFT)
        ttk.Button(self.regular_frame, text="Irregular", command=lambda: self.year_screen("Irregular")).pack(side=tk.LEFT)

        # Create a frame to hold the year buttons and student list
        self.year_frame = tk.Frame(self.student_frame)
        self.year_frame.pack(pady=10)

        self.student_list_frame = tk.Frame(self.student_frame)
        self.student_list_frame.pack(pady=10)

        # Add a Back button to return to the main menu
        ttk.Button(self.student_frame, text="Back", command=self.show_main_menu).pack(pady=10)

        # Update the current frame
        self.current_frame = self.student_frame

    def year_screen(self, status):
        # Clear the student list frame before showing the new year options
        self.clear_frame(self.student_list_frame)

        # Clear year buttons if already exist
        self.clear_frame(self.year_frame)

        # Create a frame to hold the year buttons
        years = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
        for year in years:
            button = ttk.Button(self.year_frame, text=year, command=lambda year=year, status=status: self.student_list_screen(year, status))
            button.pack(side=tk.LEFT)

    def student_list_screen(self, year, status):
        # Clear only the student list frame before showing the student list
        self.clear_frame(self.student_list_frame)

        tk.Label(self.student_list_frame, text=f"{year} {status} Students").pack()

        # Create a listbox to display the student list
        student_list = tk.Listbox(self.student_list_frame, width=40)
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

    def grade_screen(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        grade_frame = tk.Frame(self)
        grade_frame.pack(pady=20)

        tk.Label(grade_frame, text="Grade Screen").pack()
        ttk.Button(grade_frame, text="Back", command=self.show_main_menu).pack()

        # Update the current frame
        self.current_frame = grade_frame

    def curriculum_screen(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        curriculum_frame = tk.Frame(self)
        curriculum_frame.pack(pady=20)

        tk.Label(curriculum_frame, text="Curriculum Screen").pack()
        ttk.Button(curriculum_frame, text="Back", command=self.show_main_menu).pack()

        # Update the current frame
        self.current_frame = curriculum_frame

    def archive_screen(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        archive_frame = tk.Frame(self)
        archive_frame.pack(pady=20)

        tk.Label(archive_frame, text="Archive Screen").pack()
        ttk.Button(archive_frame, text="Back", command=self.show_main_menu).pack()

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