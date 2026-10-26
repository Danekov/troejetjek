import json, os, socket, time, urllib.request

# Foretræk IPv4 (GitHub-runnere har nogle gange ikke IPv6-forbindelse)
_orig = socket.getaddrinfo
socket.getaddrinfo = lambda *a, **k: [r for r in _orig(*a, **k) if r[0] == socket.AF_INET] or _orig(*a, **k)

URL = "https://shoppen.brondby.com/products/udebanetroje-l-s-26-27.js"
SIDE = "https://shoppen.brondby.com/products/udebanetroje-l-s-26-27"
TOPIC = os.environ["NTFY_TOPIC"]
STR = os.environ.get("STOERRELSE", "L").strip().upper() or "L"


def proev(funktion, forsoeg=5):
    for i in range(forsoeg):
        try:
            return funktion()
        except Exception as e:
            print(f"Forsøg {i + 1} fejlede: {e}")
            if i == forsoeg - 1:
                raise
            time.sleep(5 * (i + 1))


def hent():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=20))


data = proev(hent)
v = next(v for v in data["variants"] if v["title"].strip().upper() == STR)
print(f"{STR} på lager:", v["available"])

if v["available"]:
    tekst = f"Størrelse {STR} er på lager!"
    if STR != "L":
        tekst = "TEST: " + tekst

    def send():
        urllib.request.urlopen(urllib.request.Request(
            f"https://ntfy.sh/{TOPIC}", data=tekst.encode(),
            headers={"Title": "Brondby-troeje", "Click": SIDE, "Priority": "high"}), timeout=15)

    proev(send)
    print("Besked sendt")
