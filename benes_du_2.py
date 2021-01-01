import json, os
from pyproj import CRS, Transformer
from math import sqrt
from sys import exit

CESTA_KONTEJNERY = "kontejnery.geojson"
CESTA_ADRESY = "adresy.geojson"

def ziskej_souradsys():
    """*Ziskani souradnic systemu ve formatu S-JTSK."""
    return prevod_WGS_na_SJTSK(CRS.from_epsg(4326))

def prevod_WGS_na_SJTSK(wgs):
    """*Prevod z WGS-84 na S-JTSK."""
    return Transformer.from_crs(wgs, CRS.from_epsg(5514))

def nacteni_souboru(nazev):
    """*Nacteni souboru a validace, jestli soubor existuje."""
    try:
        return open(nazev, "r", encoding="UTF-8")
    except FileNotFoundError:
        print(f"Pozadovany soubor {nazev} neexistuje.")
        exit()

def cteni_jsonu_features(soubor,nazev):
    """*Prijme na vstupu soubor a jeho obsah precte jako JSON a vrati vysledek pod klicem "features". 
    Provede validaci, pokud dojde pri cteni k chybe."""
    try:
        return json.load(soubor)["features"]
    except ValueError as e: # validuje i pokud se jedna o validni JSON
        print(f"Soubor {nazev} neni validni.\n", e)
        exit()
        
def cteni_kontejneru(misto):
    ulice = misto["properties"]["STATIONNAME"]
    souradnice = misto["geometry"]["coordinates"]
    pristup = misto["properties"]["PRISTUP"]

    if pristup=="volně":
        return ulice, souradnice
    return None, None

def cteni_adresy(misto):
    ulice = misto["properties"]["addr:street"] + " " + misto["properties"]["addr:housenumber"]
    souradnice_sirka = misto["geometry"]["coordinates"][1]
    souradnice_delka = misto["geometry"]["coordinates"][0]

    return ulice, wgsdojtsk.transform(souradnice_sirka, souradnice_delka)

wgsdojtsk = ziskej_souradsys()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

soubor_kontejnery = nacteni_souboru(CESTA_KONTEJNERY)
soubor_adresy = nacteni_souboru(CESTA_ADRESY)

data_kontejnery = cteni_jsonu_features(soubor_kontejnery, CESTA_KONTEJNERY)
data_adresy = cteni_jsonu_features(soubor_adresy, CESTA_ADRESY)

serializace_kontejnery = serializace_dat(data_kontejnery)

serializace_adresy = serializace_dat(data_adresy, False)

maximum = max(vzdalenosti.values())

for (adresa, vzdalenost) in vzdalenosti.items():
    if vzdalenost == maximum:
        nejvzdalenejsi = adresa

vzdalenosti = generovani_min_vzdalenosti(serializace_kontejnery, serializace_adresy)

# vypsani vysledku v terminalu

print(f"Nacteno adresnich bodu: {len(serializace_adresy)}")
print(f"Nacteno kontejneru na trideny odpad: {len(serializace_kontejnery)}")

print(
    "\n"
    "Prumerna vzdalenost adresniho bodu k verejnemu kontejneru: "
    f"{prumer:.0f} metru"
)

print(f"Median vzdalenosti ke kontejneru: {median:.0f} metru")

print(
    f"Nejdale je ke kontejnerum je z adresy '{nejvzdalenejsi}' "
    f"a to {maximum:.0f} metru."
)