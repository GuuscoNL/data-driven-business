from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from math import sqrt

def calculate_baseline(df):
    baseline = df['anm_tot_fh'].mean()

    y_pred = [baseline] * len(df)
    y_true = df['anm_tot_fh']

    baseline_rmse = sqrt(mean_squared_error(y_true, y_pred))
    baseline_r2 = r2_score(y_true, y_pred)

    return baseline_rmse, baseline_r2