import requests
from bs4 import BeautifulSoup

url = "https://vizvezetek-szerelo.net/dzsungelhangulat-a-furdoszobaban-5-noveny-amelyek-jol-birjak-az-extra-paratartalmat"  # Replace with your desired URL

# Send a GET request to the URL and retrieve the HTML content
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Extract the metadata tags from the HTML using BeautifulSoup
metadata = {}
for tag in soup.find_all("meta"):
    if tag.get("name") or tag.get("property"):
        name = tag.get("name") or tag.get("property")
        value = tag.get("content")
        metadata[name] = value

title = metadata['og:title']
description = metadata['description']
if len(description) > 200:
    description = description[:200] + "..."
text = f"""
A 0-24 Varga Lakásszerviz Kft segít Önnek bármikor!
https://vizvezetek-szerelo.net/
További ajánlatunkért keresse fel weboldalunkat, referenciákért nézze meg Facebook oldalunk! 🏡

{title}
{description}
A teljes cikk elolvasásához kattintson az alábbi linkre!
{url}

Szolgáltatásaink elérhetőek éjjel-nappal. 🤩
Bármilyen gondja adódna, keressen minket bizalommal. 📞 +36301367069 📞
Ingyenes helyszíni felméréssel és tanácsadással, számlaképes szakembereinkkel 👷🏽 állunk rendelkezésére, még hétvégén és ünnepnapokon is! 🎉
"""

print(text)