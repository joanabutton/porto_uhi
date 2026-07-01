# Urban Heat Island Mapping — Porto, Portugal

This project identifies and visualizes Urban Heat Islands (UHIs) in Porto using thermal satellite data from Landsat 8. The project was guided by AI-assisted learning and developed through open-source geospatial tools.

## Overview

- Focus Area: Porto municipality, Portugal
- Satellite Date: July 4, 2024
- Data Source: Landsat 8 (USGS EarthExplorer)
- Tools: Python, QGIS, rasterio, geopandas

## What This Project Does

- Converts Landsat Band 10 radiance to Land Surface Temperature (LST)
- Clips data to the Porto administrative boundary
- Classifies temperature into 4 heat categories:
  - Warm (25–30 °C)
  - Very Warm (30–35 °C)
  - Hot (35–38 °C)
  - Critical (>38 °C)
- Exports a GeoTIFF highlighting critical zones
- Visualizes results with QGIS and matplotlib

## 📂 Project Structure

porto-uhi-project/
├── data/ # Raw and processed spatial data
├── outputs/ # Final figures and maps
├── report/ # PDF report
├── main.py # Full workflow (LST → classification → export)
├── prepare_boundary.py
├── get_porto_land_temperature_map.py
└── README.md

Note: Only Band 10 and the metadata file are included. Full Landsat scene is publicly available via EarthExplorer.

## Sample Output

> Land surface temperature map for Porto:   
>  [`outputs/porto_urban_heat_zones.png`](outputs/porto_urban_heat_zones.png)


## Final Report

> The full project report is available here:  
>  [`porto_heat_map.pdf`](porto_heat_map.pdf)

## Next Steps

- Add land use overlays (NDVI, impervious surfaces)
- Compare summer vs winter temperature data
- Build AI-generated mitigation strategy tool
- 




## License

This project is licensed under the MIT License.

## Author

**Joana Button**


[LinkedIn](https://www.linkedin.com/in/joana-cardoso-button-33310844/) 

## Acknowledgments

- Satellite data from USGS EarthExplorer
- Developed with guidance from ChatGPT-4o (OpenAI)
- Visualized using QGIS

Note: 
Full Landsat scene is publicly available via EarthExplorer.
---


