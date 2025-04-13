import rasterio
import geopandas as gpd
from shapely.geometry import box

# Open raster
with rasterio.open("C:/CWL/spatial/Raster2Vector/raster/gpw_v4_cnty_sw_ok_5km_NN.tif") as src:
    data = src.read(1)
    transform = src.transform
    crs = src.crs
    nodata = src.nodata

rows, cols = data.shape

features = []

for row in range(rows):
    for col in range(cols):
        value = data[row, col]
        if value == nodata:
            continue

        # Get bounds of the pixel
        x_left, y_top = rasterio.transform.xy(transform, row, col, offset='ul')
        x_right, y_bottom = rasterio.transform.xy(transform, row, col, offset='lr')

        geom = box(x_left, y_bottom, x_right, y_top)
        features.append({"geometry": geom, "Pop": value})

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(features, geometry="geometry")
gdf.set_crs(crs, inplace=True)

# Export to GeoJSON
gdf.to_file("raster_per_pixel.geojson", driver="GeoJSON")
