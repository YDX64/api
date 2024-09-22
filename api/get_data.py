import httpx
import random
import utils
from config import Config

async def get_match_data(match_id):
    """
    Fetch match data and odds from the given URLs using the match ID.

    Parameters:
    match_id (str): The ID of the match to fetch data for.

    Returns:
    tuple: HTML content and various odds data.
    """
    random_deger = random.uniform(0.50000534734714295, 0.90000534734714295)
    
    # URLs for different data points
    urls = {
        "html_content": f"{Config.MAIN_SITE_URL}match/h2h-{match_id}",
        "odds": f"{Config.MAIN_SITE_URL}ajax/soccerajax?type=14&t=1&id={match_id}&h=0&flesh={random_deger}",
        "ht_odds": f"{Config.MAIN_SITE_URL}ajax/soccerajax?type=14&t=1&id={match_id}&h=1&flesh={random_deger}",
        "double_chance_odds": f"{Config.MAIN_SITE_URL}ajax/soccerajax?type=14&t=7&id={match_id}&flesh={random_deger}",
        "corner_odds": f"{Config.MAIN_SITE_URL}ajax/soccerajax?type=14&t=4&id={match_id}&flesh={random_deger}",
        "score_odds": f"{Config.MAIN_SITE_URL}ajax/soccerajax?type=14&t=5&id={match_id}&flesh={random_deger}"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            responses = {}
            for key, url in urls.items():
                print(f"{key.replace('_', ' ').title()} alınıyor...")
                responses[key] = await client.get(url)
            
        # Process and return the HTML content and odds data
        return (
            utils.get_html_content(responses["html_content"]),
            utils.get_html_content(responses["odds"]),
            utils.get_html_content(responses["ht_odds"]),
            utils.get_html_content(responses["double_chance_odds"]),
            utils.get_html_content(responses["corner_odds"]),
            utils.get_html_content(responses["score_odds"])
        )
    
    except httpx.RequestError as e:
        print(f"HTTP Request failed: {e}")
        return None