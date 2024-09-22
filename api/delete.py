import requests

def delete_data_from_firebase(url):
    """
    Delete data from Firebase using the given URL.

    Parameters:
    url (str): The URL from which data should be deleted.

    Returns:
    str: Success message or error message with status code and error text.
    """
    try:
        response = requests.delete(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        if response.status_code == 200:
            return "Veri başarıyla silindi."
        else:
            return f"Hata kodu: {response.status_code}, Hata mesajı: {response.text}"
    
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"