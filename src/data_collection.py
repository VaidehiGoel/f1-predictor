import fastf1
import pandas as pd
from datetime import timedelta
from fastf1.exceptions import RateLimitExceededError
from configs.config import RAW_DATA_DIR 


def get_session_results(year: int, round_number: int, session_type: str,event_name: str) -> pd.DataFrame:
    session = fastf1.get_session(year, round_number, session_type)
    session.load(laps=False, telemetry=False, weather=False)

    results = session.results.copy()

    results["Year"] = year
    results["RoundNumber"] = round_number
    results["SessionType"] = session_type
    results["EventName"] = event_name

    return results


def collect_season(year: int) -> pd.DataFrame:
    schedule = fastf1.get_event_schedule(year)
    all_results = []

    today = pd.Timestamp.now()

    for _, event in schedule.iterrows():
        round_number = event["RoundNumber"]
        event_date = event["EventDate"]
        event_name = event["EventName"]

        if event_date > today + timedelta(days=3):
            print(f"Skipping round {round_number} — too far in the future ({event_date.date()})")
            continue

        for session_type in ["Q", "R"]:
            try:
                df = get_session_results(year, round_number, session_type,event_name)
                all_results.append(df)
            except RateLimitExceededError:
                raise   
            except Exception as e:
                print(f"Skipped {year} round {round_number} ({session_type}): {e}")

    return pd.concat(all_results, ignore_index=True)

def collect_multiple_seasons(years: list[int]) -> pd.DataFrame:
    all_seasons = []

    for year in years:
        try:
            season_df = collect_season(year)
            all_seasons.append(season_df)

        except RateLimitExceededError:
            print(f"Rate limit hit while collecting {year}. Stopping early — rerun later to continue (cached data will load instantly).")
            break
       
        except Exception as e:
            print(f"Failed to collect season {year}: {e}")

    return pd.concat(all_seasons, ignore_index=True)



def save_season_data(df: pd.DataFrame, year: int) -> None:
    file_path = RAW_DATA_DIR / f"results_{year}.csv"
    df_year=df[df["Year"] == year]
    df_year.to_csv(file_path, index=False)
    print(f"Saved season {year} data to {file_path}")

def save_all_seasons(df: pd.DataFrame, years: list[int]) -> None:
    for year in years:
        save_season_data(df, year)