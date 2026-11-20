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

from html import escape
from pathlib import Path

cards = []

for coin in coins:
    name = escape(str(coin.get("name", "")))
    symbol = escape(str(coin.get("symbol", "")).upper())
    price = number(coin.get("current_price"), 6)
    change_value = coin.get("price_change_percentage_24h")
    change = number(change_value)
    color = "#4ade80" if (change_value or 0) >= 0 else "#f87171"

    cards.append(
        f'<article><strong>{name} ({symbol})</strong>'
        f'<p>{price} USD</p>'
        f'<span style="color:{color}">24 saat: %{change}</span>'
        f'</article>'
    )

page = """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="apple-mobile-web-app-capable" content="yes">
<title>Kripto Takip</title>
<style>
body{background:#0b1220;color:#e5e7eb;font-family:system-ui;
margin:0;padding:20px}
h1{font-size:26px}
.note{color:#a6b3c8;font-size:14px;line-height:1.6}
article{background:#172237;border-radius:16px;
padding:18px;margin:12px 0}
article p{font-size:21px;margin:12px 0}
input{box-sizing:border-box;width:100%;padding:15px;
border-radius:12px;border:1px solid #44516a;
background:#172237;color:white;font-size:16px}
</style>
</head>
<body>
<h1>Kripto Takip</h1>
<p class="note">Yalnızca piyasa verisi. Alım-satım yapılmaz.<br>
Son güncelleme: UPDATE_TIME</p>
<input placeholder="Coin ara..."
oninput="document.querySelectorAll('article').forEach(
el => el.hidden = !el.textContent.toLowerCase().includes(
this.value.toLowerCase()))">
<main>COIN_CARDS</main>
<p class="note">Henüz teknik analiz, sanal işlem ve Telegram yoktur.</p>
</body>
</html>"""

page = page.replace("UPDATE_TIME", escape(updated))
page = page.replace("COIN_CARDS", "".join(cards))

Path("public").mkdir(exist_ok=True)
Path("public/index.html").write_text(page, encoding="utf-8")
print("Mobil panel dosyasi hazirlandi.")
