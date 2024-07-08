import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering

def map_year_semester(year_semester):
    try:
        year_semester = str(year_semester)
        if '.' in year_semester:
            year, semester = year_semester.split('.')
            return f"Y{year}S{semester}"
        else:
            print(f"Skipping invalid Year Level value: {year_semester}")
            return np.nan
    except ValueError:
        print(f"Skipping invalid Year Level value: {year_semester}")
        return np.nan

def process_data(df):
    """Process the dataset, fill missing values, encode categorical features,
    and apply hierarchical clustering based on year levels and additional features."""

    # Check if required columns exist
    required_columns = ['Course No.', 'Descriptive Title', 'Year Level', 'Units', 'Lab', 'Lec', 'Prerequisite']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"The required column '{col}' does not exist in the DataFrame. Available columns: {df.columns.tolist()}")

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

    # Print unique 'Year Level' values to debug
    print("Unique 'Year Level' values before mapping:")
    print(df['Year Level'].unique())

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

    # Print unique 'Year Level Code' values to debug
    print("Unique 'Year Level Code' values after mapping:")
    print(df['Year Level Code'].unique())

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

        # Apply hierarchical clustering to split into two clusters (semesters)
        clustering = AgglomerativeClustering(n_clusters=1, metric='euclidean', linkage='ward')
        cluster_labels = clustering.fit_predict(scaled_features)

        # Add cluster labels to the DataFrame
        year_level_df['Cluster'] = cluster_labels

        # Append to the final clustered data
        clustered_data = pd.concat([clustered_data, year_level_df])

    # Create a mapping of clusters to year level titles for display
    year_level_titles = {
        0: "First Semester",
        1: "Second Semester"
    }

    return clustered_data, year_level_titles

# Sample usage for testing
if __name__ == "__main__":
    # Load your dataset
    df = pd.read_csv("c:/Users/VASQUEZ FAMILY/Documents/Thesis1/curri.csv")

    try:
        # Process the data
        processed_data, year_level_titles = process_data(df)

        # Example: Display processed data
        print("Processed Data:")
        print(processed_data)

        # Example: Display clustering results based on year level titles
        for year_level in processed_data['Year Level'].unique():
            for cluster_id in processed_data['Cluster'].unique():
                print(f"Year Level {year_level} - Cluster {cluster_id}: {year_level_titles.get(cluster_id, 'Unknown Cluster')}")
                cluster_df = processed_data[(processed_data['Year Level'] == year_level) & (processed_data['Cluster'] == cluster_id)]
                print(cluster_df[['Course No.', 'Descriptive Title', 'Year Level', 'Units', 'Lab', 'Lec', 'Prerequisite']])
                print("\n")

    except FileNotFoundError:
        print("Error: The specified file was not found.")
    
    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
