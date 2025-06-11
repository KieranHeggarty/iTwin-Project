'''

This module contains functions to detect plateaus in time series data.
Slope data is calculated from rolling regression result and represents the rate of change over different time windows.

I plan to add edge case support, this function took a while to recognise obvious plateaus in testing.

'''




def detect_plateau(slope_data, threshold=0.05, min_duration=4):
    count = 0
    for i, (date, slope) in enumerate(slope_data):

        if slope < threshold: # if the rate of change of weight is below a threshold then we add one to the count.
            count += 1

            # if the count is >= min_duration, i.e. the cow has gained
            # weight below the threshold for min_duration days, then we have a plateau.
            if count >= min_duration:
                plateau_date =  slope_data[i - min_duration + 1][0]  # plateau start date
                return plateau_date
        else:
            count = 0
    return 250  # no plateau, chose 250 to mark as outlier for grid search and testing purposes








