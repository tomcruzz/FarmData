# This script is used to test the ml_pipeline module and the build_dataset function.
# It loads a tile and a CSV file, processes the data, and prints the resulting DataFrame.
# This file is part of the ml_pipeline.

from utils.prepare_training_data import build_dataset
from ml_pipeline.constants import TRUTH_LABELS_CSV

X, y_species, y_biomass = build_dataset(
    tile_path="data/sentinel2_tiles",
    csv_path=TRUTH_LABELS_CSV
)

print(X.head())
