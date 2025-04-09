# This script trains two models: a regression model for biomass prediction and a classification model 
# for species classification.
# It uses PyTorch for model training and evaluation, and scikit-learn for data splitting 
# and metrics calculation.
# It also imports utility functions for data preparation and 
# model definitions from other modules in the ml_pipeline package.

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.preprocessing import StandardScaler

import numpy as np
import pandas as pd

from utils.prepare_training_data import build_dataset
from ml_pipeline.constants import TRUTH_LABELS_CSV
from ml_pipeline.model_biomass import BiomassRegressionNN
from ml_pipeline.model_species import SpeciesClassifierNN


def train_biomass_model(X, y_biomass):
    X_train, X_val, y_train, y_val = train_test_split(X, y_biomass, test_size=0.2, random_state=42)

    model = BiomassRegressionNN(input_dim=X.shape[1])
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)

    for epoch in range(200):
        optimizer.zero_grad()
        output = model(X_train_tensor)
        loss = criterion(output, y_train_tensor)
        loss.backward()
        optimizer.step()
    print(f"Biomass Training MSE: {loss.item():.4f}")

    X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
    pred = model(X_val_tensor).detach().numpy().flatten()
    mse = mean_squared_error(y_val, pred)
    rmse = np.sqrt(mse)
    print("Biomass RMSE:", rmse)


def train_species_model(X, y_species):
    X_train, X_val, y_train, y_val = train_test_split(X, y_species, test_size=0.2, random_state=42)

    num_classes = len(set(y_species))
    model = SpeciesClassifierNN(input_dim=X.shape[1], num_classes=num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long)

    for epoch in range(200):
        optimizer.zero_grad()
        output = model(X_train_tensor)
        loss = criterion(output, y_train_tensor)
        loss.backward()
        optimizer.step()
    print(f"Species Training Loss: {loss.item():.4f}")

    X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
    pred = model(X_val_tensor).argmax(dim=1).numpy()
    print("Species Accuracy:", accuracy_score(y_val, pred))


def main():
    
    X_df, y_species, y_biomass = build_dataset(
        tile_path="data/sentinel2_tiles",
        csv_path=TRUTH_LABELS_CSV
    )

    
    scaler = StandardScaler()
    X_scaled_np = scaler.fit_transform(X_df)

    print("\n Training Models...")
    train_biomass_model(X_scaled_np, y_biomass)
    train_species_model(X_scaled_np, y_species)


if __name__ == "__main__":
    main()
