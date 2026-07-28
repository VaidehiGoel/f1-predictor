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
from configs.config import SEASONS, PROCESSED_DATA_DIR

df = load_all_seasons(SEASONS)

featured_df = build_race_level_dataset(df)
featured_df = drop_rows_with_missing_target(featured_df)
featured_df = add_recent_form_feature(featured_df)
featured_df = add_team_form_feature(featured_df)
featured_df = add_teammate_form_feature(featured_df)
featured_df = add_team_reliability_feature(featured_df)
featured_df = add_circuit_history_feature(featured_df)

featured_df.to_csv(PROCESSED_DATA_DIR / "featured_historical.csv", index=False)
print(f"Saved {len(featured_df)} rows to featured_historical.csv")