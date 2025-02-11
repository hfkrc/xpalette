import requests
from bs4 import BeautifulSoup
import os
import random
import re

# İndirilen resimleri kaydetmek için klasör oluştur
if not os.path.exists('downloaded_images'):
    os.makedirs('downloaded_images')

# Detay sayfasındaki resmi indiren fonksiyon
def download_image_from_detail_page(detail_url):
    # Detay sayfasını çek
    response = requests.get(detail_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Resmin başlığını bul
    title_element = soup.find('a', href=re.compile(r'^https://artvee\.com/dl/'))
    if title_element:
        title = title_element.text.strip()  # Başlığı al
        # Geçersiz karakterleri kaldır, parantezleri koru
        title = re.sub(r'[^\w\s\-()]', '', title)  # Düzeltilmiş regex deseni
        title = title.replace(' ', '_')  # Boşlukları alt çizgi ile değiştir
    else:
        print(f"Başlık bulunamadı: {detail_url}")
        return False
    
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
        return True
    else:
        print(f"Download butonu bulunamadı: {detail_url}")
        return False

# TXT dosyasından linkleri oku
def read_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = file.read().splitlines()
    return links

# TXT dosyasına linkleri yaz (silinen link hariç)
def write_links_to_file(file_path, links):
    with open(file_path, 'w') as file:
        for link in links:
            file.write(link + '\n')

# Ana işlem
def main():
    file_path = 'detail_links.txt'
    
    # Linkleri dosyadan oku
    links = read_links_from_file(file_path)
    
    if not links:
        print("Dosyada link bulunamadı.")
        return
    
    # Rastgele bir link seç
    selected_link = random.choice(links)
    print(f"Seçilen link: {selected_link}")
    
    # Resmi indir
    if download_image_from_detail_page(selected_link):
        # İndirme başarılıysa linki listeden sil
        links.remove(selected_link)
        # Güncellenmiş listeyi dosyaya yaz
        write_links_to_file(file_path, links)
        print(f"Link dosyadan silindi: {selected_link}")
    else:
        print("İndirme başarısız oldu, link silinmedi.")

# Programı çalıştır
if __name__ == "__main__":
    main()