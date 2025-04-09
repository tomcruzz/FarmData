# This file is part of the ml_pipeline.

import pandas as pd
import numpy as np
from ml_pipeline.constants import *
from ml_pipeline.label_encoder import load_ground_truth, encode_species
from ml_pipeline.data_loader import load_multiband_tile, extract_patch
from ml_pipeline.feature_extractor import compute_index
import os
from tqdm import tqdm

def build_dataset(tile_path, csv_path, patch_size=16):
    df = load_ground_truth(csv_path)
    df, label_map = encode_species(df)
    tile = load_multiband_tile(tile_path)

    features = []
    targets_species = []
    targets_biomass = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        lat, lon = row["lat"], row["lon"]
        patch = extract_patch(tile, lat, lon, patch_size)
        if patch is None:
            continue

        red   = patch["B04"]
        nir   = patch["B08"]
        swir  = patch["B11"]
        green = patch["B03"]

        # Optional: New Bands
        b01 = patch["B01"]
        b05 = patch["B05"]
        b06 = patch["B06"]
        b07 = patch["B07"]
        b8a = patch["B8A"]
        b09 = patch["B09"]
        b12 = patch["B12"]


        ndvi = compute_index(red, nir, "NDVI").mean()
        savi = compute_index(red, nir, "SAVI").mean()
        gci  = compute_index(green, nir, "GCI").mean()
        ndwi = compute_index(nir, swir, "NDWI").mean()

        features.append([
            ndvi, savi, gci, ndwi,
            b01.mean(), b05.mean(), b06.mean(), b07.mean(),
            b8a.mean(), b09.mean(), b12.mean()
        ])

        targets_species.append(row["species_label"])
        targets_biomass.append(row["biomass"])

    return pd.DataFrame(features, columns=[
        "NDVI", "SAVI", "GCI", "NDWI",
        "B01", "B05", "B06", "B07",
        "B8A", "B09", "B12"
    ]), np.array(targets_species), np.array(targets_biomass)

