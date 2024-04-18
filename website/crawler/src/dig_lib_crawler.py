import os
import subprocess
import pandas as pd

def run():


    spider_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scrapers", "digital_lib_scraper", "spiders"))
    spider_files = os.listdir(spider_path)
    data_path =  os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
    master_path = os.path.join(data_path, "MasterSpider.csv")
    with open(master_path, 'w') as file:
        pass

    # data_files = os.listdir(data_path)
    # data_files = [name.replace('.csv', '') for name in data_files ]
    # spider_df = pd.DataFrame({"spider": spider_files})
    # data_df = pd.DataFrame({"data": data_files})
    # run_spider = spider_df[spider_df["spider"].str.contains("_Spider")]
    # run_spider = run_spider[~run_spider["spider"].str.contains('|'.join(data_df["data"]))]
    # print(run_spider)
    
    for file in spider_files["spider"]:
        cmd = "scrapy runspider " + '"' + os.path.join(spider_path, file) + '"' # to check error message: -v 2"
        subprocess.run(cmd, shell=True, check=True, text=True, stdout=subprocess.PIPE)

if __name__ == '__main__':
    run()