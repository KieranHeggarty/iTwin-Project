'''

This script generates a JSON file with fake cattle weight data.
The weights follow a logorithmic growth with random noise,
then plateau after a certain number of days.


'''




import json
import random
import math
from datetime import datetime, timedelta

def generate_weight_curve(start_weight: float, plateau_day: int, total_days: int):
    weights = []
    date = datetime(2024, 1, 1)

    # Compute expected gain over time using a scaled logarithmic approach
    scale = random.uniform(180, 220)  # Controls the sharpness of the growth curve

    for day in range(total_days):
        if day < plateau_day:
            growth = scale * math.log(day/20 + 5) - 322 # +2 avoids log(0) and slows early growth
            noise = random.uniform(-0.007, 0.007)
            weight = start_weight + growth + (start_weight + growth) * noise
        else:
            # Gradual plateau: maintain weight ±0.5kg
            prev_weight = weights[plateau_day-1]["weight"]
            fluctuation = random.uniform(-0.007, 0.007)
            weight = prev_weight + prev_weight * fluctuation

        weights.append({
            "date": date.strftime("%Y-%m-%d"),
            "weight": round(weight, 1)
        })
        date += timedelta(days=1)

    return weights

def generate_fake_cattle(num_cows=1, total_days=180):
    cattle = []
    for i in range(1, num_cows + 1):
        start_weight = random.uniform(395, 455)
        plateau_day = random.randint(100, 160)

        cow = {
            "cowId": f"cow-{i:04d}",
            "name": f"Cow {i}",
            "weights": generate_weight_curve(start_weight, plateau_day, total_days),
            "ready": True,
            "plateau_day": plateau_day
        }
        cattle.append(cow)
    return cattle

# Generate and save JSON file
if __name__ == "__main__":
    fake_data = generate_fake_cattle(10000)
    with open("./Data/cattle-data1.json", "w") as f:
        json.dump(fake_data, f, indent=2)

    print("✅ Generated cattle-data.json with realistic growth and plateau.")
