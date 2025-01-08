import os
from astropy.io import fits
import pandas as pd
import numpy as np

# Define the folder containing the .fits files
fits_folder = "./sun_meas_25/meas_1/"  # Replace with the path to your folder
output_folder = "./sun_meas_25/meas_1/"  # Replace with the path to save .csv files

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate through all .fits files in the folder
for filename in os.listdir(fits_folder):
    if filename.endswith(".fit"):  # Check if the file is a .fits file
        fits_path = os.path.join(fits_folder, filename)
        csv_path = os.path.join(output_folder, filename.replace(".fit", ".csv"))

        # Open and process the .fits file
        try:
            with fits.open(fits_path) as hdul:
                print(f"Processing {filename}")
                # Assuming the data is in HDU 1 (adjust if needed)
                data = hdul[1].data

                print(type(data))
                print(data.shape)
                print(data.dtype)

                
                # Check if it's a structured array
                if isinstance(data, (fits.fitsrec.FITS_rec, np.recarray)):
                    # Convert to a Pandas DataFrame directly
                    df = pd.DataFrame(data.tolist(), columns=data.names)
                else:
                    # For raw NumPy arrays, reshape or flatten if necessary
                    data = data.flatten()
                    df = pd.DataFrame(data)

                # Save to .csv
                df.to_csv(csv_path, index=False)
                print(f"Saved {csv_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
