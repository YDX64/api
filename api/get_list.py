import http.client
import gzip
from io import BytesIO
import re
from config import Config

async def fetch_soccer_data(path):
    try:
        conn = http.client.HTTPSConnection(Config.LIVE_MATCHES_URL)
        conn.request("GET", path)
        response = conn.getresponse()

        if response.status == 200:
            data = response.read()
            if response.getheader('Content-Encoding') == 'gzip':
                with gzip.open(BytesIO(data), 'rb') as f:
                    data = f.read()
            return extract_specific_elements(data)
        else:
            print("Error:", response.status, response.reason)
            return None
    except Exception as e:
        print(f"Error fetching soccer data: {e}")
        return None

def extract_specific_elements(data):
    try:
        if isinstance(data, bytes):
            data = data.decode('utf-8')

        # Lig bilgilerini ayrıştır
        leagues = extract_leagues(data)
        
        # Maç bilgilerini ayrıştır
        matches = re.findall(r'A\[\d+\]=\[(.*?)\];', data)
        specific_elements = [parse_element(item, leagues) for item in matches]

        return specific_elements
    except Exception as e:
        print(f"Error extracting elements: {e}")
        return []

def extract_leagues(data):
    try:
        league_data = re.findall(r'B\[(\d+)\]=\[.*?,.*?,\'(.*?)\',.*?\];', data)
        leagues = {int(league_id): league_name for league_id, league_name in league_data}
        return leagues
    except Exception as e:
        print(f"Error extracting leagues: {e}")
        return {}

def parse_element(item, leagues):
    try:
        # Verileri tuple olarak değerlendirir ve sadece gerekli elemanları alır
        element_tuple = eval(f"({item})")
        match_id = element_tuple[0]
        home_team = element_tuple[4]
        away_team = element_tuple[5]
        time = element_tuple[6]
        league_id = int(element_tuple[1])  # Lig id'si 1. eleman olarak varsayılmıştır, verilerinize göre ayarlayınız
        league_name = leagues.get(league_id, "Unknown League")
        return (match_id, home_team, away_team, league_name,time)
    except (SyntaxError, TypeError, IndexError) as e:
        print(f"Error parsing element: {e}")
        return None
