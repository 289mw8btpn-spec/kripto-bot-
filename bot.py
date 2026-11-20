import json
from urllib.request import urlopen
from datetime import datetime, timezone

def main():
    url = "https://testnet.binance.vision/api/v3/time"

    try:
        with urlopen(url, timeout=20) as response:
            result = json.load(response)

        server_time = datetime.fromtimestamp(
            result["serverTime"] / 1000,
            tz=timezone.utc
        )

        print("Binance Testnet bağlantısı başarılı.")
        print("Sunucu saati:", server_time.isoformat())
        print("Bu kontrol hiçbir alım-satım emri göndermez.")

    except Exception as error:
        print("Bağlantı kurulamadı:", error)
        raise

if __name__ == "__main__":
    main()
