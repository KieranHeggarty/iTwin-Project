'''

This script is used to graph the made up data of cattle weights.
Also shows the real plateau date and you can manually input the predicted plateau date to see how accurate the model is.

'''





import json
import matplotlib.pyplot as plt

# Set number of cows to graph
num = 1

# Load JSON data from file
with open("./Data/cattle-data.json", "r") as f:
    cattle_data = json.load(f)


# Plot weights for the first `num` cows
# plot the x ticks every 7 days
# plot 7 day moving average

for cow in cattle_data[:num]:
    dates = [entry["date"] for entry in cow["weights"]]
    weights = [entry["weight"] for entry in cow["weights"]]
    plateau_day = cow.get("plateau_day", None)

    # Calculate 7-day moving average
    moving_avg = []
    for i in range(len(weights)):
        if i < 6:
            moving_avg.append(None)  # Not enough data for moving average
        else:
            avg = sum(weights[i-6:i+1]) / 7
            moving_avg.append(avg)


    plt.figure(figsize=(12, 6))
    plt.plot(dates, weights, label=f"{cow['name']} - Daily Weights", marker='o', linestyle='-', markersize=3)
    plt.plot(dates, moving_avg, label=f"{cow['name']} - 7-Day Moving Avg", color='orange', linewidth=2)

    # plot the plateau day if it exists
    if plateau_day is not None:
        plateau_date = dates[plateau_day - 1]  # Adjust for zero-based index
        plt.axvline(x=plateau_date, color='red', linestyle='--', label=f"Plateau Day {plateau_day} ({plateau_date})")
        # If you want to manually input the predicted plateau day, change x=predicted date in line below
        plt.axvline(x=99, color='green', linestyle='--', label=f"Predicted Plateau Day {cow['plateau_day']} ({dates[cow['plateau_day'] - 1]})")

    plt.title(f"Weight Progression for {cow['name']}")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(dates[::7], rotation=45)
    #plt.grid()

    plt.legend()
    plt.tight_layout()
    
    # Show the plot
    plt.show()
