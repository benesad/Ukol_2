# Toto je repozitář s druhým úkolem.
### Zadání a očekávání od programu
Pro zvolenou množinu adresních bodů a množinu kontejnerů na tříděný odpad program zjistí průměrnou a maximální vzdálenost k nejbližšímu kontejneru na tříděný odpad. Pro každý adresní bod tedy určí nejbližší kontejner na tříděný odpad a následně z těchto vzdáleností spočte průměr, medián a maximum. Průměr, medián a maximum vypíše, pro maximum vypíše i adresu, která má nejbližší kontejner nejdále. Program započítává i neveřejné kontejnery k adresám, na kterých jsou přiděleny a započítává do statistik vzdálenost rovnou nule.
### Vstupní data
Vstupními daty jsou 2 soubory GeoJSON. První obsahuje adresní body zvolené
čtvrti ve WGS-84, lze jej stáhnout z [Overpass
Turbo](http://overpass-turbo.eu/s/11rE). V souboru program nalezne atribut `addr:street` jméno ulice a v atributu
`addr:housenumber` nalezne číslo orientační / číslo popisné, a ty následně používá a případně vypíše do výstupu. Soubor je v repozitáři jako `adresy.geojson` a pod tímto jménem ho program také načítá.

Druhý soubor obsahuje souřadnice kontejnerů na tříděný odpad, lze jej stáhnout z
[pražského Geoportálu](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB)
v S-JTSK. Každý kontejner obsahuje v atributu `STATIONNAME` adresu, kde se
nachází a v atributu `PRISTUP`, zda je veřejně přístupný, nebo je přístupný
pouze obyvatelům domu. Soubor je v repozitáři pojmenovaný `kontejnery.geojson` a pod tímto jménem ho program také načítá.

Oba souboru obsahují pouze testovací data,, nikoliv kompletní data tak, jak byly stažena, ačkoliv program funguje se všemi validními soubory se správným názvem a příponou `.geojson`.
### Výstup
xxxxx