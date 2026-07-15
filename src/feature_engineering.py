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

def add_recent_form_feature(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["Year", "RoundNumber"])

    df["RecentFormPosition"] = (
        df.groupby("DriverId")["Position"]
        .transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    )

    return df

def add_team_form_feature(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["Year", "RoundNumber"])

    team_round_avg = (
        df.groupby(["Year", "RoundNumber", "TeamId"])["Position"]
        .mean()
        .reset_index()
        .rename(columns={"Position": "TeamRoundAvgPosition"})
    )

    team_round_avg = team_round_avg.sort_values(["Year", "RoundNumber"])
    team_round_avg["RecentFormTeamPosition"] = (
        team_round_avg.groupby("TeamId")["TeamRoundAvgPosition"]
        .transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    )

    df = df.merge(
        team_round_avg[["Year", "RoundNumber", "TeamId", "RecentFormTeamPosition"]],
        on=["Year", "RoundNumber", "TeamId"],
        how="left"
    )

    return df

def fill_missing_form(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    overall_avg_position = df["Position"].mean()

    df["DriverHasHistory"] = df["RecentFormPosition"].notna()
    df["TeamHasHistory"] = df["RecentFormTeamPosition"].notna()

    df["RecentFormPosition"] = df["RecentFormPosition"].fillna(overall_avg_position)
    df["RecentFormTeamPosition"] = df["RecentFormTeamPosition"].fillna(overall_avg_position)

    return df