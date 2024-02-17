import os
import psycopg2
from dotenv import load_dotenv

class DatabaseOperations:
    def __init__(self):
        load_dotenv()
        self.connection_string = "postgresql://PhilopateerAz:CF3q1wNWbOle@ep-lively-hat-a5tacpqp.us-east-2.aws.neon.tech/Project22?sslmode=require"
        self.conn = psycopg2.connect(self.connection_string)

    def __del__(self):
        if hasattr(self, 'conn') and self.conn is not None:
            self.conn.close()

    def add_collection(self, collection_name, path, libraries):
        cur = self.conn.cursor()
        sql = "INSERT INTO collections (collectionName, path, libraries) VALUES (%s, %s, %s)"
        cur.execute(sql, (collection_name, path, libraries))
        self.conn.commit()
        cur.close()

    def add_collection_name_path(self, collection_name, path):
        cur = self.conn.cursor()
        sql = "INSERT INTO collections (collectionName, path) VALUES (%s, %s)"
        cur.execute(sql, (collection_name, path))
        self.conn.commit()
        cur.close()

    def remove_collection(self, path):
        cur = self.conn.cursor()
        sql = "DELETE FROM collections WHERE path = %s"
        cur.execute(sql, (path,))
        self.conn.commit()
        cur.close()

    def edit_collection(self, collection_name, path, libraries):
        cur = self.conn.cursor()
        sql = "UPDATE collections SET collectionName = %s, libraries = %s WHERE path = %s"
        cur.execute(sql, (collection_name, libraries, path))
        self.conn.commit()
        cur.close()

    def lookup_collection(self, path):
        cur = self.conn.cursor()
        sql = "SELECT * FROM collections WHERE path = %s"
        cur.execute(sql, (path,))
        result = cur.fetchone()
        cur.close()
        return result

    def get_unique_collection_names(self):
        cur = self.conn.cursor()
        sql = "SELECT DISTINCT collectionName FROM collections"
        cur.execute(sql)
        result = [row[0] for row in cur.fetchall()]
        cur.close()
        return result

# Example usage:
# db = DatabaseOperations()
# db.add_collection("MyCollection", "/path/to/collection", "library1, library2")
# db.add_collection_name_path("AnotherCollection", "/another/path")
# print(db.lookup_collection("/path/to/collection"))
# print(db.get_unique_collection_names())
