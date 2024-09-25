from src.data_prep.championship_past_data import get_all_season_data
import pandas as pd

# Constants for season data URLs
GOAL_URLS = {
    "2015-2016": "https://www.worldfootball.net/goalgetter/eng-championship-2015-2016/",
    "2016-2017": "https://www.worldfootball.net/goalgetter/eng-championship-2016-2017/",
    "2017-2018": "https://www.worldfootball.net/goalgetter/eng-championship-2017-2018/",
    "2018-2019": "https://www.worldfootball.net/goalgetter/eng-championship-2018-2019/",
    "2019-2020": "https://www.worldfootball.net/goalgetter/eng-championship-2019-2020/",
    "2020-2021": "https://www.worldfootball.net/goalgetter/eng-championship-2020-2021/",
    "2021-2022": "https://www.worldfootball.net/goalgetter/eng-championship-2021-2022/",
    "2022-2023": "https://www.worldfootball.net/goalgetter/eng-championship-2022-2023/",
    "2023-2024": "https://www.worldfootball.net/goalgetter/eng-championship-2023-2024/",
}

ASSIST_URLS = {
    "2015-2016": "https://www.worldfootball.net/assists/eng-championship-2015-2016/",
    "2016-2017": "https://www.worldfootball.net/assists/eng-championship-2016-2017/",
    "2017-2018": "https://www.worldfootball.net/assists/eng-championship-2017-2018/",
    "2018-2019": "https://www.worldfootball.net/assists/eng-championship-2018-2019/",
    "2019-2020": "https://www.worldfootball.net/assists/eng-championship-2019-2020/",
    "2020-2021": "https://www.worldfootball.net/assists/eng-championship-2020-2021/",
    "2021-2022": "https://www.worldfootball.net/assists/eng-championship-2021-2022/",
    "2022-2023": "https://www.worldfootball.net/assists/eng-championship-2022-2023/",
    "2023-2024": "https://www.worldfootball.net/assists/eng-championship-2023-2024/",
}


# Fetch and save goal data
get_all_season_data(seasons=GOAL_URLS, metric="goals", sleep_time=0.5)
get_all_season_data(seasons=ASSIST_URLS, metric="assists", sleep_time=0.5)
