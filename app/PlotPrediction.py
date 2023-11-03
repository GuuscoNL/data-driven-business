import numpy as np
import matplotlib.pyplot as plt
import sklearn
import pandas as pd
import matplotlib
from sklearn.metrics import mean_squared_error

def plot_prediction(model, 
                    input_data: pd.DataFrame, 
                    ax: matplotlib.axes._axes.Axes, 
                    X: pd.DataFrame, 
                    y: pd.DataFrame):
    
    mean_prediction = model.predict(input_data)[0]
    pred_leaf_id = model.apply(input_data)[0]
    
    leaf_indices = model.apply(X)
    durations = np.array(y[leaf_indices == pred_leaf_id].tolist())

    percentile_95 = np.percentile(durations, 95)

    _, bins, _ = ax.hist(durations, bins=30, density=False, alpha=0.6, color='b', label='Historische storingsduur Data')
    ax.axvline(mean_prediction, color='r', linestyle='--', label=f'Mean Prediction = {mean_prediction:.0f}')
    ax.axvline(percentile_95, color='g', linestyle='--', label='95% Mark', linewidth=2)
    ax.set_xlabel('Duur storing (minuten)')
    ax.set_ylabel('Frequentie')
    ax.set_title('Storingsduur histogram')

    values_below_mean_prediction = durations[durations < mean_prediction]
    values_above_mean_prediction = durations[durations >= mean_prediction]
    percentage_below_mean = len(values_below_mean_prediction) / len(durations) * 100
    percentage_above_mean = len(values_above_mean_prediction) / len(durations) * 100

    right_side_color = 'orange'
    _, bins, _ = ax.hist(values_above_mean_prediction, bins=bins, alpha=0.6, color=right_side_color, label=f'Values Above Mean Prediction: {percentage_above_mean:.2f}%')

    labels = [
        f'Waardes onder voorspelling: {percentage_below_mean:.2f}%', 
        f'Voorspelling: {mean_prediction:.2f} min',
        f'95% van de data: {percentile_95:.2f} min', 
        f'Waardes boven voorspelling: {percentage_above_mean:.2f}%'
        ]
    ax.legend(labels=labels)


def get_95_interval(model, input_data, X, y):
    pred_leaf_id = model.apply(input_data)[0]
    
    leaf_indices = model.apply(X)
    durations = np.array(y[leaf_indices == pred_leaf_id].tolist())

    percentile_95 = np.percentile(durations, 95)
    
    # Calculate RMSE for the selected leaf
    leaf_durations = y[leaf_indices == pred_leaf_id].tolist()
    rmse = np.sqrt(mean_squared_error(leaf_durations, np.full(len(leaf_durations), np.mean(leaf_durations))))
    
    return {
        'interval': (5, percentile_95),
        'rmse': rmse
    }
