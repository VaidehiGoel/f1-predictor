from src.eda import load_all_seasons
from src.feature_engineering import build_race_level_dataset
from configs.config import SEASONS

df = load_all_seasons(SEASONS)
race_level_df = build_race_level_dataset(df)

print(race_level_df.shape)
print(race_level_df[["Abbreviation", "EventName", "Year", "GridPosition", "Q1_seconds", "Q2_seconds", "Q3_seconds", "Position"]].head(10))
print(race_level_df["Q1_seconds"].isna().sum())
