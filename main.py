'''

This is the main script and it takes an incomplete set of weights and after each update it checks if the cow has plateaued.
Right now it does not work well.

'''



import json
from datetime import datetime
from models.rolling_regression import rolling_regression
from models.plateau_detection import detect_plateau

def check_plateau_status(cow_id: str, new_date: str, new_weight: float, cattle_data_file: str) -> str:
    # Load cattle data
    with open(cattle_data_file, "r") as f:
        cattle_data = json.load(f)

    # Find the cow by ID
    cow = next((c for c in cattle_data if c["cowId"] == cow_id), None)
    if not cow:
        return f"Cow with ID {cow_id} not found."

    # Append the new weight entry
    cow["weights"].append({
        "date": new_date,
        "weight": new_weight
    })

    # Sort weights by date to ensure order
    cow["weights"].sort(key=lambda x: x["date"])

    # Run rolling regression and detect plateau
    slope_data = rolling_regression(cow, window_size=14)
    plateau = detect_plateau(slope_data, threshold=0.05, min_duration=4)

    # Save updated cattle data back to file
    with open(cattle_data_file, "w") as f:
        json.dump(cattle_data, f, indent=2)

    return "Yes, plateaued." if plateau != 250 else "No, still gaining."

# Example usage
if __name__ == "__main__":
    cattle_data_file = "./Data/cattle-data3.json"
    cow_id = "cow-0001"
    new_date = "2024-05-04"
    new_weight = 590.0

    result = check_plateau_status(cow_id, new_date, new_weight, cattle_data_file)
    print(result)