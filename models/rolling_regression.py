'''

This module breaks the cattle weight data into multiple windows and performs a linear regression on each window.
It returns a list of tuples containing the date and the slope of the regression line for 

'''




import pandas as pd
from sklearn.linear_model import LinearRegression
from typing import List, Tuple, Dict

def rolling_regression(cow_json_data: Dict, window_size: int = 14) -> List[Tuple[str, float]]:

    # Extract weights from the cow JSON data
    weights = cow_json_data["weights"]

    # 2. Convert to DataFrame
    df = pd.DataFrame(weights)
    df["date"] = pd.to_datetime(df["date"])
    df["day"] = (df["date"] - df["date"].min()).dt.days  # convert date to number
    df["weight"] = df["weight"].astype(float)

    # 3. Perform rolling linear regression
    slopes = []

    # Initate the model
    model = LinearRegression()

    for i in range(len(df) - window_size + 1):
        window = df.iloc[i:i+window_size]
        X = window["day"].to_numpy().reshape(-1, 1)
        y = window["weight"].to_numpy()

        model.fit(X, y)
        slope = model.coef_[0]
        slopes.append((window.iloc[-1]["date"], slope))

    return slopes

