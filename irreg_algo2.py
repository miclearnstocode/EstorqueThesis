import pandas as pd

# Load data from the Excel file
old_curriculum_path = '/mnt/data/OldcurriCopy.xlsx'
old_df = pd.read_excel(old_curriculum_path)

# Load data from the CSV file for existing curriculum
existing_curriculum_path = '/mnt/data/existing_curriculum.csv'  # Update this path as needed
existing_df = pd.read_csv(existing_curriculum_path)

# Add a column to indicate the curriculum type
existing_df['Curriculum_Type'] = 'Existing'
old_df['Curriculum_Type'] = 'Old'

# Ensure the columns match between both dataframes
old_df = old_df[existing_df.columns]

# Combine both dataframes
df = pd.concat([existing_df, old_df], ignore_index=True)

# Load student grades data
student_grades_path = '/mnt/data/file-shQ3T0c1fdTo4akqJP4ZHKvj'  # Update this path as needed
grades_df = pd.read_excel(student_grades_path)

# Reshape grades_df to a long format for easier processing
grades_df_long = grades_df.melt(id_vars=['Student_Id'], var_name='Course_Code', value_name='Grade')

# Function to check if a student meets the prerequisites
def check_prerequisites(row, student_id, grades_df_long):
    prerequisites = row['Prerequisite'].split(',')
    for prereq in prerequisites:
        prereq = prereq.strip()
        if prereq and not ((grades_df_long['Student_Id'] == student_id) & 
                           (grades_df_long['Course_Code'] == prereq) & 
                           (grades_df_long['Grade'] <= 2.0)).any():
            return False
    return True

# Function to filter eligible subjects for a student
def get_eligible_subjects(student_id, df, grades_df_long, max_units=18, max_new_subjects=2):
    df['Eligible'] = df.apply(lambda row: check_prerequisites(row, student_id, grades_df_long), axis=1)
    eligible_df = df[df['Eligible']]

    possible_subjects = []
    for (semester, year), group in eligible_df.groupby(['Semester', 'Year']):
        total_units = 0
        subjects = []
        new_subject_count = 0
        for _, row in group.iterrows():
            if total_units + row['Units'] <= max_units and new_subject_count < max_new_subjects:
                subjects.append(row['Course_Code'])
                total_units += row['Units']
                new_subject_count += 1
        possible_subjects.append({'Semester': semester, 'Year': year, 'Subjects': subjects, 'Total_Units': total_units})

    possible_subjects_df = pd.DataFrame(possible_subjects)
    return possible_subjects_df

# Example student_id for testing
student_id = '2021-322138'

# Get eligible subjects for the student
eligible_subjects_df = get_eligible_subjects(student_id, df, grades_df_long)

# Display eligible subjects
print(eligible_subjects_df)