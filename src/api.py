from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
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

historical_data = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading and preparing historical data...")

    df = load_all_seasons(SEASONS)
    featured_df = build_race_level_dataset(df)
    featured_df = drop_rows_with_missing_target(featured_df)
    featured_df = add_recent_form_feature(featured_df)
    featured_df = add_team_form_feature(featured_df)
    featured_df = add_teammate_form_feature(featured_df)
    featured_df = add_team_reliability_feature(featured_df)
    featured_df = add_circuit_history_feature(featured_df)

    historical_data["featured_df"] = featured_df
    print("Historical data ready.")

    yield

    historical_data.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "F1 Race Prediction API is running"}



@app.get("/predict")
def predict(year: int, round_number: int, event_name: str):
    featured_df = historical_data["featured_df"]

    try:
        result = predict_race(
            year=year,
            round_number=round_number,
            event_name=event_name,
            featured_historical_df=featured_df
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    output_columns = ["Abbreviation", "FullName", "GridPosition", "PredictedRank"]
    return result[output_columns].to_dict(orient="records")