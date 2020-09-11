import sqlite3


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {
            "name": self.name,
            "price": self.price
        }
    
    @classmethod
    def find_by_name(cls, name):
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM items WHERE name=?"
            cursor.execute(query, (name,))
            row = cursor.fetchone()
            if row:
                return cls(*row)
    
    def insert(self):
        try:
            with sqlite3.connect("data.db") as connection:
                cursor = connection.cursor()
                query = "INSERT INTO items VALUES (?, ?)"
                cursor.execute(query, (self.name, self.price))
                connection.commit()
                return self
        except Exception as e:
            print(f"Exception in class mothod Item.insert(cls, item): {e}")

    def update(self):
        try:
            with sqlite3.connect("data.db") as connection:
                cursor = connection.cursor()
                query = "UPDATE items SET price=? WHERE name=?"
                cursor.execute(query, (self.price, self.name))
                connection.commit()
                return self
        except Exception as e:
            print(f"Exception in class method Item.update(cls, item): {e}")
