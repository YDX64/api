import utils

def information(soup):
    """
    Verilen BeautifulSoup objesi üzerinden futbol maçına ait bilgileri çıkarır.
    
    Args:
        soup (BeautifulSoup): Ayrıştırılmış HTML içeriği.

    Returns:
        list: Maç bilgilerini içeren liste. Listede lig adı, ev sahibi ve deplasman takım adları,
              tarih, saat, ev sahibi ve deplasman takım skorları, ilk yarı skoru bulunur.
    """
    info = []

    try:
        league = soup.find(class_="LName").text.strip()
    except AttributeError:
        league = "Bilinmiyor"

    try:
        time_element = soup.find('span', class_='time')
        time_data = time_element['data-t']
        tarih, saat = utils.clear_time(time_data)
    except (AttributeError, TypeError):
        tarih, saat = "Bilinmiyor", "Bilinmiyor"

    try:
        class_elements = soup.find_all(class_="sclassName")
        home_team_name = class_elements[0].text.strip()
        away_team_name = class_elements[1].text.strip()
    except (AttributeError, IndexError):
        home_team_name, away_team_name = "Bilinmiyor", "Bilinmiyor"

    try:
        class_elements2 = soup.find_all(class_="score")
        home_score = class_elements2[0].text.strip() if len(class_elements2) > 0 else ""
        away_score = class_elements2[1].text.strip() if len(class_elements2) > 1 else ""
    except AttributeError:
        home_score, away_score = "Bilinmiyor", "Bilinmiyor"

    try:
        span_with_title = soup.find('span', {'title': 'Score 1st Half'})
        iy_score = span_with_title.text if span_with_title else ""
    except AttributeError:
        iy_score = "Bilinmiyor"

    info.extend([league, home_team_name, away_team_name, tarih, saat, home_score, away_score, iy_score])

    return info
