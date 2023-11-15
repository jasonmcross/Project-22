import os
import subprocess

def main():

    cur_dir = os.getcwd()
    dir_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir, "digital_lib_scraper", "digital_lib_scraper", "spiders"))
    files = os.listdir(dir_path)

    for file in files:
        if "_" in file:
            continue
        cmd = "scrapy runspider " + dir_path + "/" + file # to check error message: -v 2"
        subprocess.run(cmd, shell=True, check=True, text=True, stdout=subprocess.PIPE)

if __name__ == '__main__':
    main()