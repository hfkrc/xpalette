import requests
from bs4 import BeautifulSoup

# Ana sayfanın URL'si
base_url = "https://artvee.com"
collection_url = "https://artvee.com/s_collection/1084652/"

# Sayfanın HTML içeriğini al
response = requests.get(collection_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Tüm resim detay sayfalarının bağlantılarını bul
detail_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if '/dl/' in href:  # Sadece detay sayfalarının bağlantılarını al
        full_link = href
        detail_links.append(full_link)

# Bağlantıları bir metin dosyasına kaydet
with open('detail_links.txt', 'w') as file:
    for link in detail_links:
        file.write(link + '\n')

print(f"{len(detail_links)} detay sayfası bağlantısı kaydedildi.")