import os
import subprocess

def main():

    # Windows
    #dir_path = "..\\digital_lib_scraper\\digital_lib_scraper\\spiders"
    # UNIX type
    dir_path = "../digital_lib_scraper/digital_lib_scraper/spiders"
    files = os.listdir(dir_path)

    for file in files:
        if "_" in file:
            continue
        #result = subprocess.run("scrapy runspider " + dir_path + "\\" + file, shell=True, check=True, text=True, stdout=subprocess.PIPE)
        result = subprocess.run("scrapy runspider " + dir_path + "/" + file, shell=True, check=True, text=True, stdout=subprocess.PIPE)

if __name__ == '__main__':
    main()