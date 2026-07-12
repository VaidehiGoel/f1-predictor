import pandas as pd
from configs.config import RAW_DATA_DIR,PROCESSED_DATA_DIR

def clean_lap_times(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["Q1_seconds"] = pd.to_timedelta(df["Q1"]).dt.total_seconds()
    df["Q2_seconds"] = pd.to_timedelta(df["Q2"]).dt.total_seconds()
    df["Q3_seconds"] = pd.to_timedelta(df["Q3"]).dt.total_seconds()

    return df

def drop_leakage_and_redundant_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    columns_to_drop = ["Time", "ClassifiedPosition"]
    df = df.drop(columns=columns_to_drop)

    return df

def clean_season_data(df:pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = clean_lap_times(df)
    df = drop_leakage_and_redundant_columns(df)

    return df
def load_and_clean_season(year: int) -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_DIR / f"results_{year}.csv")
    df_clean = clean_season_data(df)
    return df_clean


def save_cleaned_season(df: pd.DataFrame, year: int) -> None:
    file_path = PROCESSED_DATA_DIR / f"cleaned_{year}.csv"
    df.to_csv(file_path, index=False)
    print(f"Saved cleaned season {year} data to {file_path}")

def clean_and_save_all_seasons(years: list[int]) -> None:
    for year in years:
        df_clean = load_and_clean_season(year)
        save_cleaned_season(df_clean, year)