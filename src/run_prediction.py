from src.eda import load_all_seasons
from src.feature_engineering import (
    build_race_level_dataset,
    drop_rows_with_missing_target,
    add_recent_form_feature,
    add_team_form_feature,
    add_teammate_form_feature,
    add_team_reliability_feature,
    add_circuit_history_feature,
)
from src.predict import predict_race
from configs.config import SEASONS

df = load_all_seasons(SEASONS)

featured_historical_df = build_race_level_dataset(df)
featured_historical_df = drop_rows_with_missing_target(featured_historical_df)
featured_historical_df = add_recent_form_feature(featured_historical_df)
featured_historical_df = add_team_form_feature(featured_historical_df)
featured_historical_df = add_teammate_form_feature(featured_historical_df)
featured_historical_df = add_team_reliability_feature(featured_historical_df)
featured_historical_df = add_circuit_history_feature(featured_historical_df)

result = predict_race(
    year=2026,
    round_number=11,
    event_name="Hungarian Grand Prix",
    featured_historical_df=featured_historical_df
)

print(result[["Abbreviation", "FullName", "GridPosition", "PredictedScore", "PredictedRank"]])