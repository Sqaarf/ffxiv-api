from bs4 import BeautifulSoup
import requests
import json
import re

class SeafoodManager:
    schema = [
        ('name', 'TEXT NOT NULL'),
        ('icon', 'TEXT'),
        ('fishing_method', 'TEXT'),
        ('fishing_level', 'INTEGER'),
        ('location', 'TEXT'),
        ('wiki_url', 'TEXT'),
    ]

    def __init__(self):
        self.short_url = "https://ffxiv.consolegameswiki.com"
        self.url = "https://ffxiv.consolegameswiki.com/wiki/Seafood"

    def fetch_data(self):
        print(f"Fetching URL: {self.url}")
        response = requests.get(self.url)
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            seafood_table = soup.find('table', {'class': ['sortable', 'item', 'align-left', 'table']})
            print(f"Table found: {seafood_table is not None}")
            seafood_list = []
            rows = seafood_table.find_all('tr')[1:]  # Skip header row
            print(f"Total rows (excluding header): {len(rows)}")
            for i, row in enumerate(rows):
                cells = row.find_all('td')
                if len(cells) >= 5:
                    name = cells[0].text.strip()
                    icon_src = cells[1].find('img')['src'] if cells[1].find('img') else None
                    icon = f"https://ffxiv.consolegameswiki.com{icon_src}" if icon_src else None
                    fishing_method = cells[2].text.strip() if cells[2].text.strip() != '????' else None
                    raw_level = cells[3].text.strip()
                    level_match = re.match(r'(\d+)\s*(★*)', raw_level)
                    if level_match:
                        fishing_level = int(level_match.group(1))
                        stars = len(level_match.group(2))
                    else:
                        fishing_level = None
                        stars = 0
                    location = cells[4].text.strip() if cells[4].text.strip() != "" else None
                    entry = Seafood(name, icon, fishing_method, fishing_level, location).__dict__
                    # print(f"Row {i}: {entry}")
                    seafood_list.append(entry)
                else:
                    print(f"Row {i}: skipped (only {len(cells)} cells)")
            print(f"Total seafood parsed: {len(seafood_list)}")
            return seafood_list
        else:   
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return []

class Seafood:
    def __init__(self, name, icon, fishing_method, fishing_level, location):
        self.name = name
        self.icon = icon
        self.fishing_method = fishing_method
        self.fishing_level = fishing_level
        self.location = location
        self.wiki_url = f"https://ffxiv.consolegameswiki.com/wiki/{name.replace(' ', '_')}"