# Sentinel-2 band names (10m/20m resolution) commonly used in remote sensing applications
# and their corresponding indices in the Sentinel-2 data cube.

S2_BAND_MAPPING = {
    "B02": 1,   # Blue
    "B03": 2,   # Green
    "B04": 3,   # Red
    "B08": 4,   # NIR
    "B11": 5,   # SWIR
    "B12": 6,   # SWIR-2
    "B05": 7,   # Red Edge 1
    "B06": 8,   # Red Edge 2
    "B07": 9    # Red Edge 3
}

# Define spectral indices to compute
# These indices are commonly used in remote sensing for vegetation analysis and other applications.
VEGETATION_INDICES = ["NDVI", "SAVI", "GCI", "NDWI", "EVI"]

# Reference paths for input and output data
TRUTH_LABELS_CSV = "data/truth_labels.csv"
