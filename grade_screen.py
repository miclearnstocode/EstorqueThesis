import threading
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from database import DatabaseHandler
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_EMAIL = 'michaelestorque123@gmail.com'
SMTP_PASSWORD = 'ycxyqorukveyxiqs'

class GradeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#008080")
        self.master = master

        self.data_frame = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Grade", bg="#008080").pack(pady=10)

        # Create a frame to hold the year and semester selectors
        selection_frame = tk.Frame(self, bg="#008080")
        selection_frame.pack(pady=10)

        # Dropdown for selecting the year level
        year_var = tk.StringVar()
        year_var.set("1st Year")  # default value
        year_label = tk.Label(selection_frame, text="Year Level:", bg="#008080")
        year_label.pack(side=tk.LEFT, padx=5)
        year_option = ttk.OptionMenu(selection_frame, year_var, "1st Year", "1st Year", "2nd Year", "3rd Year", "4th Year")
        year_option.pack(side=tk.LEFT, padx=5)

        # Dropdown for selecting the semester
        semester_var = tk.StringVar()
        semester_var.set("1st Semester")  # default value
        semester_label = tk.Label(selection_frame, text="Semester:", bg="#008080")
        semester_label.pack(side=tk.LEFT, padx=5)
        semester_option = ttk.OptionMenu(selection_frame, semester_var, "1st Semester", "1st Semester", "2nd Semester")
        semester_option.pack(side=tk.LEFT, padx=5)

        # Button to import the grading sheet
        import_button = ttk.Button(selection_frame, text="Import", command=lambda: self.open_file_dialog(year_var.get(), semester_var.get()))
        import_button.pack(side=tk.LEFT, padx=5)

        # Save button (initially disabled)
        self.save_button = ttk.Button(selection_frame, text="Save Grade", state=tk.DISABLED, command=self.on_save_button_click)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Add a label for displaying status messages
        self.status_label = tk.Label(self, text="", bg="#008080", fg="white")
        self.status_label.pack(pady=5)

        # Add a progress bar
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="indeterminate")
        self.progress_bar.pack(pady=5)
        self.progress_bar.pack_forget()  # Hide it initially

        # Back button
        ttk.Button(self, text="Back", command=self.master.show_main_menu).pack(pady=10)
        # Create a DatabaseHandler instance
        self.db_handler = DatabaseHandler()

    def open_file_dialog(self, year, semester):
        # Open a file dialog to select a CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.import_grading_sheet(file_path, year, semester)

    def import_grading_sheet(self, file_path, year, semester):
        try:
            grading_data = pd.read_csv(file_path)

            if not grading_data.empty:
                messagebox.showinfo("Success", f"Processed grading sheet data for {year} {semester}")
                self.grading_data = grading_data
                self.year = year
                self.semester = semester
                self.display_grading_data(grading_data)
                self.save_button.config(state=tk.NORMAL)

                # Check for missing grades and process students
                threading.Thread(target=self.process_students, args=(grading_data,), daemon=True).start()
            else:
                messagebox.showerror("Error", f"No data found in {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {e}")

    def process_students(self, grading_data):
        # Show loading state
        self.status_label.config(text="Checking for missing grades...")
        self.progress_bar.pack()
        self.progress_bar.start()

        # Get student information from the database
        student_info = self.db_handler.get_student_info()

        total_students = len(grading_data)
        processed_students = 0

        # Loop through each student (row) in the grading data
        for index, row in grading_data.iterrows():
            student_id = row['ID_NO']
            student_name = row['STUDENT_NAME']

            # Get the courses where the grade is empty (NaN or blank)
            missing_courses = [col for col in grading_data.columns[2:] if pd.isna(row[col]) or row[col] == '']

            if missing_courses:
                # Fetch the student's email from the student info table
                student_data = student_info[student_info['ID_NO'] == student_id]
                if not student_data.empty:
                    student_email = student_data['EMAIL_ADDRESS'].values[0]

                    if student_email:
                        # Send an email if the student's email is found
                        success = self.send_email(student_email, student_name, student_id, missing_courses)
                        if success:
                            # Notify user that the email has been sent
                            messagebox("Email Sent", f"Email sent to {student_name} (ID: {student_id}) for missing courses: {', '.join(missing_courses)}.")
                            self.update_status(f"Email sent to {student_name}")
                        else:
                            # Notify user if email sending failed
                            messagebox.showerror("Email Failed", f"Failed to send email to {student_name} (ID: {student_id}).")
                            self.update_status(f"Failed to send email to {student_name}")
                    else:
                        self.update_status(f"No email found for {student_name}")
                else:
                    self.update_status(f"No information found for student ID: {student_id}")

            processed_students += 1
            self.update_status(f"Processed {processed_students}/{total_students} students")

        # Hide loading state after processing
        self.update_status("All notifications processed", final=True)
        self.progress_bar.stop()
        self.progress_bar.pack_forget()


    def send_email(self, student_email, student_name, student_id, missing_courses):
        subject = f"Notification: Missing Grades for {student_name} (ID: {student_id})"
        body = f"Dear {student_name},\n\nYou are missing grades for the following courses:\n\n"

        for course in missing_courses:
            body += f"- {course}\n"

        body += "\nPlease contact your instructor to complete the requirements.\n\nRegards,\nComputer Science Department"

        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL
        msg['To'] = student_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.set_debuglevel(1)  # Enable SMTP debug output
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            text = msg.as_string()
            server.sendmail(SMTP_EMAIL, student_email, text)
            server.quit()

            # Notify the user that the email has been successfully sent
            messagebox.showinfo("Email Sent", f"Email has been successfully sent to {student_name} (ID: {student_id}).")
            return True
        except Exception as e:
            messagebox.showerror(f"Failed to send email to {student_email}. Error: {e}")
            return False


    def update_status(self, message, final=False):
        self.status_label.config(text=message)
        if final:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
        self.master.update_idletasks()


    def on_save_button_click(self):
        try:
            self.db_handler.save_grading_data(self.grading_data, self.year, self.semester)
            messagebox.showinfo("Success", "Grades have been successfully saved to the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save grades: {e}")

    def display_grading_data(self, grading_data):
        # Clear the previous frame content if already present
        if self.data_frame:
            self.data_frame.destroy()

        # Create a new frame to hold the grading data table
        self.data_frame = tk.Frame(self, bg="#008080")
        self.data_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Create a Treeview with dynamic columns based on the CSV data
        tree = ttk.Treeview(self.data_frame, columns=list(grading_data.columns), show='headings')
        tree.pack(expand=True, fill='both')

        # Add table headers
        for col in grading_data.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=100)  # Adjust the width for better display

        # Add rows to the table
        for _, row in grading_data.iterrows():
            tree.insert("", "end", values=list(row))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.data_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Optionally, you can save the grading_data dataframe to a class variable for future joining operations
        self.grading_data = grading_data
