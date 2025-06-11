'''

This script is used to test the plateau detection by inspection.
Can choose a cow and see what the model predicts as the plateau date and compare it to the real plateau date.

'''

import json
from datetime import timedelta
from datetime import datetime
import json
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.plateau_detection import detect_plateau
from models.rolling_regression import rolling_regression



number = 4 # change this number to test different cows


cattle_data_file = "./Data/cattle-data.json"
def load_cattle_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


data = load_cattle_data(cattle_data_file)
cow = data[number]
first_weight_date = cow["weights"][0]["date"]
start_date = datetime.strptime(first_weight_date, "%Y-%m-%d")


slope_data = rolling_regression(cow, window_size=11) # change this parameter according to grid search results
plateau_date = detect_plateau(slope_data, threshold=0.5429, min_duration=3) # Gets prediction of plateau date, change these parameters according to grid search results
print(f"Plateau date: {plateau_date}")
real_days_to_plateau = cow.get('plateau_day', None)
# real_platea_date is an integer representing how many days after the start date the plateau was detected
# convert the platea
real_plateau_date = (start_date + timedelta(days=real_days_to_plateau)).strftime("%Y-%m-%d")

print(f"Real plateau date: {real_plateau_date}")