import os
import subprocess

def run():

    dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scrapers", "digital_lib_scraper", "spiders"))
    files = os.listdir(dir_path)
    
    for file in files:
        if file.endswith("Spider.py"):
            cmd = "scrapy runspider " + '"' + os.path.join(dir_path, file) + '"' # to check error message: -v 2"
            subprocess.run(cmd, shell=True, check=True, text=True, stdout=subprocess.PIPE)

if __name__ == '__main__':
    run()