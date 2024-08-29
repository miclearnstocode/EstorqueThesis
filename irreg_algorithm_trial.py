import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering

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
    df_old['Course No.'] = df_old['Course No.'].astype(str)
    df_new['Course No.'] = df_new['Course No.'].astype(str)
    df_old['Prerequisite'] = df_old['Prerequisite'].astype(str)
    df_new['Prerequisite'] = df_new['Prerequisite'].astype(str)

    # Check for uniqueness in 'Course No.' column only
    if not df_old['Course No.'].is_unique:
        raise ValueError("Old curriculum 'Course No.' contains duplicate values.")
    if not df_new['Course No.'].is_unique:
        raise ValueError("New curriculum 'Course No.' contains duplicate values.")

    # Replace 'N/A' values with NaN and convert numerical columns
    for df in [df_old, df_new]:
        df['Units'] = df['Units'].replace('N/A', np.nan)
        df['Lab'] = df['Lab'].replace('N/A', np.nan)
        df['Lec'] = df['Lec'].replace('N/A', np.nan)
        df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
        df['Lab'] = pd.to_numeric(df['Lab'], errors='coerce')
        df['Lec'] = pd.to_numeric(df['Lec'], errors='coerce')
        df['Year Level'] = df['Year Level'].astype(str)
        df['Year Level Code'] = df['Year Level'].apply(map_year_semester)

    # Filter the old curriculum to show only subjects that have grades
    subjects_with_grades_old = df_old[df_old['Grades'].notna()]

    # Match the filtered old curriculum subjects with the new curriculum
    matched_subjects = pd.merge(subjects_with_grades_old[['Course No.', 'Descriptive Title', 'Grades']],
                                df_new, on='Course No.', how='left')

    # Drop rows where the 'Course No.' from the old curriculum is not found in the new curriculum
    matched_subjects = matched_subjects.dropna(subset=['Descriptive Title_y'])

    # Now proceed with the clustering on the new curriculum
    year_semester_mapping = {
        "Y1S1": 1, "Y1S2": 2,
        "Y2S1": 3, "Y2S2": 4,
        "Y3S1": 5, "Y3S2": 6,
        "Y4S1": 7, "Y4S2": 8
    }
    df_new['Year Level Num'] = df_new['Year Level Code'].map(year_semester_mapping)
    df_new = df_new.dropna(subset=['Year Level Num'])

    clustered_data = pd.DataFrame()
    year_levels = df_new['Year Level Num'].unique()
    for year_level in year_levels:
        year_level_df = df_new[df_new['Year Level Num'] == year_level]

        # Extract features for clustering
        features = year_level_df[['Units', 'Lab', 'Lec']].values

        # Standardize the features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # Apply hierarchical clustering
        clustering = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
        cluster_labels = clustering.fit_predict(scaled_features)

        # Add cluster labels to the DataFrame
        year_level_df['Cluster'] = cluster_labels

        # Append to the final clustered data
        clustered_data = pd.concat([clustered_data, year_level_df])

    return matched_subjects, clustered_data

# Example usage
old_file_path = '/path/to/old_curriculum.csv'
new_file_path = '/path/to/new_curriculum.csv'
matched_subjects, clustered_data = process_data(old_file_path, new_file_path)

# Output the results
print("Matched Subjects with Grades:")
print(matched_subjects)
print("\nClustered Data for New Curriculum:")
print(clustered_data)