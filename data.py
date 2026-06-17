import json
import sqlite3
from entities.seafood import SeafoodManager
from entities.mining_node import MiningNodeManager

class DataManager:
    def __init__(self):
        self.supported_types = {'seafood': SeafoodManager, 'mining_node': MiningNodeManager}

    def migrate(self, item_type):
        if item_type not in self.supported_types:
            print(f"Unsupported type: {item_type}. Only {list(self.supported_types.keys())} are supported.")
            return

        item_manager = self.supported_types[item_type]()
        data = item_manager.fetch_data()

        schema = item_manager.schema
        col_defs = ', '.join(f'{name} {typ}' for name, typ in schema)
        col_names = ', '.join(name for name, _ in schema)
        placeholders = ', '.join(f':{name}' for name, _ in schema)

        with sqlite3.connect(f'./data/{item_type}.db') as conn:
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {item_type} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {col_defs}
                )
            """)
            conn.executemany(
                f"INSERT INTO {item_type} ({col_names}) VALUES ({placeholders})",
                data
            )
            print(f"Inserted {len(data)} rows into {item_type} table.")
    
    def clear_table(self, item_type):
        if item_type not in self.supported_types:
            print(f"Unsupported type: {item_type}. Only {list(self.supported_types.keys())} are supported.")
            return

        with sqlite3.connect(f'./data/{item_type}.db') as conn:
            conn.execute(f"DELETE FROM {item_type}")
            print(f"Cleared all data from {item_type} table.")

if __name__ == "__main__":

    data_manager = DataManager()
    data_manager.migrate('seafood')
    data_manager.migrate('mining_node')
