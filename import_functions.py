#pip install mysql-connector-python
#a trial importation
import csv
import mysql.connector
from tkinter import filedialog

def import_grading_sheet(title):
    """Import a grading sheet, process the data, and write to the MySQL database."""
    file_path = filedialog.askopenfilename(title=title, filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
    if file_path:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            grading_data = [row for row in reader]
        
        print(f"Preparing for an important thesis with data from {file_path}")
        
        print("Preparing table for database entry...")
        grading_table = prepare_table_for_database(grading_data)
        
        print("Writing data to the database...")
        write_to_database('grading', grading_table)
        
        print(f"Imported grading sheet from {file_path}")
        return grading_table
    else:
        print("No file selected.")
        return None

def import_student_data(title):
    """Import student data, process the data, and write to the MySQL database."""
    file_path = filedialog.askopenfilename(title=title, filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
    if file_path:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            student_data = [row for row in reader]
        
        print(f"Preparing for an important thesis with data from {file_path}")
        
        print("Preparing table for database entry...")
        student_table = prepare_table_for_database(student_data)
        
        print("Writing data to the database...")
        write_to_database('students', student_table)
        
        print(f"Imported student data from {file_path}")
        return student_table
    else:
        print("No file selected.")
        return None

def prepare_table_for_database(data):
    """Prepare data for database entry."""
    # This function would transform the raw data into a format suitable for database entry
    table = []
    for row in data:
        table.append({
            'Column1': row[0],
            'Column2': row[1],
            # Add transformations as needed
        })
    return table

def write_to_database(table_name, data):
    """Write data to the MySQL database."""
    conn = mysql.connector.connect(
        host='your_host',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    cursor = conn.cursor()
    
    # Creating table if it doesn't exist
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                        Column1 VARCHAR(255),
                        Column2 VARCHAR(255)
                        -- Add other columns as needed
                      )''')
    
    # Inserting data into the table
    for row in data:
        cursor.execute(f'''INSERT INTO {table_name} (Column1, Column2)
                           VALUES (%s, %s)''', (row['Column1'], row['Column2']))
    
    conn.commit()
    conn.close()

def retrieve_data(table_name):
    """Retrieve data from the MySQL database."""
    conn = mysql.connector.connect(
        host='your_host',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    
    conn.close()
    return data
