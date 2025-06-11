'''

This module implements a grid search for hyperparameter tuning of the prediction model.
It evaluates different combinations of window sizes, thresholds, and minimum durations to find the best parameters that minimize prediction error.
This function logs the results to a specified file so we can analyse the different parameters, specifically in the heatmap scipt.

'''

# import the prediction_accuracy function to evaluate the model's performance
from models.prediction_accuracy import prediction_accuracy


def grid_search(data, start_date, window_sizes, thresholds, min_durations, log_file_path=None):
    best_accuracy = float('inf')
    best_params = (None, None, None)


    with open(log_file_path, "w") as log_file:
        for window_size in window_sizes:
            for threshold in thresholds:
                for min_duration in min_durations:
                    total_accuracy = 0
                    for cow in data:


                        accuracy, prediction_int, actual_int = prediction_accuracy(cow, start_date, window_size, threshold, min_duration)
                        total_accuracy += accuracy

                    average_accuracy = total_accuracy / len(data)
                    message = (f"Window Size: {window_size}, Threshold: {threshold}, Min Duration: {min_duration} => Average Accuracy: {average_accuracy:.2f} days")
                    print(message)
                    log_file.write(message + "\n")
                    if average_accuracy < best_accuracy:
                        best_accuracy = average_accuracy
                        best_params = (window_size, threshold, min_duration)

    return best_params, best_accuracy

