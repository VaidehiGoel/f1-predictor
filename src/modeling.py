import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import mean_absolute_error, mean_squared_error

def select_features_and_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    feature_columns = [
        "GridPosition", "Q1_seconds", "Q2_seconds", "Q3_seconds",
        "RecentFormPosition", "RecentFormTeamPosition", "CircuitAvgPosition",
        "DriverHasHistory", "TeamHasHistory", "CircuitHasHistory",
        "ReachedQ2", "ReachedQ3"
    ]

    X = df[feature_columns]
    y = df["Position"]

    return X, y


def train_test_split_by_year(df: pd.DataFrame, test_year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_df = df[df["Year"] < test_year]
    test_df = df[df["Year"] == test_year]

    return train_df, test_df


def race_spearman(group: pd.DataFrame) -> float:
    correlation, _ = spearmanr(group["PredictedPosition"], group["Position"])
    return correlation


def evaluate_predictions(test_df: pd.DataFrame) -> None:
    mae = mean_absolute_error(test_df["Position"], test_df["PredictedPosition"])
    rmse = mean_squared_error(test_df["Position"], test_df["PredictedPosition"]) ** 0.5

    spearman_all = test_df.groupby(["Year", "RoundNumber"]).apply(race_spearman).mean()

    finished_df = test_df[test_df["Status"].isin(["Finished", "Lapped"])]
    spearman_finished = finished_df.groupby(["Year", "RoundNumber"]).apply(race_spearman).mean()

    print(f"MAE: {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"Mean Spearman (all rows): {spearman_all:.3f}")
    print(f"Mean Spearman (finished only): {spearman_finished:.3f}")