'''

This script runs the accuracy function and stores the results.
It then plots the distribution of the prediction accuracy results.

'''




import json
from datetime import datetime
import json
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.prediction_accuracy import prediction_accuracy




cattle_data_file = "./Data/cattle-data.json"
def load_cattle_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


data = load_cattle_data(cattle_data_file)
cow = data[0]
first_weight_date = cow["weights"][0]["date"]
start_date = datetime.strptime(first_weight_date, "%Y-%m-%d")



accuracy_results = []
non_results = []
result_dict = {}

for cow in data[:100]:
        
    accuracy, plateau_date, real_plateau_date = prediction_accuracy(cow, start_date, window_size=8, threshold=0.2, min_duration=2)
    result_dict[cow["cowId"]] = {
        "predicted_plateau": plateau_date,
        "real_plateau": real_plateau_date,
        "accuracy": accuracy
        }
    
    accuracy_results.append(accuracy)


# put results in a JSON file
with open("accuracy_results_dictionary.json", "w") as f:
    json.dump(result_dict, f, indent=2)


# plot distribution of accuracy results
import matplotlib.pyplot as plt
plt.hist(accuracy_results, bins=20, edgecolor='black')
plt.title('Distribution of Prediction Accuracy')
plt.xlabel('Days Difference')
plt.ylabel('Frequency')
plt.axvline(np.mean(accuracy_results), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {np.mean(accuracy_results):.2f} days')
plt.axvline(np.median(accuracy_results), color='blue', linestyle='dashed', linewidth=1, label=f'Median: {np.median(accuracy_results):.2f} days')
plt.legend()
plt.tight_layout()
plt.show()
