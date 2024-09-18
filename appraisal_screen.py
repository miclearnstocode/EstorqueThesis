import importlib
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from tkinter import filedialog
from database import DatabaseHandler
from fuzzywuzzy import fuzz, process

class AppraisalScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#00BFFF")  # Set background color
        self.data_appraised = False

        # Add widgets for appraisal screen
        self.label = tk.Label(self, text="Appraisal", font=("Times New Roman", 18,))
        self.label.pack(pady=20)

        # Create a Notebook to hold the Treeview (for matched subjects)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a frame for displaying matched subjects within the Notebook
        self.frame1 = tk.Frame(self.notebook, bg="#00BFFF")
        self.notebook.add(self.frame1, text="Matched Subjects")

        # Define the Treeview for displaying matched subjects
        self.tree1 = ttk.Treeview(self.frame1, show="headings", height=15)
        self.tree1.pack(fill=tk.BOTH, expand=True)
        # Create a frame to hold the buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)
        # Appraise button
        self.appraise_button = ttk.Button(button_frame, text="Appraise", command=self.start_appraisal)
        self.appraise_button.pack(side=tk.LEFT, pady=5)

        # Back button
        back_button = ttk.Button(button_frame, text="Back", command=self.master.show_main_menu)
        back_button.pack(side=tk.LEFT, pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        return file_path


    from fuzzywuzzy import fuzz, process


    def process_data(self, old_file_path, new_file_path):
        # Read old and new curriculum data
        df_old = pd.read_csv(old_file_path)
        df_new = pd.read_csv(new_file_path)

        # Clean Descriptive_Title columns
        df_old['Descriptive_Title'] = df_old['Descriptive_Title'].astype(str).str.strip()
        df_new['Descriptive_Title'] = df_new['Descriptive_Title'].astype(str).str.strip()

        # Clean column names
        df_old.columns = [col.strip() for col in df_old.columns]
        df_new.columns = [col.strip() for col in df_new.columns]

        # Check if 'Descriptive_Title' exists in both dataframes
        if 'Descriptive_Title' not in df_old.columns or 'Descriptive_Title' not in df_new.columns:
            messagebox.showerror("Error", "'Descriptive_Title' column is missing in one of the files.")
            return

        # Filter old curriculum to keep only rows where 'Grades' are not NaN
        filtered_old = df_old[df_old['Grades'].notna()]

        # Initialize a dictionary to store matched Descriptive_Titles and their corresponding grades
        matched_grades = {}

        # Perform fuzzy matching for each Descriptive_Title in the old curriculum
        for index, row in filtered_old.iterrows():
            old_title = row['Descriptive_Title']
            # Using token_sort_ratio to allow for matching even if word order changes
            match_result = process.extractOne(old_title, df_new['Descriptive_Title'], scorer=fuzz.token_sort_ratio)

            if match_result:
                new_title, score,_ = match_result
                # Adjust the threshold score based on your matching requirements
                if score >= 80:  # Adjust the threshold score as needed
                    matched_grades[new_title] = row['Grades']

        # Update grades in the new curriculum DataFrame based on matched titles
        df_new['Grades'] = df_new['Descriptive_Title'].map(matched_grades)

        # Drop rows without valid 'Descriptive_Title' if necessary
        matched_subjects = df_new.dropna(subset=['Descriptive_Title'])

        # Sort the data by year (assuming you have a 'Year_Level' or equivalent column)
        if 'Year_Level' in matched_subjects.columns:
            matched_subjects = matched_subjects.sort_values(by=['Year_Level', 'Descriptive_Title'])

        return matched_subjects


    def display_data(self, matched_subjects):
        # Clear existing data in the Treeview
        for child in self.tree1.get_children():
            self.tree1.delete(child)

        # Define which columns to display
        columns_to_display = ['Course_No', 'Descriptive_Title', 'Year_Level','Units', 'Lec', 'Lab', 'Grades']
        self.tree1["columns"] = columns_to_display

        # Configure treeview headings and column width
        for col in columns_to_display:
            self.tree1.heading(col, text=col)
            self.tree1.column(col, width=100)

         # Insert matched subjects into the treeview
        for _, row in matched_subjects.iterrows():
            self.tree1.insert("", "end", values=[row.get(col, "") for col in columns_to_display])


    def start_appraisal(self):
        old_file_path = self.select_file()
        new_file_path = self.select_file()

        matched_subjects = self.process_data(old_file_path, new_file_path)
    
        if matched_subjects is not None:
            self.display_data(matched_subjects)

        self.data_appraised = True  # Mark as appraised
