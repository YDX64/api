import pandas as pd
from io import StringIO
from typing import List, Union, Dict
import logging

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_standings_data(soup) -> Union[List[float], None]:
    """
    Verilen BeautifulSoup nesnesinden takım istatistiklerini çıkarır.

    Args:
        soup: BeautifulSoup nesnesi

    Returns:
        List[float]: İstatistik yüzdeleri listesi veya None (hata durumunda)
    """
    try:
        standing_home = soup.find("table", class_="team-table-home")
        standing_away = soup.find("table", class_="team-table-guest")
        
        if not standing_home or not standing_away:
            logger.warning("Standings tabloları bulunamadı")
            return None

        home_data = extract_table_data(standing_home)
        away_data = extract_table_data(standing_away)

        if not home_data or not away_data:
            logger.warning("Standings verileri çıkarılamadı")
            return None

        total_stats = calculate_total_stats(home_data, away_data)
        home_away_stats = calculate_home_away_stats(home_data, away_data)
        last6_stats = calculate_last6_stats(home_data, away_data)

        if not all([total_stats, home_away_stats, last6_stats]):
            logger.warning("Bir veya daha fazla istatistik hesaplanamadı")
            return None

        final_stats = calculate_final_stats(total_stats, home_away_stats, last6_stats)

        if final_stats:
            final_stats = [0.0 if pd.isna(stat) or pd.isinf(stat) else stat for stat in final_stats]

        return final_stats

        if not all(isinstance(stat, float) for stat in final_stats):
            logger.warning("Bazı final istatistikleri geçerli float değerleri değil")
            return None

        return final_stats

    except Exception as e:
        logger.error(f"Standings verisi işlenirken hata oluştu: {e}")
        return None

def extract_table_data(table) -> Union[Dict[str, List[float]], None]:
    """
    HTML tablosundan veri çıkarır.

    Args:
        table: BeautifulSoup table nesnesi

    Returns:
        Dict: Çıkarılan veriler veya None (hata durumunda)
    """
    try:
        df = pd.read_html(StringIO(str(table)))[0]
        if df.empty:
            logger.warning("Tablo boş")
            return None
        data = {
            'total': safe_convert_list(df.iloc[2, 1:7]),
            'home_away': safe_convert_list(df.iloc[3, 1:7]),
            'last6': safe_convert_list(df.iloc[5, 1:7])
        }
        if not all(data.values()):
            logger.warning("Bazı veri setleri boş")
            return None
        return data
    except Exception as e:
        logger.error(f"Tablo verisi çıkarılırken hata oluştu: {e}")
        return None

def safe_convert_list(series) -> List[float]:
    """
    Pandas serisini güvenli bir şekilde float listesine dönüştürür.

    Args:
        series: Pandas serisi

    Returns:
        List[float]: Dönüştürülmüş liste
    """
    return [safe_float(x) for x in series]

def safe_float(value) -> float:
    """
    Değeri güvenli bir şekilde float'a dönüştürür.

    Args:
        value: Dönüştürülecek değer

    Returns:
        float: Dönüştürülmüş değer veya 0.0 (hata durumunda)
    """
    try:
        float_value = float(value)
        if pd.isna(float_value) or pd.isinf(float_value):
            logger.warning(f"'{value}' geçersiz bir float değeri (nan veya inf), 0.0 kullanılıyor")
            return 0.0
        return float_value
    except (ValueError, TypeError):
        logger.warning(f"'{value}' float'a dönüştürülemedi, 0.0 kullanılıyor")
        return 0.0

def calculate_total_stats(home_data: Dict, away_data: Dict) -> Union[List[float], None]:
    """
    Toplam istatistikleri hesaplar.

    Args:
        home_data: Ev sahibi takım verileri
        away_data: Deplasman takım verileri

    Returns:
        List[float]: Hesaplanan istatistikler veya None (hata durumunda)
    """
    try:
        home_total = home_data['total']
        away_total = away_data['total']
        
        total_matches = home_total[0] + away_total[0]
        if total_matches == 0:
            logger.warning("Toplam maç sayısı sıfır")
            return None

        total_1_percent = (home_total[1] + away_total[3]) / total_matches
        total_x_percent = (home_total[2] + away_total[2]) / total_matches
        total_2_percent = (home_total[3] + away_total[1]) / total_matches
        total_home_goal = (home_total[4] + away_total[5]) / total_matches
        total_away_goal = (home_total[5] + away_total[4]) / total_matches

        return [total_1_percent, total_x_percent, total_2_percent, total_home_goal, total_away_goal]
    except Exception as e:
        logger.error(f"Toplam istatistikler hesaplanırken hata oluştu: {e}")
        return None

def calculate_home_away_stats(home_data: Dict, away_data: Dict) -> Union[List[float], None]:
    """
    Ev sahibi ve deplasman istatistiklerini hesaplar.

    Args:
        home_data: Ev sahibi takım verileri
        away_data: Deplasman takım verileri

    Returns:
        List[float]: Hesaplanan istatistikler veya None (hata durumunda)
    """
    try:
        home = home_data['home_away']
        away = away_data['home_away']
        
        total_matches = home[0] + away[0]
        if total_matches == 0:
            logger.warning("Ev sahibi ve deplasman maç sayısı toplamı sıfır")
            return None

        home_away_1_percent = (home[1] + away[3]) / total_matches
        home_away_x_percent = (home[2] + away[2]) / total_matches
        home_away_2_percent = (home[3] + away[1]) / total_matches
        ha_home_goal = (home[4] + away[5]) / total_matches
        ha_away_goal = (home[5] + away[4]) / total_matches

        return [home_away_1_percent, home_away_x_percent, home_away_2_percent, ha_home_goal, ha_away_goal]
    except Exception as e:
        logger.error(f"Ev sahibi ve deplasman istatistikleri hesaplanırken hata oluştu: {e}")
        return None

def calculate_last6_stats(home_data: Dict, away_data: Dict) -> Union[List[float], None]:
    """
    Son 6 maçın istatistiklerini hesaplar.

    Args:
        home_data: Ev sahibi takım verileri
        away_data: Deplasman takım verileri

    Returns:
        List[float]: Hesaplanan istatistikler veya None (hata durumunda)
    """
    try:
        home_last6 = home_data['last6']
        away_last6 = away_data['last6']
        
        total_matches = home_last6[0] + away_last6[0]
        if total_matches == 0:
            logger.warning("Son 6 maç için toplam maç sayısı sıfır")
            return None

        last6_1_percent = (home_last6[1] + away_last6[3]) / total_matches
        last6_x_percent = (home_last6[2] + away_last6[2]) / total_matches
        last6_2_percent = (home_last6[3] + away_last6[1]) / total_matches
        last6_home_goal = (home_last6[4] + away_last6[5]) / total_matches
        last6_away_goal = (home_last6[5] + away_last6[4]) / total_matches

        return [last6_1_percent, last6_x_percent, last6_2_percent, last6_home_goal, last6_away_goal]
    except Exception as e:
        logger.error(f"Son 6 maç istatistikleri hesaplanırken hata oluştu: {e}")
        return None

def calculate_final_stats(total_stats: List[float], home_away_stats: List[float], last6_stats: List[float]) -> List[float]:
    """
    Final istatistikleri hesaplar.

    Args:
        total_stats: Toplam istatistikler
        home_away_stats: Ev sahibi ve deplasman istatistikleri
        last6_stats: Son 6 maç istatistikleri

    Returns:
        List[float]: Hesaplanan final istatistikler
    """
    try:
        final_stats = []
        for i in range(5):
            values = [total_stats[i], home_away_stats[i], last6_stats[i]]
            valid_values = [v for v in values if not pd.isna(v) and not pd.isinf(v)]
            if valid_values:
                avg = sum(valid_values) / len(valid_values)
                final_stats.append(round(avg, 4))
            else:
                final_stats.append(0.0)
        
        return final_stats
    except Exception as e:
        logger.error(f"Final istatistikleri hesaplanırken hata oluştu: {e}")
        return [0.0, 0.0, 0.0, 0.0, 0.0]  # Hata durumunda sıfır değerlerle dolu liste döndür