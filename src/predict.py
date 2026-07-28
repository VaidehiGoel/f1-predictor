import pandas as pd
import joblib

from configs.config import MODELS_DIR
from src.data_collection import get_session_results
from src.data_cleaning import clean_lap_times
from src.feature_engineering import add_qualifying_flags, fill_missing_form
from src.modeling import select_features_and_target


def build_upcoming_race_row(year: int, round_number: int, event_name: str) -> pd.DataFrame:
    quali_results = get_session_results(year, round_number, "Q", event_name)
    quali_results = pd.DataFrame(quali_results)

    if quali_results.empty:
        raise ValueError(
            f"No qualifying data available for {event_name} ({year}, Round {round_number}). "
            "This likely means qualifying hasn't happened yet, or the race/round doesn't exist."
        )

    quali_results = clean_lap_times(quali_results)

    upcoming_race_row = quali_results.copy()
    upcoming_race_row["SessionType"] = "R"
    upcoming_race_row["GridPosition"] = upcoming_race_row["Position"]

    num_drivers = len(upcoming_race_row)
    upcoming_race_row["GridPosition"] = upcoming_race_row["GridPosition"].fillna(num_drivers)

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
    upcoming = build_upcoming_race_row(year, round_number, event_name)

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


def predict_race(year: int, round_number: int, event_name: str, featured_historical_df: pd.DataFrame) -> pd.DataFrame:
    model = joblib.load(MODELS_DIR / "xgb_ranker.pkl")
    fitted_values = joblib.load(MODELS_DIR / "fitted_values.pkl")

    prediction_row = assemble_prediction_row(year, round_number, event_name, featured_historical_df)

    prediction_row = add_qualifying_flags(prediction_row, fitted_values["max_q1"], fitted_values["max_q2"])
    prediction_row = fill_missing_form(prediction_row, fitted_values["overall_avg_position"])

    X_pred, _ = select_features_and_target(prediction_row)

    X_pred = X_pred.astype(float)
    X_pred = X_pred.reset_index(drop=True)

    prediction_row = prediction_row.reset_index(drop=True)
    prediction_row["PredictedScore"] = model.predict(X_pred)

    prediction_row = prediction_row.sort_values("PredictedScore")
    prediction_row["PredictedRank"] = range(1, len(prediction_row) + 1)
    print(prediction_row.isna().sum())
    return prediction_row