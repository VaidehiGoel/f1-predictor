from src.eda import load_all_seasons
from src.feature_engineering import build_race_level_dataset
from configs.config import SEASONS
from src.feature_engineering import add_recent_form_feature,build_race_level_dataset,add_team_form_feature,fill_missing_form

df = load_all_seasons(SEASONS)
race_level_df = build_race_level_dataset(df)
race_level_df = add_recent_form_feature(race_level_df)
race_level_df = add_team_form_feature(race_level_df)
race_level_df = fill_missing_form(race_level_df)

print(race_level_df["RecentFormPosition"].isna().sum())
print(race_level_df["RecentFormTeamPosition"].isna().sum())
print(race_level_df[["DriverHasHistory", "TeamHasHistory"]].value_counts())

cadillac = race_level_df[race_level_df["TeamId"] == "cadillac"]
print(cadillac[["Year", "RoundNumber", "Abbreviation", "Position", "RecentFormPosition", "RecentFormTeamPosition", "DriverHasHistory", "TeamHasHistory"]].head(6))