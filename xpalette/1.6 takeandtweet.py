import os
import tweepy

# Twitter API anahtarları
API_KEY = "your_api_key"
API_SECRET_KEY = "your_api_secret_key"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Twitter API'sine bağlan
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Resmi Twitter'da paylaşan fonksiyon
def tweet_image(image_path):
    try:
        # Resmin adını al ve formatını düzelt
        image_name = os.path.basename(image_path).replace('.jpg', '')
        tweet_text = image_name.replace('_', ' ')  # Alt çizgileri boşlukla değiştir

        # Resmi Twitter'da paylaş
        media = api.media_upload(image_path)
        api.update_status(status=tweet_text, media_ids=[media.media_id])
        print(f"Tweet atıldı: {tweet_text}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

# İndirilen resimlerin bulunduğu klasör
image_folder = "downloaded_images"

# Klasördeki tüm resimleri Twitter'da paylaş
for image_file in os.listdir(image_folder):
    if image_file.endswith(".jpg"):
        image_path = os.path.join(image_folder, image_file)
        tweet_image(image_path)