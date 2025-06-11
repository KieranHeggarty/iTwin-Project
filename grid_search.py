'''

This script performs a grid search to find the best parameters for detecting cattle weight gain.
goal is to minimise the prediction error.
To create the heatmap, run this script and then copy the 

'''



import json
from datetime import datetime
import json
import numpy as np
from utils.data_io import load_json
from models import grid_search

# Time how long it takes to run the script
import time



cattle_data_file = "./Data/cattle-data.json"
data = load_json(cattle_data_file)
data = data[:10]

first_weight_date = data[0]["weights"][0]["date"]
start_date = datetime.strptime(first_weight_date, "%Y-%m-%d")

# grid search for best parameters



window_sizes = range(6, 9)         # More responsive windows
thresholds = np.linspace(0.1, 0.3, 7)  # Reasonable slope cutoffs in kg/day
min_durations = range(1, 3)        # Faster detection





start_time = time.time()
print("Starting grid search...")
best_params, best_accuracy = grid_search(data, start_date, window_sizes, thresholds, min_durations, log_file_path="./testing/grid_search_log.txt")
print("\nBest Parameters Found:")
print(f"Best Parameters: Window Size: {best_params[0]}, Threshold: {best_params[1]}, Min Duration: {best_params[2]}")
print(f"Best Average Accuracy: {best_accuracy:.2f} days")
end_time = time.time()
print(f"Grid search completed in {end_time - start_time:.2f} seconds")