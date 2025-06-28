import os
import requests
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Muat variabel dari file .env
load_dotenv()

# --- KONFIGURASI PENTING ---
# Ambil kredensial dari file .env
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
YOUR_CHAT_ID = os.getenv('CHAT_ID')

# Username channel sumber (diawali dengan '@')
SOURCE_CHANNEL_USERNAME = 'growagardenlivestock' # GANTI DENGAN USERNAME CHANNEL YANG BENAR

# Daftar item yang Anda inginkan (gunakan huruf kecil semua)
KEYWORDS = [
    'master sprinkler',
    'sugar apple',
    'feijoa',
    'prickly pear',
    'loquat',
    'bug egg',
    'paradise',
    'mythical egg',
    'rare summer egg',
    'weather event alert',
    'oasis egg',
    'pitcher plant',
    'bee egg'
]
# --- AKHIR KONFIGURASI ---

# Nama file sesi untuk menyimpan status login Anda
SESSION_FILE = 'my_telegram_session'

# Buat client Telethon
client = TelegramClient(SESSION_FILE, int(API_ID), API_HASH)

def send_notification(message_text):
    """Fungsi untuk mengirim notifikasi via bot Anda menggunakan requests."""
    print(f"Mengirim notifikasi untuk pesan: {message_text[:30]}...")
    pesan_kirim = f"🚨 ITEM INCERAN TERSEDIA! 🚨\n\n{message_text}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": YOUR_CHAT_ID, "text": pesan_kirim}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Notifikasi berhasil dikirim!")
        else:
            print(f"Gagal mengirim notifikasi: {response.text}")
    except Exception as e:
        print(f"Terjadi error saat mengirim notifikasi: {e}")

@client.on(events.NewMessage(chats=SOURCE_CHANNEL_USERNAME))
async def handle_new_message(event):
    """Fungsi yang berjalan setiap ada pesan baru di channel sumber."""
    message_text = event.raw_text
    message_lower = message_text.lower()
    print(f"Menerima pesan baru dari {SOURCE_CHANNEL_USERNAME}")

    # Cek apakah ada kata kunci yang cocok di dalam pesan
    for item in KEYWORDS:
        if item in message_lower:
            print(f"ITEM DITEMUKAN: '{item.upper()}'")
            send_notification(message_text)
            # Hentikan pengecekan jika satu item sudah ditemukan agar tidak spam
            break

async def main():
    """Fungsi utama untuk menjalankan client."""
    # Pastikan bot notifikasi sudah di-start oleh Anda
    print("Pastikan Anda sudah menekan /start pada bot notifikasi Anda.")
    print("Menjalankan client...")
    await client.start()
    print(f"Client berhasil terhubung! Mendengarkan pesan dari channel: {SOURCE_CHANNEL_USERNAME}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Pastikan untuk menjalankan START pada bot notifikasi Anda di Telegram
    # agar bot bisa mengirimi Anda pesan.
    client.loop.run_until_complete(main())