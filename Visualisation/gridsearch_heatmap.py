'''

This script visualizes the results of a grid search for average accuracy.
It is used to hone in on the best parameters for the plateau detection model.

'''




import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_grid_search_results(file_path):
    with open(file_path, "r") as f:
        results = f.readlines()
    return [line.strip() for line in results]

file_path = "./testing/grid_search_log.txt"
results = load_grid_search_results(file_path)

data_list = []
for line in results:
    parts = line.split(", ")
    window_size = int(parts[0].split(": ")[1])
    threshold = float(parts[1].split(": ")[1])
    min_duration = int(parts[2].split(": ")[1].replace(" => Average Accuracy", ""))
    accuracy = float(parts[2].split(": ")[2].replace(" days", ""))

    data_list.append({
        'Window Size': window_size,
        'Threshold': threshold,
        'Min Duration': min_duration,
        'Average Accuracy': accuracy
    })

df = pd.DataFrame(data_list)

# Filter out the clearly bad 250.00 day results for better visualization range
# We'll still keep them in mind for interpretation, but they skew the color scale.
df_filtered = df[df['Average Accuracy'] < 250]

print("Data Head:")
print(df.head())
print("\nFiltered Data Head:")
print(df_filtered.head())

# Create a figure and a set of subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 12), sharex=True, sharey=True)
axes = axes.flatten() # Flatten the 2x2 array of axes for easy iteration

min_durations = sorted(df['Min Duration'].unique())

for i, md in enumerate(min_durations):
    # Filter data for the current Min Duration
    df_md = df[df['Min Duration'] == md]

    # Pivot the table for heatmap: Window Size on x, Threshold on y, Accuracy as value
    heatmap_data = df_md.pivot_table(index='Threshold', columns='Window Size', values='Average Accuracy')

    # Create the heatmap
    sns.heatmap(
        heatmap_data,
        ax=axes[i],
        annot=True,      # Show the accuracy values on the heatmap
        fmt=".1f",       # Format annotations to one decimal place
        cmap="plasma_r", # 'viridis_r' or 'plasma_r' for lower values being "better" (brighter/more distinct)
        linewidths=.5,   # Add lines between cells
        cbar=True,       # Show color bar
        vmin=df_filtered['Average Accuracy'].min(), # Set min for color scale from filtered data
        vmax=df_filtered['Average Accuracy'].max() # Set max for color scale from filtered data
    )
    axes[i].set_title(f'Min Duration: {md} days')
    axes[i].set_xlabel('Window Size')
    axes[i].set_ylabel('Threshold')

plt.suptitle('Average Accuracy (Days) by Window Size, Threshold, and Min Duration', fontsize=18)
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to make room for suptitle
plt.show()