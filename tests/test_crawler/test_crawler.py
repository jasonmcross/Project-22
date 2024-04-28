import os

import subprocess
import psycopg2
from database import DatabaseOperations

def test(self):
    db_ops = DatabaseOperations() 
    db_ops.deleteAll()
    
    if db_ops.get_unique_collections() ==0 : print ("database is empty and no libraries stored")
    
    # Execute the external Python crawler script
    crawler_script_path = "../website/crawler/src/dig_lib_crawler.py"
    subprocess.run(["python", crawler_script_path], check=True)
    
    if db_ops.get_unique_collections() != 0: print ("datavase is updated and data was stored correctly")
