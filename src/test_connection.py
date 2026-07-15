from src.eda import load_all_seasons
from src.feature_engineering import (
    build_race_level_dataset,
    add_recent_form_feature,
    add_team_form_feature,
    fill_missing_form,
    add_circuit_history_feature,
)
from configs.config import SEASONS

df = load_all_seasons(SEASONS)

race_level_df = build_race_level_dataset(df)
race_level_df = add_recent_form_feature(race_level_df)
race_level_df = add_team_form_feature(race_level_df)
race_level_df = add_circuit_history_feature(race_level_df)
race_level_df = fill_missing_form(race_level_df)

print(race_level_df["CircuitAvgPosition"].isna().sum())
print(race_level_df[["DriverHasHistory", "TeamHasHistory", "CircuitHasHistory"]].value_counts())