from src.data_collection import collect_multiple_seasons,save_all_seasons
from configs.config import SEASONS


df = collect_multiple_seasons(SEASONS)
save_all_seasons(df,SEASONS)