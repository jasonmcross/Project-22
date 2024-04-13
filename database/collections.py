import os
import psycopg2
from dotenv import load_dotenv

class DatabaseOperations:
    def __init__(self):
        load_dotenv()
        self.connection_string = "postgresql://PhilopateerAz:CF3q1wNWbOle@ep-lively-hat-a5tacpqp.us-east-2.aws.neon.tech/Project22?sslmode=require"
        print("url:", self.connection_string)
        self.conn = psycopg2.connect(self.connection_string)
        self.cur = self.conn.cursor()

    def __del__(self):
        if hasattr(self, 'conn') and self.conn is not None:
            self.conn.close()

    def insert_file_data(self):
        self.cur.execute("DELETE FROM collections")

        folder_path = '../website/source_files'
        files = os.listdir(folder_path)
        for file in files:
            #without the extension
            file_name_without_extension = os.path.splitext(file)[0]
            #with the extension
            file_name_extension = os.path.splitext(file)[1]
            # Create the path string
            file_path = f'website/source_files/{file_name_without_extension}{file_name_extension}'
            # Insert data into the database
            query = """
            INSERT INTO collections (collectionname, path) VALUES (%s, %s);
            """
            self.cur.execute(query, (file_name_without_extension, file_path))
        # Commit changes
        self.conn.commit()


    def get_collection_names(self):
            query = """
            SELECT collectionname FROM collections;
            """
            self.cur.execute(query)
            rows = self.cur.fetchall()
            return [row[0] for row in rows]

    def get_collection_path(self, collectionname):
        cur = self.conn.cursor()
        sql = "SELECT path FROM collections WHERE collectionname = %s"
        cur.execute(sql, (collectionname,))
        result = cur.fetchone()
        cur.close()
        return result [0]
    
# # Usage
# db_ops = DatabaseOperations()
# db_ops.insert_file_data()
# collection_names = db_ops.get_collection_names()
# print(collection_names)
# path = db_ops.get_collection_path("masterGOFNew")
# print (path)
