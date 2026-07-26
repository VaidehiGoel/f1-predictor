import pandas as pd
from src.data_collection import get_session_results


def build_upcoming_race_row(year: int, round_number: int) -> pd.DataFrame:
    quali_results = get_session_results(year, round_number, "Q")

    upcoming_race_row = quali_results.copy()
    upcoming_race_row["SessionType"] = "R"
    upcoming_race_row["GridPosition"] = upcoming_race_row["Position"]
    upcoming_race_row["Position"] = None
    upcoming_race_row["Status"] = None

    return upcoming_race_row


def get_latest_driver_stats(featured_df: pd.DataFrame) -> pd.DataFrame:
    featured_df = featured_df.sort_values(["Year", "RoundNumber"])
    latest_per_driver = featured_df.groupby("DriverId").tail(1)
    return latest_per_driver

def get_latest_circuit_stats(featured_df: pd.DataFrame, event_name: str) -> pd.DataFrame:
    circuit_df = featured_df[featured_df["EventName"] == event_name]
    circuit_df = circuit_df.sort_values(["Year", "RoundNumber"])

    latest_per_driver_at_circuit = circuit_df.groupby("DriverId").tail(1)

    return latest_per_driver_at_circuit

def assemble_prediction_row(year: int, round_number: int, event_name: str, featured_historical_df: pd.DataFrame) -> pd.DataFrame:
    upcoming = build_upcoming_race_row(year, round_number)

    latest_driver_stats = get_latest_driver_stats(featured_historical_df)
    latest_circuit_stats = get_latest_circuit_stats(featured_historical_df, event_name)

    driver_stat_cols = ["DriverId", "RecentFormPosition", "RecentFormTeamPosition",
                         "RecentTeammateGap", "RecentTeamDNFRate"]
    circuit_stat_cols = ["DriverId", "CircuitAvgPosition"]

    prediction_row = upcoming.merge(
        latest_driver_stats[driver_stat_cols],
        on="DriverId",
        how="left"
    )

    prediction_row = prediction_row.merge(
        latest_circuit_stats[circuit_stat_cols],
        on="DriverId",
        how="left"
    )

    return prediction_row

