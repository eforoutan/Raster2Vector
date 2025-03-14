import geopandas as gpd
import numpy as np
import rasterio
import rasterio.features
from rasterio.errors import RasterioIOError

def raster_to_vector(input_raster, rounding_precision=0):
    """
    Converts raster data to vector polygons, with an option to round raster values to specified precision.
    
    Parameters:
    - input_raster (str): Path to the input raster file.
    - rounding_precision (int): The number of decimal places to round values to before vectorizing.
    
    Returns:
    - gdf (GeoDataFrame): A GeoDataFrame containing polygons based on the raster values.
    """
    try:
        with rasterio.open(input_raster) as src:
            band = src.read(1)
            nodata = src.nodata

            # Set NoData values to NaN for consistent handling
            if nodata is not None:
                band = np.where(band == nodata, np.nan, band)

            # Round the values based on rounding_precision for non-NaN values
            rounded_band = np.round(band, decimals=rounding_precision)
            
            # Get unique values after rounding (excluding NaN)
            unique_values = np.unique(rounded_band[~np.isnan(rounded_band)])
            polygons = []

            for value in unique_values:
                # Create a mask for each unique value
                mask = rounded_band == value
                shapes = list(rasterio.features.shapes(rounded_band, mask=mask, transform=src.transform))

                for shape, val in shapes:
                    if val == value:
                        polygons.append({
                            'geometry': shape,
                            'properties': {'value': value}  # Keep as float for decimals
                        })

            # Convert the list of polygons to a GeoDataFrame
            gdf = gpd.GeoDataFrame.from_features(polygons)
            return gdf

    except RasterioIOError as e:
        print(f"Failed to read raster file: {e}")
        return None

def save_outputs(gdf, geojson_output, csv_output):
    """
    Save the vectorized data to both GeoJSON and CSV files.
    
    Parameters:
    - gdf (GeoDataFrame): The GeoDataFrame to save.
    - geojson_output (str): Path for saving the GeoJSON file.
    - csv_output (str): Path for saving the CSV file.
    """
    try:
        # Save to GeoJSON
        gdf.to_file(geojson_output, driver="GeoJSON")
        print(f"Results saved as GeoJSON to {geojson_output}")

        # Save to CSV (without geometry)
        gdf.drop(columns='geometry').to_csv(csv_output, index=False)
        print(f"Results saved as CSV to {csv_output}")

    except Exception as e:
        print(f"Failed to save output files: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script.py <input_raster> <rounding_precision>")
        sys.exit(1)

    input_raster = sys.argv[1]
    rounding_precision = int(sys.argv[2])

    # Convert raster to vector
    gdf = raster_to_vector(input_raster, rounding_precision)

    if gdf is not None:
        geojson_output = "vectorized_output.geojson"
        csv_output = "vectorized_output.csv"
        
        # Save results to GeoJSON and CSV
        save_outputs(gdf, geojson_output, csv_output)
    else:
        print("Raster to vector conversion failed.")
