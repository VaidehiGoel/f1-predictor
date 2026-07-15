import pandas as pd


def build_race_level_dataset(df: pd.DataFrame) -> pd.DataFrame:
    race_df = df[df["SessionType"] == "R"].copy()
    race_df = race_df.drop(columns=["Q1_seconds", "Q2_seconds", "Q3_seconds", "Q1", "Q2", "Q3"])

    quali_df = df[df["SessionType"] == "Q"]
    quali_features = quali_df[["Year", "RoundNumber", "DriverId", "Q1_seconds", "Q2_seconds", "Q3_seconds"]]

    merged = race_df.merge(
        quali_features,
        on=["Year", "RoundNumber", "DriverId"],
        how="left"
    )

    return merged