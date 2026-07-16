import pandas as pd


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