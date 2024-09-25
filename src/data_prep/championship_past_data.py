import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


def fetch_html(url):
    """
    Fetches the HTML content from the given URL.

    Parameters
    ----------
    url : str
        The URL of the webpage to fetch.

    Returns
    -------
    str
        The HTML content of the webpage. Returns None if the request fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def parse_table(html, headers, columns_to_clean=None):
    """
    General function to parse HTML table content and return it as a DataFrame.

    Parameters
    ----------
    html : str
        The HTML content of the webpage.
    headers : list
        List of column headers for the table.
    columns_to_clean : dict, optional
        Dictionary where the key is the column name and the value is a function to clean the column (default is None).

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the table data. Returns an empty DataFrame if no table is found.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "standard_tabelle"})

    if not table:
        print("Table not found on the page.")
        return pd.DataFrame()

    # Extract table rows
    rows = table.find_all("tr")[1:]  # Skip the header row

    # Prepare data for the DataFrame
    data = []
    for row in rows:
        columns = row.find_all("td")
        processed_columns = [col.text.strip().split("\n")[-1] for col in columns]
        data.append(processed_columns)

    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Clean specific columns if needed
    if columns_to_clean:
        for col, cleaning_function in columns_to_clean.items():
            if col in df.columns:
                df[col] = df[col].apply(cleaning_function)

    return df


def clean_goals_column(goal_str):
    """
    Cleans the 'Goals' column by extracting the number of goals, ignoring penalty information.

    Parameters
    ----------
    goal_str : str
        The raw goals data in the format 'X (Y penalties)'.

    Returns
    -------
    str
        The cleaned goal number.
    """
    return goal_str.split(" ")[0]


def parse_goals_table(html):
    """
    Parses the HTML content and extracts the goals table data.

    Parameters
    ----------
    html : str
        The HTML content of the webpage.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the goal data.
    """
    headers = ["#", "Player", "", "Country", "Team", "Goals"]
    columns_to_clean = {"Goals": clean_goals_column}
    return parse_table(html=html, headers=headers, columns_to_clean=columns_to_clean)


def parse_assists_table(html):
    """
    Parses the HTML content and extracts the assists table data.

    Parameters
    ----------
    html : str
        The HTML content of the webpage.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the assist data.
    """
    headers = ["#", "Player", "", "Country", "Team", "Assists"]
    return parse_table(html=html, headers=headers)


def get_season_data(url, season, metric, sleep_time=0.5):
    """
    Gets data (goals or assists) for a specific season from the given URL.

    Parameters
    ----------
    url : str
        The URL of the webpage to get data from.
    season : str
        The season for which to get the data.
    metric : str
        Either 'goals' or 'assists' to determine which table to parse.
    sleep_time : float, optional
        Time to sleep between requests to avoid overloading the server (default is 0.5 seconds).

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the data for the given season. Returns an empty DataFrame if getting data fails.
    """
    html = fetch_html(url=url)
    if html is None:
        return pd.DataFrame()

    if metric == "goals":
        df = parse_goals_table(html=html)
    elif metric == "assists":
        df = parse_assists_table(html=html)

    # Add season column
    if not df.empty:
        df["Season"] = season

    # Drop unnecessary columns
    df = df.drop(columns=["#", ""], errors="ignore")

    # Sleep to avoid overloading the server
    time.sleep(sleep_time)

    return df


def get_all_season_data(seasons, metric, sleep_time=0.5):
    """
    Gets data (goals or assists) for multiple seasons and writes them as individual CSVs.

    Parameters
    ----------
    seasons : dict
        A dictionary where keys are season strings and values are URLs to get data from for those seasons.
    metric : str
        Either 'goals' or 'assists' to determine which data to get.
    sleep_time : float, optional
        Time to sleep between requests to avoid overloading the server (default is 0.5 seconds).
    """
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)

    for season, url in seasons.items():
        print(f"Getting {metric} data for season {season}...")

        # Fetch data for the current season
        season_data = get_season_data(
            url=url, season=season, metric=metric, sleep_time=sleep_time
        )

        if not season_data.empty:
            # Define file path
            file_path = f"data/championship_{metric}/{season}.csv"

            # Save each season's data to a separate CSV file
            season_data.to_csv(file_path, index=False)
            print(f"Data for season {season} saved to {file_path}.")
        else:
            print(f"No data available for season {season}.")
