import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main Menu")
        self.geometry("300x200")

        # Create the frames
        self.frames = {}
        for F in (MainMenu, StudentScreen, GradeScreen, CurriculumScreen, ArchiveScreen):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create the buttons
        student_button = tk.Button(self, text="Student", command=lambda: controller.show_frame("StudentScreen"))
        grade_button = tk.Button(self, text="Grade", command=lambda: controller.show_frame("GradeScreen"))
        curriculum_button = tk.Button(self, text="Curriculum", command=lambda: controller.show_frame("CurriculumScreen"))
        archive_button = tk.Button(self, text="Archive", command=lambda: controller.show_frame("ArchiveScreen"))

        # Create a frame to center the buttons
        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, fill=tk.BOTH)

        # Place the buttons in the frame
        student_button.pack(pady=5)
        grade_button.pack(pady=5)
        curriculum_button.pack(pady=5)
        archive_button.pack(pady=5)

        # Center the buttons
        button_frame.pack_propagate(False)

        for button in [student_button, grade_button, curriculum_button, archive_button]:
            button_frame.columnconfigure(0, weight=1)
            button.pack(side="top", fill="x", pady=5, padx=10)

class StudentScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Student Screen")
        label.pack(pady=10)

        # Create a frame to center the button
        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, fill=tk.BOTH)

        back_button = tk.Button(button_frame, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=5)

        # Center the button
        button_frame.pack_propagate(False)
        button_frame.columnconfigure(0, weight=1)
        back_button.pack(side="top", fill="x", pady=5, padx=10)

class GradeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Grade Screen")
        label.pack(pady=10)

        # Create a frame to center the button
        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, fill=tk.BOTH)

        back_button = tk.Button(button_frame, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=5)

        # Center the button
        button_frame.pack_propagate(False)
        button_frame.columnconfigure(0, weight=1)
        back_button.pack(side="top", fill="x", pady=5, padx=10)

class CurriculumScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Curriculum Screen")
        label.pack(pady=10)

        # Create a frame to center the button
        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, fill=tk.BOTH)

        back_button = tk.Button(button_frame, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=5)

        # Center the button
        button_frame.pack_propagate(False)
        button_frame.columnconfigure(0, weight=1)
        back_button.pack(side="top", fill="x", pady=5, padx=10)

class ArchiveScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Archive Screen")
        label.pack(pady=10)

        # Create a frame to center the button
        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, fill=tk.BOTH)

        back_button = tk.Button(button_frame, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=5)

        # Center the button
        button_frame.pack_propagate(False)
        button_frame.columnconfigure(0, weight=1)
        back_button.pack(side="top", fill="x", pady=5, padx=10)

def main():
    app = Application()
    for frame in app.frames.values():
        frame.grid(row=0, column=0, sticky="nsew")
    app.mainloop()

if __name__ == "__main__":
    main()
