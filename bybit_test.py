import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

base = "https://api-testnet.bybit.com"

for interval in ("240", "D"):
    url = (
        base + "/v5/market/kline"
        "?category=spot&symbol=BTCUSDT"
        f"&interval={interval}&limit=5"
    )

    request = Request(
        url, headers={"User-Agent": "crypto-connection-test/1.0"}
    )

    try:
        with urlopen(request, timeout=30) as response:
            data = json.load(response)

        if data.get("retCode") != 0:
            raise RuntimeError(
                f"Bybit hata yaniti: {data.get('retMsg')}"
            )

        candles = data.get("result", {}).get("list", [])
        if not candles:
            raise RuntimeError("Mum verisi gelmedi.")

        label = "4 saatlik" if interval == "240" else "Gunluk"
        print(f"{label} veri baglantisi BASARILI.")
        print(f"Gelen mum sayisi: {len(candles)}")

    except HTTPError as error:
        print("HTTP hata kodu:", error.code)
        print(error.read().decode("utf-8", errors="replace")[:1000])
        raise

print("Kontrol tamamlandi. Hicbir emir gonderilmedi.")
