import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
import re
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 1. Load Porto boundary
aoi = gpd.read_file("data/processed/porto_boundary.geojson")

# 2. Open Band 10 and reproject AOI to match raster
with rasterio.open(
        "data/raw/LC08_L1TP_204031_20240704_20240712_02_T1_B10.TIF") as src:
    aoi = aoi.to_crs(src.crs)
    clipped, transform = mask(src, aoi.geometry, crop=True)
    band10 = clipped[0].astype(float)

# 3. Read metadata file
with open(
        "data/raw/LC08_L1TP_204031_20240704_20240712_02_T1_MTL.txt") as f:
    mtl = f.read()

def get_mtl_value(keyword):
    match = re.search(rf"{keyword}\s=\s([-0-9\.E]+)", mtl)
    return float(match.group(1)) if match else None

# 4. Extract constants
ML = get_mtl_value("RADIANCE_MULT_BAND_10")
AL = get_mtl_value("RADIANCE_ADD_BAND_10")
K1 = get_mtl_value("K1_CONSTANT_BAND_10")
K2 = get_mtl_value("K2_CONSTANT_BAND_10")

# 5. Convert to radiance and temperature
radiance = ML * band10 + AL
radiance[radiance <= 0] = np.nan
bt_kelvin = K2 / (np.log((K1 / radiance) + 1))
bt_celsius = bt_kelvin - 273.15
bt_celsius = np.clip(bt_celsius, 10, 50)

import matplotlib.colors as mcolors

# Step 1: Create mask with NaNs for outside AOI
clustered = np.full(bt_celsius.shape, np.nan)
clustered[(bt_celsius >= 25) & (bt_celsius < 30)] = 1  # Warm
clustered[(bt_celsius >= 30) & (bt_celsius < 35)] = 2  # Very Warm
clustered[(bt_celsius >= 35) & (bt_celsius <= 38)] = 3  # Hot
clustered[bt_celsius > 38] = 4                         # Critical

# Plotting: only zones 1 to 4
cmap = mcolors.ListedColormap(['blue', 'yellow', 'orange', 'red'])  # matches zones 1-4
bounds = [0.5, 1.5, 2.5, 3.5, 4.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# Plot
plt.figure(figsize=(10, 8))
im = plt.imshow(clustered, cmap=cmap, norm=norm)
plt.contour(clustered, levels=[1, 2, 3, 4], colors='black', linewidths=0.5)
plt.title("Porto Urban Heat Zones")
plt.axis('off')

# Colorbar
cbar = plt.colorbar(im, ticks=[1, 2, 3, 4])
cbar.ax.set_yticklabels([
    'Warm (25–30 °C)',
    'Very Warm (30–35 °C)',
    'Hot (35–38 °C)',
    '🔥 Critical (>38 °C)'
])
cbar.set_label("Temperature Zone")

plt.show()

# --- Export critical heat islands as GeoTIFF ---#

from rasterio.transform import from_origin
from rasterio.crs import CRS

# Generate binary mask: 1 = critical zone, 0 = elsewhere
critical_mask = (clustered == 4).astype(np.uint8)

export_path = "../porto_uhi/data/processed/porto_critical_uhi.tif"

with rasterio.open(
    export_path,
    'w',
    driver='GTiff',
    height=critical_mask.shape[0],
    width=critical_mask.shape[1],
    count=1,
    dtype='uint8',
    crs=src.crs,
    transform=transform,
) as dst:
    dst.write(critical_mask, 1)

print(f"✅ Critical UHI mask saved to {export_path}")
