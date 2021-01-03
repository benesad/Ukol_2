import json, os
from pyproj import CRS, Transformer
from math import sqrt
from sys import exit

CESTA_KONTEJNERY = "kontejnery.geojson"
CESTA_ADRESY = "adresy.geojson"

def ziskej_souradsys():
    """Ziskani souradnic systemu ve formatu S-JTSK."""
    return prevod_WGS_na_SJTSK(CRS.from_epsg(4326))

def prevod_WGS_na_SJTSK(wgs):
    """Prevod z WGS-84 na S-JTSK."""
    return Transformer.from_crs(wgs, CRS.from_epsg(5514))

def nacteni_souboru(nazev):
    """Nacteni souboru a validace, jestli soubor existuje a ma k nemu pristup."""
    try:
        with open(nazev, "r", encoding="UTF-8") as soubor:
            return json.load(soubor)["features"]
    except FileNotFoundError:
        print(f"CHYBA: Pozadovany soubor {nazev} neexistuje.")
        exit()
    except PermissionError:
        print(f"CHYBA: Nemam pristup k {nazev}." )
        exit()
    except ValueError as e: # validuje i pokud se jedna o validni JSON
        print(f"CHYBA: Soubor {nazev} neni validni.\n", e)
        exit()
        
def cteni_kontejneru(misto):
    """Cte informace z kontejnery.json potrebne pro praci. Pokud PRISTUP neni volne, tak nastavi souradnice None."""
    ulice = misto["properties"]["STATIONNAME"]
    souradnice = misto["geometry"]["coordinates"]
    pristup = misto["properties"]["PRISTUP"]

    if pristup=="volně": # selekce pouze volne stojicich kontejneru
        return ulice, souradnice
    return ulice, None

def cteni_adresy(misto):
    """Cte ulice a cisla domu, vysledek spoji, dale cte souradnice danych mist."""
    ulice = misto["properties"]["addr:street"] + " " + misto["properties"]["addr:housenumber"]
    souradnice_sirka = misto["geometry"]["coordinates"][1]
    souradnice_delka = misto["geometry"]["coordinates"][0]

    return ulice, wgsdojtsk.transform(souradnice_sirka, souradnice_delka)

def nacteni_dat(data, jeToKontejner=True):
    nacteni = {}
    pocet_neplatnych = 0

    for misto in data:
        try:
            if jeToKontejner:
                ulice, souradnice = cteni_kontejneru(misto)
            else:
                ulice, souradnice = cteni_adresy(misto)
            
            nacteni[ulice] = souradnice
        except KeyError:
            pocet_neplatnych+=1

    nazev = "kontejneru"
    if jeToKontejner==False:
        nazev = "adres"

    if pocet_neplatnych > 0:
        print(f"POZOR: vyradil jsem {pocet_neplatnych} {nazev}, protoze neobsahovaly potrebna data.")

    if len(nacteni)==0:
        print(f"CHYBA: nemam k dispozici dostatecny pocet dat pro vypocet (u {nazev}).")
        exit()

    return (nacteni)
    
def pythagoras(s1, s2):
    return sqrt((s1[0] - s2[0])**2 + (s1[1] - s2[1])**2)

def hledani_min_vzdalenosti(kontejnery, adresy):
    """Hleda minimalni vzdalenost od kontejneru."""
    vzdalenosti = {}

    for (adresa_ulice, adresa_souradnice) in adresy.items():

        min_vzd = -1
        prvni = True

        for kontejnery_ulice, kontejnery_souradnice in kontejnery.items():
            if kontejnery_souradnice==None and kontejnery_ulice==adresa_ulice:
                min_vzd = 0
                break
            if kontejnery_souradnice==None:
                continue
            
            vzdalenost = pythagoras(adresa_souradnice, kontejnery_souradnice)
            if prvni or vzdalenost < min_vzd:
                min_vzd = vzdalenost
                prvni = False

        if min_vzd > 10000: # osetreni, ze vzdalenost je mensi nez 10 km
            print(" CHYBA: Kontejner je dale nez 10 km.")
            exit()

        vzdalenosti[adresa_ulice] = min_vzd

    return vzdalenosti

def median(vzdalenosti):
    """Vypocet medianu"""
    sez_vzdalenosti = list(vzdalenosti.values())
    sez_vzdalenosti.sort()
    p = (len(sez_vzdalenosti) - 1) // 2

    # kdyz vyjde zbytek po vypoctu 0, program vypise false
    # kdyz vyjde zbytek po vypoctu 1, program vypise true
    if len(sez_vzdalenosti) % 2:
        return sez_vzdalenosti[p]

    return (sez_vzdalenosti[p] + sez_vzdalenosti[p + 1]) / 2

wgsdojtsk = ziskej_souradsys()

os.path.dirname(os.path.abspath(__file__))

data_kontejnery = nacteni_souboru(CESTA_KONTEJNERY)
data_adresy = nacteni_souboru(CESTA_ADRESY)

nacteni_kontejnery = nacteni_dat(data_kontejnery)

nacteni_adresy = nacteni_dat(data_adresy, False)

vzdalenosti = hledani_min_vzdalenosti(nacteni_kontejnery, nacteni_adresy)

prumer = sum(vzdalenosti.values()) / len(vzdalenosti)

median = median(vzdalenosti)

maximum = max(vzdalenosti.values())

for (adresa, vzdalenost) in vzdalenosti.items():
    if vzdalenost == maximum:
        nejvzdalenejsi = adresa

# vypsani vysledku v terminalu

print()
print(f"Nacteno adresnich bodu: {len(nacteni_adresy)}")
print(f"Nacteno kontejneru na trideny odpad: {len(nacteni_kontejnery)}")
print(f"Prumerna vzdalenost adresniho bodu ke kontejneru: "f"{prumer:.0f}"" metru")
print()
print(f"Median vzdalenosti ke kontejneru: {median:.0f} metru")
print(f"Nejdale je ke kontejneru je z adresniho bodu '{nejvzdalenejsi}', konkretne {maximum:.0f} metru")