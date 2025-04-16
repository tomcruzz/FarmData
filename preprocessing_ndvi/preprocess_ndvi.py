import rasterio
import numpy as np
import matplotlib.pyplot as plt

def calculate_ndvi(red_band_path, nir_band_path):
    with rasterio.open(red_band_path) as red:
        red_data = red.read(1).astype('float32')

    with rasterio.open(nir_band_path) as nir:
        nir_data = nir.read(1).astype('float32')

    # Avoid division by zero
    ndvi = (nir_data - red_data) / (nir_data + red_data + 1e-5)
    ndvi = np.clip(ndvi, -1, 1)
    
    return ndvi

# Example usage
if __name__ == "__main__":
     # .tif files downloaded from https://apps.sentinel-hub.com/eo-browser/
    red = "data/B04_red.tif"
    nir = "data/B08_nir.tif"
    
    ndvi = calculate_ndvi(red, nir)
    
    plt.imshow(ndvi, cmap='RdYlGn')
    plt.colorbar()
    plt.title("NDVI Map")
    plt.show()
