import os
from astropy.io import fits
import pandas as pd
import numpy as np

# Define the folder containing the .fit files
fits_folder = "./sun_meas_25/meas_1/"  # Replace with the path to your folder
output_folder = "./sun_meas_25/meas_1/"  # Replace with the path to save .csv files

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate through all .fit files in the folder
for filename in os.listdir(fits_folder):
    if filename.endswith(".fit"):  # Check if the file is a .fit file
        fits_path = os.path.join(fits_folder, filename)
        csv_path = os.path.join(output_folder, filename.replace(".fit", ".csv"))

        # Open and process the .fit file
        try:
            with fits.open(fits_path) as hdul:
                print(f"Processing {filename}")
                
                # Extract intensity data from HDU 0
                intensity_data = hdul[0].data  # Shape: (200, 806)
                print(intensity_data.shape)
                
                # Extract frequency and time from HDU 1
                frequencies = hdul[1].data['FREQUENCY'].flatten()  # Shape: (200,)
                times = hdul[1].data['TIME'].flatten()  # Shape: (806,)
                print(frequencies.shape)
                print(times.shape)
                
                # Validate dimensions
                if intensity_data.shape != (len(frequencies), len(times)):
                    raise ValueError("Intensity data shape does not match frequency and time arrays.")
                
                # Reshape into a DataFrame with columns: Time, Frequency, Intensity
                rows = []
                for i, freq in enumerate(frequencies):
                    for j, time in enumerate(times):
                        rows.append([time, freq, intensity_data[i, j]])
                
                # Create a DataFrame
                df = pd.DataFrame(rows, columns=["Time", "Frequency", "Intensity"])
                
                # Save to CSV
                df.to_csv(csv_path, index=False)
                print(f"Saved {csv_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")
