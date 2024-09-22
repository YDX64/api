import pandas as pd
from typing import List, Tuple, Union
from io import StringIO
from utils import metni_ayir

def last_10_data(soup, takim: str, table_id: str) -> Union[List[int], bool]:
    """
    Extract the last 10 match data for a given team.

    Args:
        soup (BeautifulSoup): The parsed HTML content.
        takim (str): The name of the team.
        table_id (str): The ID of the table containing match data.

    Returns:
        List[int]: A list containing statistics of the last 10 matches.
        bool: False if an error occurs during data extraction.
    """
    try:
        table = soup.find("table", id=table_id)
        if not table:
            print(f"Table with id '{table_id}' not found")
            return False

        df = pd.read_html(StringIO(str(table)))[0]
        if df.empty:
            print("DataFrame is empty")
            return False

        second_column = df.iloc[3:13, 2]
        if second_column.empty:
            print("No data found in the second column")
            return False

        match_data = [process_match_score(df.iloc[index, 3], value, takim) for index, value in second_column.items()]
        
        json_home_goal, json_away_goal, json_home_goal_ht, json_away_goal_ht = zip(*match_data)
        
        W, D, L = sum(h > a for h, a, _, _ in match_data), sum(h == a for h, a, _, _ in match_data), sum(h < a for h, a, _, _ in match_data)
        
        win = df.iloc[3:13, 9].str.count("W").sum()
        draw = df.iloc[3:13, 9].str.count("D").sum()
        loss = df.iloc[3:13, 9].str.count("L").sum()

        total_goal_home = sum(json_home_goal)
        total_goal_away = sum(json_away_goal)
        total_goal_home_ht = sum(json_home_goal_ht)
        total_goal_away_ht = sum(json_away_goal_ht)

        return [win, draw, loss, W, D, L, total_goal_home, total_goal_away, total_goal_home_ht, total_goal_away_ht]

    except Exception as e:
        print(f"Error in last_10_data: {str(e)}")
        return False

def process_match_score(score_data: str, value: str, takim: str) -> Tuple[int, int, int, int]:
    """
    Process match scores based on team name.

    Args:
        score_data (str): The score data from the table.
        value (str): The team name from the table row.
        takim (str): The name of the team being analyzed.

    Returns:
        Tuple[int, int, int, int]: Processed home score, away score, home half-time score, away half-time score.
    """
    try:
        if pd.isna(score_data) or pd.isna(value):
            return 0, 0, 0, 0

        scores = metni_ayir(score_data)
        if not scores or len(scores) < 4:
            return 0, 0, 0, 0

        if value == takim:
            return scores[0], scores[1], scores[2], scores[3]
        else:
            return scores[1], scores[0], scores[3], scores[2]
    except Exception as e:
        print(f"Error processing match score: {e}")
        return 0, 0, 0, 0