'''

This module runs the prediction function and compares the result to the real plateau integer stored in the cow data.
Returns the difference in days between the prediction and the real date. Also returns the predcited date and real date.

Maybe can toggle absolute value of difference to create a distribution of prediction accuracy.

'''




from models.plateau_detection import detect_plateau
from models.rolling_regression import rolling_regression

def prediction_accuracy(cow, start_date, window_size, threshold, min_duration):
    # find the gradient of the weight change graph using rolling regression
    slope_data = rolling_regression(cow, window_size)
    # detect plateau using the slope data from rolling regression
    plateau_date = detect_plateau(slope_data, threshold, min_duration)

    # get the real plateau date stored the cow data
    real_plateau_date = cow.get('plateau_day', None)
    #print(f"Real plateau date: {real_plateau_date}")

    # If the detect_plateau returns a day, then this function returns the accuracy, else returns 250 to mark as an outlier
    if plateau_date != 250:
        plateau_date = (plateau_date - start_date).days + 1  # Convert to days since start date
        #print(f"Plateau detected on day {plateau_date}")

        # If the model returns a prediction, return the difference in days
        return abs(plateau_date - real_plateau_date), plateau_date, real_plateau_date
    else:
        return 250, 250, real_plateau_date  # No plateau detected, return a sentinel value
    
