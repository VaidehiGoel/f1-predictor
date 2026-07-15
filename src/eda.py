import pandas as pd
from src.data_cleaning import load_and_clean_season
from configs.config import SEASONS


def load_all_seasons(years: list[int]) -> pd.DataFrame:
    all_seasons = [load_and_clean_season(year) for year in years]
    return pd.concat(all_seasons, ignore_index=True)


