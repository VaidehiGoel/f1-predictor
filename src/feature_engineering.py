import pandas as pd
from configs.config import RAW_DATA_DIR, PROCESSED_DATA_DIR


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


def drop_rows_with_missing_target(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna(subset=["Position"])
    return df


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


def add_circuit_history_feature(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["Year", "RoundNumber"])

    df["CircuitAvgPosition"] = (
        df.groupby(["DriverId", "EventName"])["Position"]
        .transform(lambda x: x.shift(1).expanding().mean())
    )

    return df


def add_qualifying_flags(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ReachedQ2"] = df["Q2_seconds"].notna()
    df["ReachedQ3"] = df["Q3_seconds"].notna()

    max_q1 = df["Q1_seconds"].max()
    max_q2 = df["Q2_seconds"].max()

    df["Q1_seconds"] = df["Q1_seconds"].fillna(max_q1)
    df["Q2_seconds"] = df["Q2_seconds"].fillna(max_q2)
    df["Q3_seconds"] = df["Q3_seconds"].fillna(max_q2)

    return df


def fill_missing_form(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    overall_avg_position = df["Position"].mean()

    df["DriverHasHistory"] = df["RecentFormPosition"].notna()
    df["TeamHasHistory"] = df["RecentFormTeamPosition"].notna()
    df["CircuitHasHistory"] = df["CircuitAvgPosition"].notna()
    df["TeammateHistoryExists"] = df["RecentTeammateGap"].notna()
    df["TeamDNFHistoryExists"] = df["RecentTeamDNFRate"].notna()

    df["RecentFormPosition"] = df["RecentFormPosition"].fillna(overall_avg_position)
    df["RecentFormTeamPosition"] = df["RecentFormTeamPosition"].fillna(overall_avg_position)
    df["CircuitAvgPosition"] = df["CircuitAvgPosition"].fillna(overall_avg_position)
    df["RecentTeammateGap"] = df["RecentTeammateGap"].fillna(0)
    df["RecentTeamDNFRate"] = df["RecentTeamDNFRate"].fillna(0)

    return df

def compute_teammate_gap(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    team_race_positions = df.groupby(["Year", "RoundNumber", "TeamId"])["Position"].transform(
        lambda x: x.sum()
    )

    df["TeammateGap"] = df["Position"] - (team_race_positions - df["Position"])

    return df


def add_teammate_form_feature(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["Year", "RoundNumber"])
    df = compute_teammate_gap(df)

    df["RecentTeammateGap"] = (
        df.groupby("DriverId")["TeammateGap"]
        .transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    )

    df = df.drop(columns=["TeammateGap"])

    return df

def add_team_reliability_feature(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values(["Year", "RoundNumber"])

    team_round_dnf = (
        df.groupby(["Year", "RoundNumber", "TeamId"])["Status"]
        .apply(lambda x: (x == "Retired").mean())
        .reset_index()
        .rename(columns={"Status": "TeamRoundDNFRate"})
    )

    team_round_dnf = team_round_dnf.sort_values(["Year", "RoundNumber"])
    team_round_dnf["RecentTeamDNFRate"] = (
        team_round_dnf.groupby("TeamId")["TeamRoundDNFRate"]
        .transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    )

    df = df.merge(
        team_round_dnf[["Year", "RoundNumber", "TeamId", "RecentTeamDNFRate"]],
        on=["Year", "RoundNumber", "TeamId"],
        how="left"
    )

    return df

def finalize_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop(columns=["SessionType"])
    return df


def save_final_dataset(df: pd.DataFrame) -> None:
    file_path = PROCESSED_DATA_DIR / "model_ready_dataset.csv"
    df.to_csv(file_path, index=False)
    print(f"Saved final dataset to {file_path}")