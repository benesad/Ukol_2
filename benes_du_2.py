import json, os
from pyproj import CRS, Transformer
from math import sqrt
from sys import exit

CESTA_KONTEJNERY = "kontejnery.geojson"
CESTA_ADRESY = "adresy.geojson"

def nacteni_souboru(nazev):
    """*Nacteni souboru a validace, jestli soubor existuje"""
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
        

os.chdir(os.path.dirname(os.path.abspath(__file__)))

soubor_kontejnery = nacteni_souboru(CESTA_KONTEJNERY)
soubor_adresy = nacteni_souboru(CESTA_ADRESY)

data_kontejnery = cteni_jsonu_features(soubor_kontejnery, CESTA_KONTEJNERY)
data_adresy = cteni_jsonu_features(soubor_adresy, CESTA_ADRESY)