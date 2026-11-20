import json
import os
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError

url = (
    "https://api.coingecko.com/api/v3/coins/markets"
    "?vs_currency=usd"
    "&order=market_cap_desc"
    "&per_page=200"
    "&page=1"
    "&sparkline=false"
)

request = Request(
    url,
    headers={"User-Agent": "crypto-paper-dashboard/1.0"}
)

try:
    with urlopen(request, timeout=40) as response:
        coins = json.load(response)

    if not isinstance(coins, list) or not coins:
        raise RuntimeError("Coin listesi alinamadi.")

    def number(value, digits=2):
        if value is None:
            return "-"
        return f"{float(value):,.{digits}f}"

    updated = datetime.now(timezone.utc).strftime(
        "%d.%m.%Y %H:%M UTC"
    )

    lines = [
        "# Kripto takip paneli",
        "",
        "Mod: Yalnizca veri takibi. Emir gonderilmez.",
        f"Guncelleme: {updated}",
        f"Gelen coin sayisi: {len(coins)}",
        "",
        "| Sira | Coin | Fiyat USD | 24s % | Hacim USD |",
        "|---|---|---|---|---|",
    ]

    for coin in coins:
        symbol = str(coin.get("symbol", "")).upper()
        symbol = symbol.replace("|", "").replace("\n", "")
        rank = coin.get("market_cap_rank") or "-"
        price = number(coin.get("current_price"), 6)
        change = number(coin.get("price_change_percentage_24h"))
        volume = number(coin.get("total_volume"), 0)

        lines.append(
            f"| {rank} | {symbol} | {price} | "
            f"{change} | {volume} |"
        )

    report = "\n".join(lines)

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as file:
            file.write(report + "\n")

    print(f"Liste alindi: {len(coins)} coin.")
    print("Tablo, bu calistirmanin Summary sayfasinda.")
    print("Henuz teknik analiz veya sanal islem yapilmiyor.")

except HTTPError as error:
    print("HTTP hata kodu:", error.code)
    print(error.read().decode("utf-8", errors="replace")[:1500])
    raise
