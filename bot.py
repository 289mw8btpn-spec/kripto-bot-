import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

url = "https://api.coingecko.com/api/v3/ping"
request = Request(url, headers={"User-Agent": "crypto-paper-test/1.0"})

try:
    with urlopen(request, timeout=30) as response:
        result = json.load(response)

    print("VERI BAGLANTISI BASARILI")
    print(json.dumps(result, ensure_ascii=False))
    print("Bu test emir gondermez ve API anahtari kullanmaz.")

except HTTPError as error:
    print("HTTP hata kodu:", error.code)
    print(error.read().decode("utf-8", errors="replace")[:1500])
    raise
