# This contains functions to load and preprocess data for the ML pipeline.
# It includes functions to load Sentinel-2 tiles and truth labels from CSV files.
# It also includes a function to build a dataset from the loaded data.

import rasterio
import os

def load_multiband_tile(tile_folder):
    band_files = {
        'B01': 'B01.tiff',
        'B02': 'B02.tiff',
        'B03': 'B03.tiff',
        'B04': 'B04.tiff',
        'B05': 'B05.tiff',
        'B06': 'B06.tiff',
        'B07': 'B07.tiff',
        'B08': 'B08.tiff',
        'B8A': 'B8A.tiff',
        'B09': 'B09.tiff',
        'B11': 'B11.tiff',
        'B12': 'B12.tiff'
    }

    image = {}
    for band, filename in band_files.items():
        path = os.path.join(tile_folder, filename)
        with rasterio.open(path) as src:
            image[band] = src.read(1)

    return image


def extract_patch(tile, lat, lon, size=16):
    half = size // 2

    # Use red band as reference for geotransform
    ref_path = "data/sentinel2_tiles/B04.tiff"
    with rasterio.open(ref_path) as src:
        transform = src.transform
        col, row = ~transform * (lon, lat)

    col, row = int(col), int(row)

    x_min, x_max = col - half, col + half
    y_min, y_max = row - half, row + half

    patch = {
        band: img[y_min:y_max, x_min:x_max]
        for band, img in tile.items()
    }

    if all(p.shape == (size, size) for p in patch.values()):
        return patch
    else:
        return None


