import os, re, sys
import requests

URL = "https://www.klikego.com/inscription/trail-du-cap-pointe-du-raz-2027/running-course-a-pied/1540877566210-11"
PHRASE_FERME = "pas encore ouvertes"
TOPIC = os.environ["NTFY_TOPIC"]


def notifier(titre, msg):
    requests.post(f"https://ntfy.sh/{TOPIC}", data=msg.encode("utf-8"),
                  headers={"Title": titre.encode("utf-8"), "Priority": "urgent", "Click": URL}, timeout=15)


if os.environ.get("TEST") == "1":
    notifier("Test Trail du Cap", "La notification fonctionne.")
    sys.exit(0)

r = requests.get(URL, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
r.raise_for_status()
page = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text)).lower()

if PHRASE_FERME in page:
    print("Toujours fermé")
else:
    notifier("Trail du Cap : inscriptions OUVERTES ?", "Le message 'pas encore ouvertes' a disparu. Fonce !")
    print("Alerte envoyée")
