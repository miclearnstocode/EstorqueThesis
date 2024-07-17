import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering

def process_data(file_path):
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

    df = pd.read_csv(file_path)

    # Ensure 'Course No.' and 'Prerequisite' remain as strings
    df['Course No.'] = df['Course No.'].astype(str)
    df['Prerequisite'] = df['Prerequisite'].astype(str)

    # Check for uniqueness in 'Course No.' column only
    if not df['Course No.'].is_unique:
        raise ValueError("Column 'Course No.' contains duplicate values.")

    # Replace 'N/A' values with NaN
    df['Units'] = df['Units'].replace('N/A', np.nan)
    df['Lab'] = df['Lab'].replace('N/A', np.nan)
    df['Lec'] = df['Lec'].replace('N/A', np.nan)

    # Convert numerical columns to numeric, coercing errors to NaN
    df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
    df['Lab'] = pd.to_numeric(df['Lab'], errors='coerce')
    df['Lec'] = pd.to_numeric(df['Lec'], errors='coerce')

    # Remove rows with NaN values in numerical columns
    df = df.dropna(subset=['Units', 'Lab', 'Lec'])

    # Convert 'Year Level' to string to handle possible float NaNs
    df['Year Level'] = df['Year Level'].astype(str)

    # Map 'Year Level' to a unified format combining year and semester (e.g., "Y1S1", "Y2S2")
    df['Year Level Code'] = df['Year Level'].apply(map_year_semester)

    # Convert 'Year Level Code' to numerical labels for clustering
    year_semester_mapping = {
        "Y1S1": 1, "Y1S2": 2,
        "Y2S1": 3, "Y2S2": 4,
        "Y3S1": 5, "Y3S2": 6,
        "Y4S1": 7, "Y4S2": 8
    }
    df['Year Level Num'] = df['Year Level Code'].map(year_semester_mapping)

    # Handle missing mappings
    df = df.dropna(subset=['Year Level Num'])

    # Split data by year levels
    clustered_data = pd.DataFrame()
    year_levels = df['Year Level'].unique()
    for year_level in year_levels:
        year_level_df = df[df['Year Level'] == year_level]

        # Extract features for clustering, excluding 'Course No.' and 'Prerequisite'
        features = year_level_df[['Units', 'Lab', 'Lec']].values

        # Standardize the features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # Apply hierarchical clustering to split into clusters
        clustering = AgglomerativeClustering(n_clusters=1, metric='euclidean', linkage='ward')
        cluster_labels = clustering.fit_predict(scaled_features)

        # Add cluster labels to the DataFrame
        year_level_df['Cluster'] = cluster_labels

        # Append to the final clustered data
        clustered_data = pd.concat([clustered_data, year_level_df])

    return clustered_data

def filter_regular_subjects(df):
    # Define criteria for regular subjects (no grades)
    regular_criteria = df['Grade'].isna()
    return df[regular_criteria]

def appraise_irregular_students(df, regular_subjects_df):
    # Identify irregular subjects
    irregular_subjects = df[~df['Course No.'].isin(regular_subjects_df['Course No.'])]
    return irregular_subjects

def filter_student_conditions(df):
    # Note: Add more conditions here to filter the student CSV file based on specific criteria.
    # Example conditions:
    # df = df[df['Status'] == 'Transferee']
    # df = df[df['Status'] == 'Continuing']
    # df = df[df['Status'] == 'Shifter']
    # Combine multiple conditions if needed:
    # df = df[(df['Status'] == 'Transferee') | (df['Status'] == 'Shifter')]
    
    # Replace this example with actual conditions
    return df

# Example usage
file_path = 'your_dataset.csv'
df = process_data(file_path)
irregular_student_file_path = 'irregular_student.csv'

# Load the irregular student data
irregular_df = pd.read_csv(irregular_student_file_path)

# Apply additional student conditions
filtered_irregular_df = filter_student_conditions(irregular_df)

# Filter regular subjects
regular_subjects_df = filter_regular_subjects(filtered_irregular_df)

# Appraise irregular students
irregular_subjects_df = appraise_irregular_students(filtered_irregular_df, regular_subjects_df)

# Output the results
print("Regular Subjects:\n", regular_subjects_df)
print("Irregular Subjects:\n", irregular_subjects_df)
