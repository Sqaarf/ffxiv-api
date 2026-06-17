from bs4 import BeautifulSoup
import requests

class MiningNodeManager:
    schema = [
        ('node_type', 'TEXT'),
        ('mining_level', 'INTEGER'),
        ('location', 'TEXT'),
        ('items', 'TEXT'),
    ]

    def __init__(self):
        self.short_url = "https://ffxiv.consolegameswiki.com"
        self.url = "https://ffxiv.consolegameswiki.com/wiki/Miner_Node_Locations"

    def fetch_data(self):
        print(f"Fetching URL: {self.url}")
        response = requests.get(self.url)
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            mining_node_table = soup.find('table', {'class': ['sortable','align-left', 'gathering-role']})
            print(f"Table found: {mining_node_table is not None}")
            mining_node_list = []
            rows = mining_node_table.find_all('tr')[1:]  # Skip header row
            print(f"Total rows (excluding header): {len(rows)}")
            for i, row in enumerate(rows):
                cells = row.find_all('td')
                if len(cells) >= 5:
                    mining_level = cells[0].text.strip()
                    node_type = cells[1].text.strip() 
                    location_name = cells[2].text.strip()
                    location_coordinates = cells[3].text.strip() 
                    location = f"{location_name} {location_coordinates}"
                    items_raw = cells[4].select(".icon-label-container > a")
                    items = [x.text for x in items_raw]
                    entry = MiningNode(node_type, mining_level, location, items).__dict__
                    # print(f"Row {i}: {entry}")
                    mining_node_list.append(entry)
                else:
                    print(f"Row {i}: skipped (only {len(cells)} cells)")
            print(f"Total mining_nodes parsed: {len(mining_node_list)}")
            return mining_node_list
        else:   
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return []

class MiningNode:
    def __init__(self, node_type, mining_level, location, items):
        self.node_type = node_type
        self.mining_level = mining_level
        self.location = location
        self.items = ', '.join(items)


if __name__ == "__main__":
    mnm = MiningNodeManager()
    data = mnm.fetch_data()
    print(data)
