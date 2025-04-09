# This will provide functions to load ground truth data from a CSV file and encode species labels.
# It uses pandas for data manipulation and assumes the CSV has 'species' and 'biomass' columns.

import pandas as pd

def load_ground_truth(csv_path):
    df = pd.read_csv(csv_path)
    if 'species' not in df or 'biomass' not in df:
        raise ValueError("CSV must contain 'species' and 'biomass' columns.")
    return df

def encode_species(df):
    species_mapping = {label: idx for idx, label in enumerate(df['species'].unique())}
    df['species_label'] = df['species'].map(species_mapping)
    return df, species_mapping
