import requests
url = "https://python-project-c31eb-default-rtdb.firebaseio.com/yeni/-NjUPzFo6-WeErb952hZ.json"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    with open("sonveri.txt", "w", encoding="utf-8") as file:
        for item in data:
            info = item.get('info', {})
            tahminler = item.get('tahminler', {})
            mac = info.get('mac', 'Bilgi yok')
            lig = info.get('lig', 'Bilgi yok')
            mac_saati = info.get('mac_saati', 'Bilgi yok')
            ust_tahmini= tahminler.get('ust_tahmini','Bilgi yok')
            if ust_tahmini =="2.5 Üst":
                file.write(f"\nMaç: {mac} \nLig: {lig} \nMaç Saati: {mac_saati} \nÜst Tahmini: {ust_tahmini}\n")
else:
    print("Veri çekilemedi. Hata kodu:", response.status_code)
