# This contains functions to compute various vegetation indices from two bands of satellite imagery.
# The indices include NDVI, SAVI, NDWI, GCI, and EVI.

import numpy as np

def compute_index(band1, band2, index_type, L=0.5):
    band1 = band1.astype(float)
    band2 = band2.astype(float)

    if index_type == "NDVI":
        return (band2 - band1) / (band2 + band1 + 1e-6)
    elif index_type == "SAVI":
        return ((band2 - band1) / (band2 + band1 + L)) * (1 + L)
    elif index_type == "NDWI":
        return (band1 - band2) / (band1 + band2 + 1e-6)
    elif index_type == "GCI":
        return (band2 / (band1 + 1e-6)) - 1
    elif index_type == "EVI":
        return 2.5 * (band2 - band1) / (band2 + 6 * band1 - 7.5 * 0.1 + 1)
    else:
        raise ValueError(f"Unknown index type: {index_type}")
