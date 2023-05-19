"""projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Šárka Böhmová
email: sarka.bohmova@seznam.cz
discord: ShareenBoom#6281
"""

import requests
import csv
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def scrape_results(url, output_file):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the link for selecting a district
    links = soup.find_all('a', href=True)
    if not links:
        print("Link for selecting a district not found.")
        return

    for link in links:
        district_url = link.get('href')
        if district_url and not district_url.startswith('javascript:'):
            district_url = urljoin(url, district_url)
            response = requests.get(district_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find links for all municipalities
            municipality_links = soup.find_all('a', href=True)
            if not municipality_links:
                print("Links for municipalities not found.")
                return

            with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                for municipality_link in municipality_links:
                    municipality_url = municipality_link['href']
                    if not municipality_url.startswith('javascript:'):
                        municipality_url = urljoin(district_url, municipality_url)
                        response = requests.get(municipality_url)
                        soup = BeautifulSoup(response.content, 'html.parser')

                        municipality_name_element = soup.find('h3')
                        if municipality_name_element:
                            municipality_name = municipality_name_element.text.strip()
                        else:
                            municipality_name = "N/A"  # Default value if element not found

                        voters = soup.find_all('td', class_='cislo')[:3]
                        voters_data = [int(vol.text.replace('\xa0', '').replace(',', '')) for vol in voters]

                        writer.writerow([municipality_link.text, municipality_name] + voters_data)

                        # Find additional data and write it to the CSV file
                        results_table = soup.find('table', class_='table')
                        if results_table:
                            results_rows = results_table.find_all('tr')[1:]  # Skip the header
                            for row in results_rows:
                                result_data = [cell.text.strip() for cell in row.find_all('td')]
                                writer.writerow(result_data)

                        # Find political parties and write them to the CSV file
                        parties_table = soup.find('table', class_='table')
                        if parties_table:
                            parties_rows = parties_table.find_all('tr')[1:]  # Skip the header
                            for row in parties_rows:
                                party_data = [cell.text.strip() for cell in row.find_all('td')]
                                writer.writerow(party_data)

            print(f"Results have been saved to the file {output_file}.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Incorrect usage. Please use: python your_script.py url output.csv")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    scrape_results(url, output_file)

                