from odds import Odds

class Tahminler:
    def __init__(self, hesaplar, odds_data,odds_data_ht):
        self.hesaplar = hesaplar
        self.odds_data = odds_data
        self.odds_data_ht = odds_data_ht
        self.acilis_oran_bet365 = Odds(odds_data, 1).ou_first["u"]
        self.kapanis_oran_bet365 = Odds(odds_data, 1).ou_live["u"]
        self.acilis_goalline_bet365 = Odds(odds_data, 1).ou_first["g"]
        self.kapanis_goalline_bet365 = Odds(odds_data, 1).ou_live["g"]
        self.kapanis_taraf_bet365 = Odds(odds_data, 1).ah_live["g"]
        self.acilis_taraf_bet365 = Odds(odds_data, 1).ah_first["g"]
        self.acilis_oran_bet365_ht = Odds(odds_data_ht, 1).ou_first["u"]
        self.kapanis_oran_bet365_ht = Odds(odds_data_ht, 1).ou_live["u"]
        self.acilis_goalline_bet365_ht = Odds(odds_data_ht, 1).ou_first["g"]
        self.kapanis_goalline_bet365_ht = Odds(odds_data_ht, 1).ou_live["g"]
        self.kapanis_taraf_bet365_ht = Odds(odds_data_ht, 1).ah_live["g"]
        self.acilis_taraf_bet365_ht = Odds(odds_data_ht, 1).ah_first["g"]
        
    def iy_gol_tahmini(self):
        try:
            goalline_bet365_kapanis_ht = float(self.kapanis_goalline_bet365_ht)
            goalline_bet365_acilis_ht = float(self.acilis_goalline_bet365_ht)
        except ValueError:
            return ""  # Değerleri dönüştürme hatası aldığınızda boş bir string döndürün

        if goalline_bet365_acilis_ht < goalline_bet365_kapanis_ht:
            return "İy 0.5 Üst"
        else:
            return ""

    def ust_tahmini(self):
        sayi = 0
        a = self.hesaplar[8]
        over_percent = float(a[1])

        for i in range(0,10):
            acilis = Odds(self.odds_data, i).ou_first["g"],
            kapanis = Odds(self.odds_data, i).ou_live["g"],
            if kapanis > acilis:
                sayi = sayi+1
    
        try:
            goalline_bet365_kapanis = float(self.kapanis_goalline_bet365)
            goalline_bet365_acilis = float(self.acilis_goalline_bet365)
            goalline_bet365_kapanis_ht = float(self.kapanis_goalline_bet365_ht)
            goalline_bet365_acilis_ht = float(self.acilis_goalline_bet365_ht)
        except ValueError:
            return ""  # Değerleri dönüştürme hatası aldığınızda boş bir string döndürün
        
        if goalline_bet365_kapanis > goalline_bet365_acilis and goalline_bet365_acilis_ht < goalline_bet365_kapanis_ht:
            return "2.5 Üst" #sadecebet365 e bakmak sağlıklı sonuçlar vermiyor
        elif sayi> 4 and goalline_bet365_kapanis>2.50:
            return "2.5 Üst"        
        elif over_percent < 0.4 and goalline_bet365_kapanis < goalline_bet365_acilis and goalline_bet365_kapanis < 2.5:
            return "2.5 Alt"
        elif goalline_bet365_kapanis > goalline_bet365_acilis + 0.25:
            return "2.5 Üst"    
        elif over_percent > 0.7 and goalline_bet365_kapanis > 2.50:
            return "2.5 Üst"
        elif goalline_bet365_kapanis > goalline_bet365_acilis and goalline_bet365_kapanis > 2.5 and over_percent > 0.6:
            return "2.5 Üst"
        elif goalline_bet365_kapanis > 3.75:
            return "2.5 Üst"
        else:
            return ""

    def kg_var_tahmini(self):
        poisson_home = self.hesaplar[3]
        poisson_away = self.hesaplar[4]
        try:
            poisson_home = float(1.0 - poisson_home[0])
            poisson_away = float(1.0 - poisson_away[0])
            kapanis_goalline_bet365 = float(self.kapanis_goalline_bet365)
            kapanis_taraf_bet365 = float(self.kapanis_taraf_bet365)
        except ValueError:
            return ""  # Değerleri dönüştürme hatası aldığınızda boş bir string döndürün

        if poisson_home > 0.8 and poisson_away > 0.8:
            return "Kg Var"
        elif kapanis_goalline_bet365 > 3.25 and abs(kapanis_taraf_bet365) < 0.5:
            return "Kg Var"
        else:
            return ""
 
    def ms_tahmini(self):
        sayi = 0
        ms2kademe = 0
        for i in range(0,10):           
            try:
                acilis = float(Odds(self.odds_data, i).ah_first["g"]),
                kapanis = float(Odds(self.odds_data, i).ah_live["g"]),
                
                if kapanis > acilis:
                    sayi = sayi + 1
                elif kapanis < acilis :
                    ms2kademe = ms2kademe+1    
            except:
                ""#print("hata"),
        if sayi>4:
            return "Ms1"
        
        if ms2kademe>4:
            return "Ms2"       
        else:
            return ""
        