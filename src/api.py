from contextlib import asynccontextmanager
import pandas as pd
import fastf1
from fastapi import FastAPI, HTTPException

from src.data_collection import get_session_results
from src.predict import predict_race
from configs.config import PROCESSED_DATA_DIR

from fastapi.middleware.cors import CORSMiddleware

CURRENT_SEASON = 2026

historical_data = {}


def check_available_races(schedule_df: pd.DataFrame, year: int) -> list[dict]:
    available_races = []

    for _, event in schedule_df.iterrows():
        round_number = event["RoundNumber"]
        event_name = event["EventName"]

        try:
            quali_check = get_session_results(year, round_number, "Q", event_name)
            quali_check = pd.DataFrame(quali_check)
            if not quali_check.empty:
                available_races.append({
                    "year": year,
                    "round_number": int(round_number),
                    "event_name": event_name
                })
        except Exception:
            continue

    return available_races


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading pre-built historical dataset...")
    featured_df = pd.read_csv(PROCESSED_DATA_DIR / "featured_historical.csv")
    historical_data["featured_df"] = featured_df
    print("Historical data ready.")

    print("Checking available races for current season...")
    current_schedule_df = fastf1.get_event_schedule(CURRENT_SEASON)
    historical_data["available_races"] = check_available_races(current_schedule_df, CURRENT_SEASON)
    print(f"Total races available: {len(historical_data['available_races'])}")

    yield
    historical_data.clear()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://f1-predictor-teal.vercel.app","https://gridcast-f1.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "F1 Race Prediction API is running"}


@app.get("/races")
def get_races():
    return historical_data["available_races"]


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

    output_columns = ["Abbreviation", "FullName", "TeamName", "TeamColor", "GridPosition", "PredictedRank"]
    return result[output_columns].to_dict(orient="records")