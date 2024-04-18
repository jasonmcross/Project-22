import os
import csv
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

class DatabaseOperations:
    def __init__(self):
        load_dotenv()
        self.connection_string = "postgresql://PhilopateerAz:CF3q1wNWbOle@ep-lively-hat-a5tacpqp.us-east-2.aws.neon.tech/Project22?sslmode=require"
        self.conn = psycopg2.connect(self.connection_string)
        self.cur = self.conn.cursor()

    def __del__(self):
        if hasattr(self, 'conn') and self.conn is not None:
            self.conn.close()

    def insert_csv_data(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            #next(reader)  # Skip header row
            for row in reader:
                design_pattern, design_type, discretion, library_src, *extra = row
                collection_name = extra[0] if extra else None
                query = """
                INSERT INTO DesignPatterns (designPattern, designType, discretion, librarySRC, collectionName)
                VALUES (%s, %s, %s, %s, %s);
                """
                #
                self.cur.execute(query, (design_pattern, design_type, discretion, library_src, collection_name))

        self.conn.commit()

    def export_to_csv(self, csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(["designPattern", "designType", "discretion", "librarySRC", "collectionName"])
            # Fetch data from the database
            self.cur.execute("SELECT * FROM DesignPatterns")
            rows = self.cur.fetchall()
            for row in rows:
                writer.writerow(row)
    
    def delete_rows_by_combination(self, library_src_value, collection_name_value):
        query = """
        DELETE FROM DesignPatterns
        WHERE librarySRC = %s AND 
        collectionName = %s;
        """
        self.cur.execute(query, (library_src_value, collection_name_value))
        self.conn.commit()
        

    def get_unique_combinations(self):
        query = """
        SELECT DISTINCT librarySRC, collectionName
        FROM DesignPatterns;
        """
        self.cur.execute(query)
        rows = self.cur.fetchall()
        unique_combinations = [(f"{row[0]} ({row[1]})") for row in rows]
        return unique_combinations


    def get_unique_collections(self):
        query = """
        SELECT DISTINCT collectionName
        FROM DesignPatterns;
        """
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return [row[0] for row in rows]

    def export_collection_to_csv(self, collection_name):
        query = """
        SELECT designPattern, designType, discretion
        FROM DesignPatterns
        WHERE collectionName = %s;
        """
        self.cur.execute(query, (collection_name.strip(),))
        rows = self.cur.fetchall()
        source_filepath = Path(__file__).parent.parent / "website/Strategy/source_files/MasterSource.csv"
        combined_discription ={}
        for row in rows:
            design_pattern, design_type, discription = row
            key = (design_pattern, design_type)
            if key in combined_discription:
                combined_discription[key] += f" {discription}"
            else:
                combined_discription[key] = discription

                
        with open(source_filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            #writer.writerow(["designPattern", "designType", "discretion"])  # Write header
            for (design_pattern, design_type), description in combined_discription.items():
                writer.writerow([design_pattern, design_type, description ])

        
                
# Example usage
if __name__ == "__main__":
    db_ops = DatabaseOperations()
    #push all data
    csv_file_path = "../website/crawler/data/MasterSpider.csv"
    db_ops.insert_csv_data(csv_file_path)
    
    #get all data
    # csv_file_path = "../website/crawler/data/masterpull.csv"
    # db_ops.export_to_csv(csv_file_path)

    #delete library comb with collection
    #db_ops.delete_rows_by_combination("sourcemacking", "GOF")

    ###combination of collections and library
    # unique_combinations = db_ops.get_unique_combinations()
    # for combination in unique_combinations:
    #     print(combination)
        
    ###collections
    # unique_collections = db_ops.get_unique_collections()
    # for collection in unique_collections:
    #     print(collection)
    
    
    # csv_file_path = "../website/crawler/data/masterpull.csv"
    # db_ops.export_to_csv(csv_file_path)
    
    #pull for collection
    # collection_name = " GOF"
    # csv_file_path = "../website/Strategy/source_files/MasterSource.csv"
    # db_ops.export_collection_to_csv(collection_name, csv_file_path)