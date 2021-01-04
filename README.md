## Toto je repozitář s druhým úkolem - vzdálenost kontejnerů na tříděný odpadod adresního bodu.
### Zadání
Pro zvolenou množinu adresních bodů a množinu kontejnerů na tříděný odpad program zjistí průměrnou a maximální vzdálenost k nejbližšímu kontejneru na tříděný odpad. Pro každý adresní bod tedy určí nejbližší kontejner na tříděný odpad a následně z těchto vzdáleností spočte průměr, medián a maximum. Průměr, medián a maximum vypíše, pro maximum vypíše i adresu, která má nejbližší kontejner nejdále. Program započítává i neveřejné kontejnery k adresám, na kterých jsou přiděleny a započítává do statistik vzdálenost rovnou nule.

### Vstupní data
Vstupními daty jsou 2 soubory GeoJSON. První obsahuje adresní body libovolné
čtvrti ve WGS-84, lze jej stáhnout z [Overpass
Turbo](http://overpass-turbo.eu/s/11rE). V souboru program musí najít atributy: 
* `addr:street` - jméno ulice a v atributu
* `addr:housenumber` - číslo orientační / číslo popisné

Ty následně používá a případně vypíše do výstupu. Souřadnice ve WGS-84 program přepočítá do S-JTSK. Soubor je v repozitáři jako `adresy.geojson` a pod tímto jménem ho program také načítá.


Druhý soubor obsahuje souřadnice kontejnerů na tříděný odpad, lze jej stáhnout z
[pražského Geoportálu](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB)
v S-JTSK. 
Každý kontejner obsahuje v atributu:
* `STATIONNAME` - adresu
* `PRISTUP` - volný, nebo pouze pro obyvatele domu
    
Soubor je v repozitáři pojmenovaný `kontejnery.geojson` a pod tímto jménem ho program také načítá.

Oba souboru obsahují pouze testovací data, nikoliv kompletní data tak, jak byla stažena, ačkoliv program funguje se všemi validními soubory se správným názvem a příponou `.geojson`.
### Výstup
Program vypíše počet načtených adresních bodů společně s počtem kontejnerů na tříděný odpad. Dále vypíše průměr a medián vzdálenosti ke kontejneru a nakonec vypíše nadresní bod, který má ke kontejneru nejdále. Nutno zmínit, že jakmile je vzdálenost kontejneru od adresního bodu větší než 10 km, program vypíše chybovou hlášku a vypne se. Program též upozorní chybovým hlášením pokud `.geojson` obsahuje záznam s chybějcím atributem potřebným ke kompletní statistice. 
#### Příklad výstupu
Takto vypadá příkladný výstup pro sadu testovacích dat.
```
Nacteno adresnich bodu: 20
Nacteno kontejneru na trideny odpad: 25

Prumerna vzdalenost adresniho bodu ke kontejneru: 676 metru
Median vzdalenosti ke kontejneru: 716 metru

Nejdale je ke kontejneru je z adresniho bodu 'U invalidovny 549/5', konkretne 1145 metru
```