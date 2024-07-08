import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def process_data(df):
    """Process the dataset, fill missing values, encode categorical features, and apply RandomForestClassifier."""
    
    # Check if required columns exist
    required_columns = ['Units', 'Lab', 'Year Level', 'Lec', 'Prerequisite']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"The required column '{col}' does not exist in the DataFrame.")

    # Fill missing values and ensure proper data types
    df.fillna({'Units': 0, 'Lab': 'N/A', 'Year Level': 'N/A', 'Lec': 'N/A', 'Prerequisite': 'N/A'}, inplace=True)

    # Ensure 'Year Level' is treated as string/object initially
    df['Year Level'] = df['Year Level'].astype(str)

    # Mapping 'Year Level' to numerical values
    year_level_mapping = {
        "1.1": 1, "1.2": 2,
        "2.1": 3, "2.2": 4,
        "3.1": 5, "3.2": 6,
        "4.1": 7, "4.2": 8
    }

    # Reverse mapping for interpretation
    reverse_year_level_mapping = {v: k for k, v in year_level_mapping.items()}

    # Convert 'Year Level' to numerical labels
    df['Year Level'] = df['Year Level'].map(year_level_mapping)

    # Check for NaNs in 'Year Level' after mapping
    if df['Year Level'].isnull().any():
        raise ValueError("Target variable 'Year Level' contains NaN values after processing.")

    # One-hot encoding for categorical columns 'Lec' and 'Lab'
    df_onehot = pd.get_dummies(df, columns=['Lec', 'Lab'])

    # Define feature columns and target column
    feature_cols = [col for col in df_onehot.columns if col != 'Year Level']
    target_col = 'Year Level'

    # Split data into features and target variable
    X = df_onehot[feature_cols]
    y = df_onehot[target_col]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model using RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # Make predictions on the testing set
    y_pred = rf.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    # Predict the year level for all subjects
    df_onehot['predicted_year_level'] = rf.predict(X)
    df['predicted_year_level'] = df_onehot['predicted_year_level']

    # Reverse mapping for 'predicted_year_level' for interpretation
    df['predicted_year_level'] = df['predicted_year_level'].map(reverse_year_level_mapping)

    # Ensure that the predicted year levels match the actual year levels
    df['year_level_match'] = df['Year Level'] == df['predicted_year_level']

    # Function to display subjects by predicted year and semester
    def display_subjects_by_year_and_semester(df, year, semester):
        year_semester = f"{year}.{semester}"
        subjects = df[(df['predicted_year_level'] == year_semester) & (df['year_level_match'])]
        return subjects

    # Separate subjects by predicted year and semester, and save to CSV
    for year in range(1, 5):
        for semester in [1, 2]:
            subjects = display_subjects_by_year_and_semester(df, year, semester)
            if not subjects.empty:
                filename = f"Year_{year}_Semester_{semester}.csv"
                subjects.to_csv(filename, index=False)

    # Identify mismatches between actual and predicted year levels
    mismatches = df[~df['year_level_match']]
    mismatches.to_csv("mismatches.csv", index=False)

    return accuracy, report, df, mismatches

def save_data(df, filename):
    """Save the DataFrame to a CSV file."""
    df.to_csv(filename, index=False)

# Sample usage
if __name__ == "__main__":
    # Load your dataset
    df = pd.read_csv("c:/Users/VASQUEZ FAMILY/Documents/Thesis1/curri.csv")

    # Process the data
    accuracy, report, processed_df, mismatches = process_data(df)
    print("Accuracy:", accuracy)
    print("Classification Report:\n", report)
    print("Processed Data:\n", processed_df)
    print("Mismatches:\n", mismatches)

    # Save the processed data to a file
    save_data(processed_df, "processed_data.csv")
