import os
import subprocess
import sys
import pandas as pd
import csv


# Calculate the absolute path to the directory two levels up
project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))
#  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print("Adding to sys.path:", project_root)
sys.path.insert(0, project_root)

from database.designPatterns import DatabaseOperations

def split_filename(filename):
    # Define the pattern to match the file name
    pattern = r'^(.*?)_\((.*?)\)\.csv$'
    
    # Use regular expressions to extract librarySRC and collection
    match = re.match(pattern, filename)
    if match:
        librarySRC = match.group(1).replace('_', ' ')
        collection = match.group(2)
        return librarySRC, collection
    else:
        return None, None
    
def split_filename(filename):
    # Replace underscores with spaces
    filename_parts = filename.replace('_', ' ').split('(')
    
    # Extract librarySRC and collection
    librarySRC = filename_parts[0].strip()
    collection = filename_parts[1].replace(')', '').strip()
    
    return librarySRC, collection

def run():
    db_ops = DatabaseOperations()



    spider_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scrapers", "digital_lib_scraper", "spiders"))
    spider_files = os.listdir(spider_path)
    data_path =  os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
    master_path = os.path.join(data_path, "MasterSpider.csv")
    with open(master_path, 'w') as file:
        pass

    # data_files = os.listdir(data_path)
    # data_files = [name.replace('.csv', '') for name in data_files ]
    spider_df = pd.DataFrame({"spider": spider_files})
    # data_df = pd.DataFrame({"data": data_files})
    run_spider = spider_df[spider_df["spider"].str.contains("_Spider")]
    # run_spider = run_spider[~run_spider["spider"].str.contains('|'.join(data_df["data"]))]
    # print(run_spider)
    
    manual_data_files = os.listdir("../scrapers/manual_data_input")
    
    
    for file in run_spider["spider"]:
        cmd = "scrapy runspider " + '"' + os.path.join(spider_path, file) + '"' # to check error message: -v 2"
        subprocess.run(cmd, shell=True, check=True, text=True, stdout=subprocess.PIPE)
        file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/MasterSpider.csv"))
        db_ops.insert_csv_data(file_path)


   
    for file in manual_data_files:
         if file.endswith('.csv'):
            librarySRC, collection = split_filename(file)
            db_ops = DatabaseOperations()
            db_ops.delete_rows_by_combination(librarySRC,collection)
            copy_csv(file, master_path)
            file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/MasterSpider.csv"))
            db_ops.insert_csv_data(file_path)
        
def copy_csv(source_path, destination_path):
    with open(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scrapers","manual_data_input",source_path)), mode='r', newline='') as source_file:
        reader = csv.reader(source_file)
        
        with open(destination_path, mode='w', newline='') as dest_file:
            writer = csv.writer(dest_file)
            
            # Copy each row from the source CSV to the destination CSV
            for row in reader:
                writer.writerow(row)

if __name__ == '__main__':
    run()