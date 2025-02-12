import requests
from bs4 import BeautifulSoup
import os
import random
import re
import tweepy
import time
import schedule

# Twitter API anahtarları
API_KEY = "k41suMKhX3csA1Uufp9Lbqs1p"
API_SECRET_KEY = "f2CqqKyEZkSOD7KqWLpSio9LSsArgbZ37EKswSjsG9HCKm83H6"
ACCESS_TOKEN = "1829309777228308480-SNUi5By62ZMnwBv8B8xGugDbKSn9KW"
ACCESS_TOKEN_SECRET = "lZmpp6xSISBh06a2FgoQ9qAcg3o8bTtBFcgRykumfBW66"

# İndirilen resimleri kaydetmek için klasör oluştur
if not os.path.exists('downloaded_images'):
    os.makedirs('downloaded_images')

# Twitter API'sine bağlan
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Detay sayfasındaki resmi indiren fonksiyon
def download_image_from_detail_page(detail_url):
    try:
        # Detay sayfasını çek
        response = requests.get(detail_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Resmin başlığını bul
        title_element = soup.find('a', href=re.compile(r'^https://artvee\.com/dl/'))
        if title_element:
            title = title_element.text.strip()  # Başlığı al
            title = re.sub(r'[^\w\s\-()]', '', title)  # Geçersiz karakterleri kaldır, parantezleri koru
            title = title.replace(' ', '_')  # Boşlukları alt çizgi ile değiştir
        else:
            print(f"Başlık bulunamadı: {detail_url}")
            return None
        
        # "Download" butonunu bul
        download_button = soup.find('a', {'class': 'prem-link gr btn dis snax-action snax-action-add-to-collection snax-action-add-to-collection-downloads'})
        if download_button and download_button.get('href'):
            # Resmin indirme bağlantısını al
            image_url = download_button['href']
            
            # Resmi indir
            image_name = f"{title}.jpg"  # Resmin adını başlıktan oluştur
            image_path = os.path.join('downloaded_images', image_name)
            
            print(f"İndiriliyor: {image_name}")
            with open(image_path, 'wb') as file:
                file.write(requests.get(image_url).content)
            print(f"İndirildi: {image_path}")
            return image_path, title.replace('_', ' ')  # Resim yolu ve başlık
        else:
            print(f"Download butonu bulunamadı: {detail_url}")
            return None
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

# TXT dosyasından linkleri oku
def read_links_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            links = file.read().splitlines()
        return links
    except FileNotFoundError:
        print(f"{file_path} dosyası bulunamadı. Yeni bir dosya oluşturuluyor.")
        with open(file_path, 'w') as file:
            file.write("")  # Boş bir dosya oluştur
        return []  # Boş liste döndür

# TXT dosyasına linkleri yaz (silinen link hariç)
def write_links_to_file(file_path, links):
    with open(file_path, 'w') as file:
        for link in links:
            file.write(link + '\n')

# Resmi Twitter'da paylaşan fonksiyon
def tweet_image(image_path, tweet_text):
    try:
        # Resmi Twitter'da paylaş
        media = api.media_upload(image_path)
        api.update_status(status=tweet_text, media_ids=[media.media_id])
        print(f"Tweet atıldı: {tweet_text}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

# Ana işlem
def main():
    file_path = r'C:\Users\fafli\Desktop\xpalette\xpalette\detail_links.txt'  # Mutlak yol
    
    # Linkleri dosyadan oku
    links = read_links_from_file(file_path)
    
    if not links:
        print("Dosyada link bulunamadı.")
        return
    
    # Rastgele bir link seç
    selected_link = random.choice(links)
    print(f"Seçilen link: {selected_link}")
    
    # Resmi indir
    result = download_image_from_detail_page(selected_link)
    if result:
        image_path, tweet_text = result
        # Resmi Twitter'da paylaş
        tweet_image(image_path, tweet_text)
        # İndirme başarılıysa linki listeden sil
        links.remove(selected_link)
        # Güncellenmiş listeyi dosyaya yaz
        write_links_to_file(file_path, links)
        print(f"Link dosyadan silindi: {selected_link}")
    else:
        # İndirme başarısızsa linki listeden sil
        links.remove(selected_link)
        write_links_to_file(file_path, links)
        print(f"Link dosyadan silindi (indirme başarısız): {selected_link}")

# Her 4 saatte bir çalışacak şekilde zamanlama
schedule.every(4).hours.do(main)

# Programı çalıştır
if __name__ == "__main__":
    # İlk paylaşımı hemen yap
    main()
    
    # Sonraki paylaşımlar için 4 saatte bir döngü
    while True:
        schedule.run_pending()
        time.sleep(1)