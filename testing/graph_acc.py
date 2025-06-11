'''

This script processes the output log of a grid search and visualises the results.
Displays the average accuracy for each fixed parameter.
I am not entirely sure if this is the best way to visualise the results.

'''


from collections import defaultdict

import matplotlib.pyplot as plt


# open txt file of results from grid search
def load_grid_search_results(file_path):
    with open(file_path, "r") as f:
        results = f.readlines()
    return [line.strip() for line in results]

file_path = "./testing/graph_accuracy_results6.txt"
results = load_grid_search_results(file_path)

# plot the results of the grid search
def plot_grid_search_results(results):
    window_sizes = []
    thresholds = []
    min_durations = []
    accuracies = []

    for line in results:
        parts = line.split(", ")
        window_size = int(parts[0].split(": ")[1])
        threshold = float(parts[1].split(": ")[1])
        min_duration = int(parts[2].split(": ")[1].replace(" => Average Accuracy", ""))
        accuracy = float(parts[2].split(": ")[2].replace(" days", ""))


        window_sizes.append(window_size)
        thresholds.append(threshold)
        min_durations.append(min_duration)
        accuracies.append(accuracy)

    return window_sizes, thresholds, min_durations, accuracies

window_sizes, thresholds, min_durations, accuracies = plot_grid_search_results(results)


def average_by_param(param_list, accuracies):
    param_acc = defaultdict(list)
    for param, acc in zip(param_list, accuracies):
        param_acc[param].append(acc)
    return {k: sum(v)/len(v) for k, v in param_acc.items()}

avg_acc_window = average_by_param(window_sizes, accuracies)
avg_acc_threshold = average_by_param(thresholds, accuracies)
avg_acc_min_duration = average_by_param(min_durations, accuracies)

print(avg_acc_threshold)


def plot_average_accuracy(avg_acc, title, xlabel):
    plt.figure(figsize=(10, 6))
    plt.bar(avg_acc.keys(), avg_acc.values(), color='skyblue')
    plt.xlabel(xlabel)
    plt.ylabel('Average Accuracy (days)')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_average_accuracy(avg_acc_window, "Average Accuracy by Window Size", "Window Size (days)")
plot_average_accuracy(avg_acc_threshold, "Average Accuracy by Threshold", "Threshold (%)")
plot_average_accuracy(avg_acc_min_duration, "Average Accuracy by Minimum Duration", "Minimum Duration (days)")






