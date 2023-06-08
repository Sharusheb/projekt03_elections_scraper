"""projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Šárka Böhmová
email: sarka.bohmova@seznam.cz
discord: ShareenBoom#6281
"""

import requests
from bs4 import BeautifulSoup
import sys 
import csv


def get_rows(url: str) -> list:                                                 #Funkce získá všechna data z adresy URL
    print(f"Stahuji data z vložené URL: {url}")
    tables = BeautifulSoup(requests.get(url).text, 'html.parser').find_all\
    ("table", {"class": "table"})
    all_rows = [row for table in tables for row in table.find_all("tr")[2:]]
    return all_rows


def get_code_location(all_rows: list) -> tuple:                                 #Funkce získá kód a umístění z tabulky
    code = [row.find_all("td")[0].text for row in all_rows
            if row.find_all("td")[0].text != "-"]
    location = [row.find_all("td")[1].text for row in all_rows
                if row.find_all("td")[1].text != "-"]
    return code, location


def tables_detail(all_rows: list) -> tuple:                                     #Funkce "scrapne" URL a získá data
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    tab_district, tab_vote = [], []
    links = [base_url + row.find("a", href=True)["href"] for row in all_rows
             if row.find("a", href=True) is not None]
    for link in links:
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        tab_district.append(soup.find_all("table", {"class": "table"})[0])
        tab_vote.extend(soup.find_all("table", {"class": "table"})[1:3])
    return tab_district, tab_vote


def get_votes(tab_district: list) -> tuple:                                     #Funkce získá počty registrovaných voličů, počet obálek a počet platných hlasů
    register = [tab.find("td",{"class": "cislo", "data-rel": "L1",
                         "headers": "sa2"}).text.replace("\xa0","") 
                         for tab in tab_district]
    envelope = [tab.find("td", {"class": "cislo", "data-rel": "L1",
                         "headers": "sa3"}).text.replace("\xa0","") 
                         for tab in tab_district]
    valid = [tab.find("td", {"class": "cislo", "data-rel": "L1",
                         "headers": "sa6"}).text.replace("\xa0","") 
                         for tab in tab_district]
    return register, envelope, valid


def get_head(tab_vote: list) -> list:                                           #Funkce se dostane do "hlavičky" tabulky
    head = [tr.find("td", {"class": "overflow_name"}).text 
            for tr in tab_vote[0].find_all("tr")[2:len(tab_vote[0])]]
    head.extend([tr.find("td", {"class": "overflow_name"}).text 
                 for tr in tab_vote[1].find_all("tr")[2:len(tab_vote[1])]])
    return head


def results(tab_vote: list) -> list:                                            #Funkce vrátí data o počtu platných hlasů pro jednotlivé strany
    result_1 = []
    result_2 = []
    for rows in tab_vote:
        value_1 = rows.find_all("td", {"class": "cislo", 
                                       "headers": "t1sa2 t1sb3"})
        value_2 = rows.find_all("td", {"class": "cislo", 
                                       "headers": "t2sa2 t2sb3"})
        values_1 = [v.text.replace("\xa0", "") for v in value_1]
        values_2 = [v.text.replace("\xa0", "") for v in value_2]
        if values_1:
            result_1.append(values_1)
        if values_2:
            result_2.append(values_2)
    final_list = list(zip(*result_1)) + list(zip(*result_2))
    return final_list


def create_dict(head: list, final_list: list) -> dict:                          #Funkce vytvoří slovník. Název strany = klič. Počet hlasů = hodnota.
    dict_vote = {}
    for i, party in enumerate(head):
        dict_vote[party] = final_list[i]
    return dict_vote


def scrape_url(url: str) -> dict:                                               #Funkce "srapne" URL a vráti všechna data pro vyýstup 
    all_rows = get_rows(url)
    tab_district, tab_vote = tables_detail(all_rows)
    code, location = get_code_location(all_rows)
    register, envelope, valid = get_votes(tab_district)
    dict_vote = create_dict(get_head(tab_vote), results(tab_vote))
    data_all = {"code":code, "location": location, "registered": register,
                "envelopes": envelope, "valid": valid,}
    data_all.update(dict_vote)
    return data_all


def save_to_csv(file_name: str, data_all: dict):                                #Funkce uloží data do CSV souboru
    with open(file_name, mode='w', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data_all.keys())
        writer.writerows(zip(*data_all.values()))


def main():                                                                     #Funkce spustí program
    if len(sys.argv) != 3:
        print("Musíte zadat 3 argumenty do terminálu\
(název hlavního soubouru, zkopírované URL stránky, název výsledného souboru v CSV)")
    else:
        url = sys.argv[1]
        csv = sys.argv[2]
        save_to_csv(csv, scrape_url(url))
        print(f"Váš výstup je uložen v {csv}")
    

if __name__ == "__main__":
    main()  