import json
from bs4 import BeautifulSoup
import api.get_data as get_data
import analysis.calculate as calculate
import analysis.predictions as predictions
from odds import Odds 
from api.get_list import fetch_soccer_data
from datetime import datetime
import info
import analysis.standings as standings

async def toplu_analiz():
    all_match_data = []
    bugun = datetime.now()
    tarih = bugun.strftime("%Y-%m-%d")
    path = f"/ajax/SoccerAjax?type=6&date={tarih}&order=time&timezone=3&flesh=0.12689888719604503"
    try:
        match_id_list = await fetch_soccer_data(path)
    except Exception as e:
        print(f"Maç verileri çekilirken hata oluştu: {e}")
        return [], tarih

    for i in range(1, len(match_id_list)-i):
        print("Kalan maç: " + str(len(match_id_list)-i))    
        try:
            match_id = match_id_list[i]
            print(match_id)
            match_data = await process_match(match_id)
            if match_data is False:
                print(f"Maç verisi işlenemedi (ID: {match_id})")
                continue
            all_match_data.append(match_data)       
        except ValueError as ve:
            print(f"Veri format hatası (ID: {match_id}): {ve}")
        except TypeError as te:
            print(f"Tip hatası (ID: {match_id}): {te}")
        except Exception as e:
            print(f"Genel hata (ID: {match_id}): {e}")

    try:
        merged_data = json.dumps(all_match_data)
        sonveri = json.loads(merged_data)
    except json.JSONDecodeError as je:
        print(f"JSON dönüştürme hatası: {je}")
        sonveri = []

    return sonveri, tarih

async def get_match_info(match_id):
    html_content, html_content_odds, html_content_ht_odds, html_content_double_chance_odds, html_content_corner_odds, html_content_score_odds = await get_data.get_match_data(match_id)
    soup = BeautifulSoup(html_content, "html.parser")
    odds_data = json.loads(html_content_odds)
    odds_data_ht = json.loads(html_content_ht_odds)
    odds_data_double = json.loads(html_content_double_chance_odds)
    odds_data_corner = json.loads(html_content_corner_odds)
    odds_data_score = json.loads(html_content_score_odds)

    return soup, odds_data, odds_data_ht, odds_data_double, odds_data_corner, odds_data_score
def get_default_standings():
    """
    Standings verisi olmadığında kullanılacak varsayılan değerleri döndürür.
    """
    return [0.33, 0.34, 0.33, 1.5, 1.5]

async def process_match(match_id):
    soup, odds_data, odds_data_ht, odds_data_double, odds_data_corner, odds_data_score = await get_match_info(match_id)
    infor = info.information(soup)
    lig, evsahibi, deplasman, tarih, saat, home_score, away_score, ht_score = infor

    try:
        standing = standings.get_standings_data(soup)
    except Exception as e:
        print(f"Standings verisi alınamadı: {e}")
        standing = get_default_standings()
    

    
    hesaplar = calculate.calculate_statistics(soup, infor, standing, odds_data,odds_data_ht)
    if hesaplar is False:
        return False
    
    (home_final, draw_final, away_final, poisson_home, poisson_away, poisson_total, 
     home_final_goal, away_final_goal, a, 
     home_final_ht, draw_final_ht, away_final_ht, poisson_home_ht, poisson_away_ht, 
     poisson_total_ht, home_final_goal_ht, away_final_goal_ht, a_ht) = hesaplar
    
    over_15_percent, over_25_percent, over_35_percent = a
    over_05_percent_ht, over_15_percent_ht, over_25_percent_ht = a_ht
    
    tahminler = predictions.Tahminler(hesaplar, odds_data, odds_data_ht)
    print(f"{evsahibi} - {deplasman} maçı analiz ediliyor")
    
    match_info = {
        "info": {
            "id": match_id,
            "mac_tarihi": tarih,
            "mac_saati": saat,
            "lig": lig,
            "mac": f"{evsahibi} - {deplasman}"
        },
        "tahminler": {
            "ust_tahmini": tahminler.ust_tahmini(),
            "kg_tahmini": tahminler.kg_var_tahmini(),
            "ms_tahmini": tahminler.ms_tahmini(),
            "iy_gol_tahmini": tahminler.iy_gol_tahmini(),
        },
        "home_away_goal": {
            "home_goal": home_final_goal,
            "away_goal": away_final_goal,
            "home_goal_ht": home_final_goal_ht,
            "away_goal_ht": away_final_goal_ht
        },
        "yuzdeler": {
            "ev_gol_yuzdesi": "{:.0%}".format(sum(poisson_home) - poisson_home[0]),
            "dep_gol_yuzdesi": "{:.0%}".format(sum(poisson_away) - poisson_away[0]),
            "ust_yuzdesi_1": "{:.0%}".format(over_15_percent),
            "ust_yuzdesi2": "{:.0%}".format(over_25_percent),
            "ust_yuzdesi3": "{:.0%}".format(over_35_percent),
            "ms_yuzdeleri": f"{home_final:.0%} - {draw_final:.0%} - {away_final:.0%}",
            "ev_gol_yuzdesi_ht": "{:.0%}".format(sum(poisson_home_ht) - poisson_home_ht[0]),
            "dep_gol_yuzdesi_ht": "{:.0%}".format(sum(poisson_away_ht) - poisson_away_ht[0]),
            "ust_yuzdesi_05_ht": "{:.0%}".format(over_05_percent_ht),
            "ust_yuzdesi_15_ht": "{:.0%}".format(over_15_percent_ht),
            "ust_yuzdesi_25_ht": "{:.0%}".format(over_25_percent_ht),
            "iy_yuzdeleri_": f"{home_final_ht:.0%} - {draw_final_ht:.0%} - {away_final_ht:.0%}",
        },
    }
    
    poission = {
        "poisson": {
            "poisson_total": {str(i): poisson_total[i] for i in range(6)},
            "poisson_home": {str(i): poisson_home[i] for i in range(6)},
            "poisson_away": {str(i): poisson_away[i] for i in range(6)},
            "poisson_total_ht": {str(i): poisson_total_ht[i] for i in range(6)},
            "poisson_home_ht": {str(i): poisson_home_ht[i] for i in range(6)},
            "poisson_away_ht": {str(i): poisson_away_ht[i] for i in range(6)},
        },
    }
    
    match_info["poisson"] = poission
    match_info["bahis_oranlari"] = get_odds(odds_data, odds_data_ht)
    match_info["korner_oranlari"] = odds_data_corner
    match_info["cifte_sans_oranlari"] = odds_data_double
    match_info["skor_oranlari"] = odds_data_score
    match_info["score"] = {"home_score": home_score, "away_score": away_score, "ht_score": ht_score}

    return json.loads(json.dumps(match_info))



def get_odds(odds_data, odds_data_ht):
    bahis_siteleri = ["Sbobet", "Bet365", "M88", "188Bet", "Crown", "12Bet", "18Bet", "Macauslot", "Ladbrokes", "EasyBet"]
    return {
        site: {
            "acilis": {
                "acilis_ms1": Odds(odds_data, i).euro_first["u"],
                "acilis_msx": Odds(odds_data, i).euro_first["g"],
                "acilis_ms2": Odds(odds_data, i).euro_first["d"],
                "acilis_iy1": Odds(odds_data_ht, i).euro_first["u"],
                "acilis_iyx": Odds(odds_data_ht, i).euro_first["g"],
                "acilis_iy2": Odds(odds_data_ht, i).euro_first["d"],
                "acilis_oran": Odds(odds_data, i).ou_first['u'],
                "acilis_goalline": Odds(odds_data, i).ou_first['g'],  
                "acilis_taraf": Odds(odds_data, i).ah_first['g'],
                "acilis_oran_ht": Odds(odds_data_ht, i).ou_first['u'],
                "acilis_taraf_ht": Odds(odds_data_ht, i).ah_first['g'],  
                "acilis_goalline_ht": Odds(odds_data_ht, i).ou_first['g'],     
            },
            "kapanis": {
                "kapanis_ms1": Odds(odds_data, i).euro_live["u"],
                "kapanis_msx": Odds(odds_data, i).euro_live["g"],
                "kapanis_ms2": Odds(odds_data, i).euro_live["d"],
                "kapanis_iy1": Odds(odds_data_ht, i).euro_live["u"],
                "kapanis_iyx": Odds(odds_data_ht, i).euro_live["g"],
                "kapanis_iy2": Odds(odds_data_ht, i).euro_live["d"],           
                "kapanis_oran": Odds(odds_data, i).ou_live['u'],         
                "kapanis_goalline": Odds(odds_data, i).ou_live['g'],
                "kapanis_taraf": Odds(odds_data, i).ah_live['g'],
                "kapanis_oran_ht": Odds(odds_data_ht, i).ou_live['u'],
                "kapanis_goalline_ht": Odds(odds_data_ht, i).ou_live['g'],
                "kapanis_taraf_ht": Odds(odds_data_ht, i).ah_live['g'],
            }
        } for i, site in enumerate(bahis_siteleri)
    }