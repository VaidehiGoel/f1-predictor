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
)
from src.modeling import select_features_and_target, train_test_split_by_year, evaluate_predictions
from configs.config import SEASONS

df = load_all_seasons(SEASONS)

race_level_df = build_race_level_dataset(df)
race_level_df = drop_rows_with_missing_target(race_level_df)
race_level_df = add_recent_form_feature(race_level_df)
race_level_df = add_team_form_feature(race_level_df)
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