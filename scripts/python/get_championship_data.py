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


# Function to fetch and save data for a given metric (goals/assists)
def fetch_and_save_season_data(season_urls, metric, output_file, sleep_time=0.5):
    """
    Fetches season data for the specified metric (goals or assists) and saves it to a CSV file.

    Parameters
    ----------
    season_urls : dict
        A dictionary where keys are seasons and values are URLs.
    metric : str
        The type of data to fetch ('goals' or 'assists').
    output_file : str
        The path where the CSV file should be saved.
    sleep_time : float, optional
        Time to sleep between requests to avoid overloading the server.
    """
    # Fetch data for all seasons
    season_data = get_all_season_data(
        seasons=season_urls, metric=metric, sleep_time=sleep_time
    )

    # Save the data to a CSV file
    season_data.to_csv(output_file, index=False)
    print(f"{metric.capitalize()} data saved to {output_file}")


# Fetch and save goal data
fetch_and_save_season_data(
    season_urls=GOAL_URLS,
    metric="goals",
    output_file="data/championship_history_goals.csv",
)

# Fetch and save assist data
fetch_and_save_season_data(
    season_urls=ASSIST_URLS,
    metric="assists",
    output_file="data/championship_history_assists.csv",
)
