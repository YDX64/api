import json
import requests
from config import Config
from api.delete import delete_data_from_firebase

def veriyi_post_et(sonveri, tarih):
    """
    Veriyi belirli bir tarihle Firebase'e post eden fonksiyon.

    Parameters:
    sonveri (dict): Gönderilecek veri.
    tarih (str): Verinin gönderileceği tarih.

    Returns:
    bool: İşlemin başarılı olup olmadığını belirtir.
    """
    try:
        post_url = create_post_url(tarih)
        
        # Önceki veriyi sil
        delete_data_from_firebase(post_url)
        
        # Yeni veriyi post et
        veri_json = json.dumps(sonveri, indent=2)
        response = requests.post(post_url, data=veri_json)
        response.raise_for_status()  # Hata durumunda HTTPError raise eder

        print(f"Veri başarıyla post edildi: {response.status_code}")
        return True
    
    except requests.exceptions.RequestException as err:
        print(f'Hata oluştu: {err}')
        return False

def create_post_url(tarih):
    """
    Verilen tarih ile Firebase post URL'si oluşturur.

    Parameters:
    tarih (str): URL'de kullanılacak tarih.

    Returns:
    str: Oluşturulan URL.
    """
    base_url = Config.POST_URL
    return f'{base_url}{tarih}.json'
