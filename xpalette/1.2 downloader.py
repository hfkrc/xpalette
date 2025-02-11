import requests
from bs4 import BeautifulSoup
import os

# İndirilen resimleri kaydetmek için klasör oluştur
if not os.path.exists('downloaded_images'):
    os.makedirs('downloaded_images')

# Detay sayfasındaki resmi indiren fonksiyon
def download_image_from_detail_page(detail_url):
    # Detay sayfasını çek
    response = requests.get(detail_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # "Download" butonunu bul
    download_button = soup.find('a', {'class': 'prem-link gr btn dis snax-action snax-action-add-to-collection snax-action-add-to-collection-downloads'})
    if download_button and download_button.get('href'):
        # Resmin indirme bağlantısını al
        image_url = download_button['href']
        
        # Resmi indir
        image_name = os.path.basename(image_url).split('?')[0]  # URL'den dosya adını al
        image_path = os.path.join('downloaded_images', image_name)
        
        print(f"İndiriliyor: {image_name}")
        with open(image_path, 'wb') as file:
            file.write(requests.get(image_url).content)
        print(f"İndirildi: {image_path}")
    else:
        print(f"Download butonu bulunamadı: {detail_url}")

# Örnek detay sayfası bağlantıları
detail_links = [
    "https://artvee.com/dl/allegory-of-justice-punishing-injustice-1737#00",
    "https://artvee.com/dl/das-bad-der-diana-ruckseite-die-erziehung-des-bacchusknaben#00",
    # Diğer detay sayfası bağlantılarını buraya ekleyin
]

# Her bir detay sayfası için resmi indir
for link in detail_links:
    download_image_from_detail_page(link)

print("Tüm resimler indirildi.")