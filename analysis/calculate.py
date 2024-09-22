import statistics
from typing import List, Tuple, Union, Dict
from analysis import last10
import utils
from odds import Odds

def calculate_statistics(soup, info: List[str], standings: List[float], odds_data, odds_data_ht) -> Union[Tuple, bool]:
    try:
        
        home_data = last10.last_10_data(soup, info[1], "table_v1")
        away_data = last10.last_10_data(soup, info[2], "table_v2")

        
        bet365_percentages = convert_odds_to_percentages(odds_data)
        bet365_percentages_ht = convert_odds_to_percentages_ht(odds_data_ht)

        
        valid_data_sets = []
        valid_data_sets_ht = []
        
        if standings and all(isinstance(x, (int, float)) for x in standings):
            valid_data_sets.append(('standings', standings[:3]))

        
        if home_data and away_data:
            last10_percentages = calculate_last10_percentages(home_data, away_data)
            last10_percentages_ht = calculate_last10_percentages_ht(home_data, away_data)
            valid_data_sets.append(('last10', last10_percentages))
            valid_data_sets_ht.append(('last10', last10_percentages_ht))

        
        if bet365_percentages:
            valid_data_sets.append(('bet365', bet365_percentages))

        if bet365_percentages_ht:
            valid_data_sets_ht.append(('bet365', bet365_percentages_ht))

        
        if not valid_data_sets or not valid_data_sets_ht:
            raise ValueError("No valid data sets available for calculation")
        
        home_final, draw_final, away_final = calculate_final_percentages(valid_data_sets)
        home_final_ht, draw_final_ht, away_final_ht = calculate_final_percentages(valid_data_sets_ht)

        
        home_final_goal, away_final_goal = calculate_final_goals(standings, home_data, away_data)
        home_final_goal_ht, away_final_goal_ht = calculate_final_goals_ht(home_data, away_data)

        
        poisson_home = utils.poisson(home_final_goal)
        poisson_away = utils.poisson(away_final_goal)
        poisson_total = utils.poisson(home_final_goal + away_final_goal)

        
        poisson_home_ht = utils.poisson(home_final_goal_ht)
        poisson_away_ht = utils.poisson(away_final_goal_ht)
        poisson_total_ht = utils.poisson(home_final_goal_ht + away_final_goal_ht)

        
        over_percentages = utils.calculate_over_percent(poisson_home, poisson_away)
        over_percentages_ht = utils.calculate_over_percent(poisson_home_ht, poisson_away_ht)


        return (home_final, draw_final, away_final, poisson_home, poisson_away, 
                poisson_total, home_final_goal, away_final_goal, over_percentages,
                home_final_ht, draw_final_ht, away_final_ht, poisson_home_ht, poisson_away_ht, 
                poisson_total_ht, home_final_goal_ht, away_final_goal_ht, over_percentages_ht)
    
    except Exception as e:
        print(f"Error in calculate_statistics: {str(e)}")
        return False

def convert_odds_to_percentages(odds_data: Dict) -> List[float]:
    """Convert Bet365 odds to percentages."""
    try:
        print("\n--- Starting convert_odds_to_percentages ---")
        bet365_odds = Odds(odds_data, 1)  # Assuming Bet365 is at index 1
        ms1, msx, ms2 = bet365_odds.euro_live["u"],bet365_odds.euro_live["g"],bet365_odds.euro_live["d"],
        ms1 = float(ms1)
        msx = float(msx)
        ms2 = float(ms2)

        
        if ms1 is None or msx is None or ms2 is None or ms1 <= 0 or msx <= 0 or ms2 <= 0:
            print("Invalid odds values")
            return []
        
        total = (1/ms1) + (1/msx) + (1/ms2)
        home_percent = (1/ms1) / total
        draw_percent = (1/msx) / total
        away_percent = (1/ms2) / total
        
        result = [home_percent, draw_percent, away_percent]

        return result
    except Exception as e:

        return []

def convert_odds_to_percentages_ht(odds_data_ht: Dict) -> List[float]:
    """Convert Bet365 HT odds to percentages."""
    try:

        bet365_odds = Odds(odds_data_ht, 1)  # Assuming Bet365 is at index 1
        ms1, msx, ms2 = bet365_odds.get_first_match_odds()  # Using first odds for HT
        ms1 = float(ms1)
        msx = float(msx)
        ms2 = float(ms2)

        
        if ms1 is None or msx is None or ms2 is None or ms1 <= 0 or msx <= 0 or ms2 <= 0:
            print("Invalid HT odds values")
            return []
        
        total = (1/ms1) + (1/msx) + (1/ms2)
        home_percent = (1/ms1) / total
        draw_percent = (1/msx) / total
        away_percent = (1/ms2) / total
        
        result = [home_percent, draw_percent, away_percent]

        return result
    except Exception as e:

        return []

def calculate_last10_percentages(home_data: List[int], away_data: List[int]) -> List[float]:
    """Calculate percentages from last 10 matches data."""

    home_win_percent = (home_data[0] + away_data[2]) / 20
    draw_percent = (home_data[1] + away_data[1]) / 20
    away_win_percent = (home_data[2] + away_data[0]) / 20
    result = [home_win_percent, draw_percent, away_win_percent]

    return result

def calculate_last10_percentages_ht(home_data: List[int], away_data: List[int]) -> List[float]:
    """Calculate HT percentages from last 10 matches data."""

    home_win_percent = (home_data[3] + away_data[5]) / 20
    draw_percent = (home_data[4] + away_data[4]) / 20
    away_win_percent = (home_data[5] + away_data[3]) / 20
    result = [home_win_percent, draw_percent, away_win_percent]

    return result

def calculate_final_percentages(valid_data_sets: List[Tuple[str, List[float]]]) -> Tuple[float, float, float]:
    """Calculate final percentages using all valid data sets."""

    home_percentages = []
    draw_percentages = []
    away_percentages = []
    
    for source, percentages in valid_data_sets:

        home_percentages.append(percentages[0])
        draw_percentages.append(percentages[1])
        away_percentages.append(percentages[2])
    
    home_final = statistics.mean(home_percentages)
    draw_final = statistics.mean(draw_percentages)
    away_final = statistics.mean(away_percentages)
    
 
    # Normalize to ensure sum is 1
    total = home_final + draw_final + away_final
    result = (home_final/total, draw_final/total, away_final/total)

    return result

def calculate_final_goals(standings: List[float], home_data: List[int], away_data: List[int]) -> Tuple[float, float]:
    """Calculate final goal expectations using available data."""

    goals = []
    if standings and len(standings) >= 5:
        goals.append((standings[3], standings[4]))

    
    if home_data and away_data:
        home_goal_last10 = statistics.mean([home_data[6], away_data[7]]) * 0.1
        away_goal_last10 = statistics.mean([home_data[7], away_data[6]]) * 0.1
        goals.append((home_goal_last10, away_goal_last10))

    
    if not goals:

        return 1.5, 1.5  # Default values if no data available
    
    home_final_goal = statistics.mean([g[0] for g in goals])
    away_final_goal = statistics.mean([g[1] for g in goals])

    return home_final_goal, away_final_goal

def calculate_final_goals_ht(home_data: List[int], away_data: List[int]) -> Tuple[float, float]:

    if not home_data or not away_data:

        return 0.38, 0.38  # Default values if no data available
    
    home_goal_last10_ht = statistics.mean([home_data[8], away_data[9]]) * 0.1
    away_goal_last10_ht = statistics.mean([home_data[9], away_data[8]]) * 0.1

    return home_goal_last10_ht, away_goal_last10_ht