from sklearn.linear_model import LinearRegression
from src.eda import load_all_seasons
from src.feature_engineering import (
    build_race_level_dataset,
    drop_rows_with_missing_target,
    add_recent_form_feature,
    add_team_form_feature,
    add_circuit_history_feature,
    add_qualifying_flags,
    fill_missing_form,
    finalize_dataset,
    save_final_dataset,
    add_teammate_form_feature,
    add_team_reliability_feature,
)
from src.modeling import select_features_and_target, train_test_split_by_year, evaluate_predictions
from configs.config import SEASONS

df = load_all_seasons(SEASONS)

race_level_df = build_race_level_dataset(df)
race_level_df = drop_rows_with_missing_target(race_level_df)
race_level_df = add_recent_form_feature(race_level_df)
race_level_df = add_team_form_feature(race_level_df)
race_level_df = add_teammate_form_feature(race_level_df)
race_level_df = add_team_reliability_feature(race_level_df)
race_level_df = add_circuit_history_feature(race_level_df)
race_level_df = add_qualifying_flags(race_level_df)
race_level_df = fill_missing_form(race_level_df)
race_level_df = finalize_dataset(race_level_df)

save_final_dataset(race_level_df)

train_df, test_df = train_test_split_by_year(race_level_df, test_year=2025)

X_train, y_train = select_features_and_target(train_df)
X_test, y_test = select_features_and_target(test_df)

model = LinearRegression()
model.fit(X_train, y_train)

test_df = test_df.copy()
test_df["PredictedPosition"] = model.predict(X_test)

evaluate_predictions(test_df)

print(train_df[["Year", "RoundNumber"]].head(10))
print(train_df["RoundNumber"].is_monotonic_increasing)

for year in sorted(train_df["Year"].unique()):
    subset = train_df[train_df["Year"] == year]
    print(year, subset["RoundNumber"].is_monotonic_increasing)

overall_avg_position = race_level_df["Position"].mean()
race_level_df = fill_missing_form(race_level_df, overall_avg_position)

max_q1 = race_level_df["Q1_seconds"].max()
max_q2 = race_level_df["Q2_seconds"].max()
race_level_df = add_qualifying_flags(race_level_df, max_q1, max_q2)

print(X_train[["RecentFormPosition", "RecentFormTeamPosition", "RecentTeammateGap"]].corr())
print((X_train["TeammateHistoryExists"] == X_train["DriverHasHistory"]).mean())