import geopandas as gpd

# 1. Load the shapefile
municipalities = gpd.read_file("data/raw/concelhos-shapefile/concelhos.shp")

# 2. Print the first few rows to see the columns
print(municipalities.head())
print(municipalities.columns)

# 3. Filter for Porto
porto = municipalities[municipalities["NAME_2"] == "Porto"]

# 4. Save to GeoJSON for later use
porto.to_file("data/processed/porto_boundary.geojson", driver="GeoJSON")