import joblib
from xgboost import XGBRanker

from src.eda import load_all_seasons
from src.feature_engineering import (
    build_race_level_dataset,
    drop_rows_with_missing_target,
    add_recent_form_feature,
    add_team_form_feature,
    add_teammate_form_feature,
    add_team_reliability_feature,
    add_circuit_history_feature,
    add_qualifying_flags,
    fill_missing_form,
    finalize_dataset,
)
from src.modeling import select_features_and_target, train_test_split_by_year, evaluate_predictions
from configs.config import SEASONS, MODELS_DIR

df = load_all_seasons(SEASONS)

race_level_df = build_race_level_dataset(df)
race_level_df = drop_rows_with_missing_target(race_level_df)
race_level_df = add_recent_form_feature(race_level_df)
race_level_df = add_team_form_feature(race_level_df)
race_level_df = add_teammate_form_feature(race_level_df)
race_level_df = add_team_reliability_feature(race_level_df)
race_level_df = add_circuit_history_feature(race_level_df)

max_q1 = race_level_df["Q1_seconds"].max()
max_q2 = race_level_df["Q2_seconds"].max()
race_level_df = add_qualifying_flags(race_level_df, max_q1, max_q2)

overall_avg_position = race_level_df["Position"].mean()
race_level_df = fill_missing_form(race_level_df, overall_avg_position)

race_level_df = finalize_dataset(race_level_df)

train_df, test_df = train_test_split_by_year(race_level_df, test_year=2025)

X_train, y_train = select_features_and_target(train_df)
X_test, y_test = select_features_and_target(test_df)

group_sizes_train = train_df.groupby(["Year", "RoundNumber"]).size().values

model = XGBRanker(
    objective="rank:pairwise",
    n_estimators=20,
    max_depth=3,
    learning_rate=0.1
)
model.fit(X_train, y_train, group=group_sizes_train)

joblib.dump(model, MODELS_DIR / "xgb_ranker.pkl")
print(f"Model saved to {MODELS_DIR / 'xgb_ranker.pkl'}")

fitted_values = {
    "overall_avg_position": overall_avg_position,
    "max_q1": max_q1,
    "max_q2": max_q2,
}
joblib.dump(fitted_values, MODELS_DIR / "fitted_values.pkl")
print(f"Fitted values saved to {MODELS_DIR / 'fitted_values.pkl'}")

test_df = test_df.copy()
test_df["PredictedPosition"] = model.predict(X_test)

evaluate_predictions(test_df)