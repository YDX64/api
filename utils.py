import pandas as pd
import math
from datetime import datetime, timedelta

def calculate_win_percent(a, b):
    if b != 0:
        win_percent = a / b
    else:
        win_percent = 0

    return win_percent

def metni_ayir(metin):
    if isinstance(metin, float):
        return [metin]
    
    temiz_metin = metin.replace("(", "-").replace(")", "")  # Parantezleri kaldırma
    elemanlar = temiz_metin.split("-")  # "-" karakterine göre metni bölelim
    sonuc = []
    for eleman in elemanlar:
        if eleman.isdigit():  # Eleman bir sayı mı kontrol edelim
            sonuc.append(int(eleman))
    return sonuc
def zero(value):
    if value is None or pd.isnull(value):
        return 0
    return  int(value)

def poisson(ortalama_gol):
    gol_araligi = [0, 9]
    gol_ihtimalleri = []
    for k in range(gol_araligi[0], gol_araligi[1]+1):
        result = (math.exp(-ortalama_gol) * (ortalama_gol ** k)) / math.factorial(k)
        gol_ihtimalleri.append(result)
    return gol_ihtimalleri

def calculate_over_percent(poisson_home, poisson_away):
    under_15_percent = under_25_percent = under_35_percent = 0
    for i in range(len(poisson_home)-3):
        for j in range(len(poisson_away)):
            if i+j < 2:
                under_15_percent += poisson_home[i] * poisson_away[j]
                over_15_percent = 1 - under_15_percent
            if i+j < 3:
              under_25_percent += poisson_home[i] * poisson_away[j]
              over_25_percent = 1 - under_25_percent
            if i+j < 4:
              under_35_percent += poisson_home[i] * poisson_away[j]
              over_35_percent = 1 - under_35_percent

    yuzdeler = [over_15_percent,over_25_percent,over_35_percent]
    return yuzdeler        

def get_html_content(response):
    if response.status_code == 200:
        return response.text
    else:
        print("İstek gönderilirken bir hata oluştu. Hata kodu:", response.status_code)
        return None
    

def clear_time(girdi):
    try:
        tarih_ve_saat = datetime.strptime(girdi, '%m/%d/%Y %I:%M:%S %p') + timedelta(hours=3)
        tarih = tarih_ve_saat.strftime('%d/%m/%Y')
        saat = tarih_ve_saat.strftime('%H:%M')
        return tarih, saat
    except ValueError:
        return "Geçersiz tarih/saat formatı"
     
