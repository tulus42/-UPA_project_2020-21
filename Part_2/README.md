# README.md pre projekt z predmetu UPA
Je možné použiť nástroj [DILLINGER](https://dillinger.io/) pre lepšiu čitateľnosť tohto súboru
Tento readme obsahuje popis odovzdaných súborov a ich využitia pre splnenie zadania projektu. 

## Odovzdané súbory
Súbory pozostávajú z niekoľkých skriptov napísaných v bash-i a Python-e. 

Odovzdaný adresár obsahuje súbor *install.sh* ktorý je pripravený na čistú inštaláciu všetkých potrebných komponent pre operačný systém Ubuntu 20.04. Na ostatných Unixových systémoch alebo iných verziach Ubuntu nie je kompatibilita zaručená. Inštaláciu je možné začať spustením inštalačného skriptu *./install.sh*. Prvotná inštalácia nachystá obe databázy, stiahne a upraví dáta a spustí GUI. Ak nie je potrebné zaistiť splnenie požiadaviek, alebo je potrebné iba aktualizať dáta, je možné ručne spustiť tri skripty samostatne (popísané nižšie).

Prípravu a uloženie neštruktúrovaných dát do NoSQL databáze MongoDB je možné spustiť pomocou súboru *prepData.sh*, ktorý automaticky stiahne a importuje všetko potrebné do NoSQL databáze. Pri aktiulizácií dát je nutné tento skript spustiť ako prvý.

Po úspešnom importe dát je možné využiť skript *convertData.py* na úpravu a prenos dát z NoSQL do SQL databáze (obe tieto databázy boli inštalované pomocou *install.sh* skriptu, ak nie, je možné, že nebudú správne nastavené prístupové práva a heslá). Prípravu a prenos dát do SQL databáze je možné začať spustením skriptu *python3 convertData.py*. Pri aktualizáci dát je nutné tento skript spustiť ako druhý.

Ďalej odovzdaný adresár obsahuje súbor requirements.txt pre prípadnú manuálnu inštaláciu. Tento súbor obsahuje potrebné python3 knižnice a ich verzie, ktoré sú potrebné pre spustenie nami odovzdaných python skriptov.

Súbor *gui.py* obsahuje implementáciu intuitívneho grafického rozhrania a slúži na zodpovedanie dotazov k tomuto projektu. Grafické rozhranie je implementované pomocou knižnice *tkinter*, ktorá je natívne prítomná v štandardnej distribúcií jazyka Python. Grafické rozhranie je možné spustiť príkazom *python3 gui.py*.

Zvyšné odovzdané súbory sú pomocné súbory pre zabezpečenie správneho behu jednotlivých skriptov a ich podstata je bližšie popísaná v dokumentácií.