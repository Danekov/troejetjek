import json, os, urllib.request

URL = "https://shoppen.brondby.com/products/udebanetroje-l-s-26-27.js"
SIDE = "https://shoppen.brondby.com/products/udebanetroje-l-s-26-27"
TOPIC = os.environ["NTFY_TOPIC"]

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
data = json.load(urllib.request.urlopen(req, timeout=20))
l = next(v for v in data["variants"] if v["title"].strip().upper() == "L")
print("L på lager:", l["available"])

if l["available"]:
    urllib.request.urlopen(urllib.request.Request(
        f"https://ntfy.sh/{TOPIC}", data="Størrelse L er på lager!".encode(),
        headers={"Title": "Brondby-troeje", "Click": SIDE, "Priority": "high"}), timeout=15)
