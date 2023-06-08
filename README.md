# projekt03_elections_scraper

# Elections_scraper ze stránek https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ vytáhne výsledky voleb pro vámi dané město a uloží jej do souboru csv.

# nejprve je potřeba vytvořit virtuální prostředí a nainstalovat potřebné knihovny ze souboru requirements - po vytvoření virtuálního prostředí zadejte do příkazové řádky "pip install -r requirements.txt"

# soubor spustíte přes příkazovou řádku pomocí dvou argumentů - první argument je URL vybraného města, druhý argument je název csv souboru, do kterého se vám data vyscrapují

# příklad spuštění: python scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky.csv

# vytvoří se soubor vysledky.csv s daty vybraného města
