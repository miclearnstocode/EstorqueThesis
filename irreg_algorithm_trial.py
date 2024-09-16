import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from tkinter import filedialog, ttk
from tkinter import *

def process_data(old_file_path, new_file_path):
    def map_year_semester(year_semester):
        try:
            year_semester = str(year_semester)
            if '.' in year_semester:
                year, semester = year_semester.split('.')
                return f"Y{year}S{semester}"
            else:
                return np.nan
        except ValueError:
            return np.nan

    # Load the datasets for old and new curricula
    df_old = pd.read_csv(old_file_path)
    df_new = pd.read_csv(new_file_path)

    # Ensure 'Course No.' and 'Prerequisite' remain as strings
    df_old['Course_No'] = df_old['Course_No'].astype(str).str.strip()
    df_new['Course_No'] = df_new['Course_No'].astype(str).str.strip()
    df_old['Prerequisite'] = df_old['Prerequisite'].astype(str).str.strip()
    df_new['Prerequisite'] = df_new['Prerequisite'].astype(str).str.strip()

    # Check for uniqueness in 'Course No.' column only
    if not df_old['Course_No'].is_unique:
        raise ValueError("Old curriculum 'Course No.' contains duplicate values.")
    if not df_new['Course_No'].is_unique:
        raise ValueError("New curriculum 'Course No.' contains duplicate values.")

    # Replace 'N/A' values with NaN and convert numerical columns
    for df in [df_old, df_new]:
        df['Units'] = df['Units'].replace('N/A', np.nan)
        df['Lab'] = df['Lab'].replace('N/A', np.nan)
        df['Lec'] = df['Lec'].replace('N/A', np.nan)
        df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
        df['Lab'] = pd.to_numeric(df['Lab'], errors='coerce')
        df['Lec'] = pd.to_numeric(df['Lec'], errors='coerce')
        df['Year_Level'] = df['Year_Level'].astype(str)
        df['Year Level Code'] = df['Year_Level'].apply(map_year_semester)

    # Filter the old curriculum to show only subjects that have grades
    filtered_old = df_old[df_old['Grades'].notna()]

    # Match the filtered old curriculum subjects with the new curriculum
    matched_subjects = pd.merge(filtered_old[['Course_No', 'Descriptive_Title', 'Grades']],
                                 df_new, on='Course_No', how='left')

    # Ensure 'Grades' and 'Descriptive_Title' columns exist in both dataframes
    if 'Grades' not in matched_subjects.columns:
        matched_subjects['Grades'] = np.nan
    if 'Descriptive_Title' not in matched_subjects.columns:
        matched_subjects['Descriptive_Title'] = np.nan

    # Drop rows where the 'Course No.' from the old curriculum is not found in the new curriculum
    matched_subjects = matched_subjects.dropna(subset=['Course_No'])

    # Get the list of matched Course Nos. from the new curriculum
    matched_course_nos = matched_subjects['Course_No'].unique()

    # Filter the new curriculum based on matched subjects
    df_new_filtered = df_new[df_new['Course_No'].isin(matched_course_nos)]

    year_semester_mapping = {
        "Y1S1": 1, "Y1S2": 2,
        "Y2S1": 3, "Y2S2": 4,
        "Y3S1": 5, "Y3S2": 6,
        "Y4S1": 7, "Y4S2": 8
    }
    df_new_filtered['Year Level Num'] = df_new_filtered['Year Level Code'].map(year_semester_mapping)
    df_new_filtered = df_new_filtered.dropna(subset=['Year Level Num'])

    clustered_data = pd.DataFrame()
    year_levels = df_new_filtered['Year Level Num'].unique()

    for year_level in year_levels:
        year_level_df = df_new_filtered[df_new_filtered['Year Level Num'] == year_level]

        # Extract features for clustering
        features = year_level_df[['Units', 'Lab', 'Lec']].values

        # Check if there are enough samples to cluster
        if len(features) < 2:  # Need at least 2 samples for clustering
            continue

        # Standardize the features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # Apply hierarchical clustering
        clustering = AgglomerativeClustering(n_clusters=2, linkage='ward')  # Adjust n_clusters as needed
        cluster_labels = clustering.fit_predict(scaled_features)

        # Add cluster labels to the DataFrame
        year_level_df['Cluster'] = cluster_labels

        # Append to the final clustered data
        clustered_data = pd.concat([clustered_data, year_level_df], ignore_index=True)

    # Merge the clustered data with matched subjects to include 'Grades' and 'Descriptive_Title'
    clustered_data = pd.merge(clustered_data, matched_subjects[['Course_No', 'Grades', 'Descriptive_Title']], on='Course_No', how='left')

    # Calculate total Units, Lab, and Lec for each cluster in each semester
    total_summary = clustered_data.groupby(['Year Level Code', 'Cluster']).agg(
        Total_Units=('Units', 'sum'),
        Total_Lab=('Lab', 'sum'),
        Total_Lec=('Lec', 'sum')
    ).reset_index()

    # Sort the clustered data by semester and year level
    clustered_data['Semester'] = clustered_data['Year Level Code'].apply(lambda x: x.split('S')[1] if isinstance(x, str) else np.nan)
    clustered_data = clustered_data.sort_values(by=['Year Level Num', 'Semester'])

    # Prepare the final output with clusters and subjects
    final_output = []

    for year_level_code in clustered_data['Year Level Code'].unique():
        year_level_data = clustered_data[clustered_data['Year Level Code'] == year_level_code]
        for cluster in year_level_data['Cluster'].unique():
            cluster_data = year_level_data[year_level_data['Cluster'] == cluster]
            total_row = total_summary[(total_summary['Year Level Code'] == year_level_code) & (total_summary['Cluster'] == cluster)].copy()
            total_row['Course_No'] = 'Total'
            total_row['Descriptive_Title'] = ''
            total_row['Grades'] = ''
            final_output.append(cluster_data)
            final_output.append(total_row)

    final_output_df = pd.concat(final_output, ignore_index=True)

    # Remove the 'Total_Units', 'Total_Lab', 'Total_Lec', and 'Cluster' columns
    final_output_df = final_output_df.drop(columns=['Total_Units', 'Total_Lab', 'Total_Lec', 'Cluster'])

    return matched_subjects, final_output_df

def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

# Function to create the Tkinter window and display the data
def create_window(matched_subjects, final_output):
    root = Tk()
    root.title("Curriculum Data")

    # Creating two frames, one for Matched Subjects and one for Final Output
    frame1 = Frame(root)
    frame1.pack(side=LEFT, padx=10, pady=10)

    frame2 = Frame(root)
    frame2.pack(side=RIGHT, padx=10, pady=10)

    # Creating and displaying Matched Subjects in Treeview
    Label(frame1, text="Matched Subjects with Grades").pack()

    tree1 = ttk.Treeview(frame1, columns=matched_subjects.columns, show="headings", height=15)
    for col in matched_subjects.columns:
        tree1.heading(col, text=col)
        tree1.column(col, width=100)
    for _, row in matched_subjects.iterrows():
        tree1.insert("", "end", values=list(row))
    tree1.pack()

    # Creating and displaying Final Output in Treeview
    Label(frame2, text="Clustered Data with Totals").pack()

    tree2 = ttk.Treeview(frame2, columns=final_output.columns, show="headings", height=15)
    for col in final_output.columns:
        tree2.heading(col, text=col)
        tree2.column(col, width=100)
    for _, row in final_output.iterrows():
        tree2.insert("", "end", values=list(row))
    tree2.pack()

    # Main loop
    root.mainloop()

def main():
    old_file_path = select_file()
    new_file_path = select_file()
    matched_subjects, final_output = process_data(old_file_path, new_file_path)

    # Creating the window to display the data
    create_window(matched_subjects, final_output)

if __name__ == "__main__":
    main()
