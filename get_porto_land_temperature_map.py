import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import re

#Get the porto land temperature map

# 1. Load your Porto AOI
aoi = gpd.read_file("data/processed/porto_boundary.geojson")

# 2. Open Band 10 and reproject AOI
with rasterio.open(
        "data/raw/LC08_L1TP_204031_20240704_20240712_02_T1_B10.TIF") as src:  # update filename!
    aoi = aoi.to_crs(src.crs)  # CRS must match
    clipped, transform = mask(src, aoi.geometry, crop=True)
    band10 = clipped[0].astype(float)

# 3. Extract constants from MTL
with open("data/raw/LC08_L1TP_204031_20240704_20240712_02_T1_MTL.txt") as f:  # update filename!
    mtl = f.read()

def get_mtl_value(keyword):
    match = re.search(rf"{keyword}\s=\s([-0-9\.E]+)", mtl)
    return float(match.group(1)) if match else None

ML = get_mtl_value("RADIANCE_MULT_BAND_10")
AL = get_mtl_value("RADIANCE_ADD_BAND_10")
K1 = get_mtl_value("K1_CONSTANT_BAND_10")
K2 = get_mtl_value("K2_CONSTANT_BAND_10")

# 4. Radiance → Brightness Temperature
radiance = ML * band10 + AL
radiance[radiance <= 0] = np.nan  # filter bad values
bt_kelvin = K2 / (np.log((K1 / radiance) + 1))
bt_celsius = bt_kelvin - 273.15
bt_celsius = np.clip(bt_celsius, 10, 50)

# 5. Plot
plt.figure(figsize=(10, 8))
plt.imshow(bt_celsius, cmap="inferno")
plt.colorbar(label="Temperature (°C)")
plt.title("Land Surface Temperature – Porto")
plt.axis('off')
plt.show()




