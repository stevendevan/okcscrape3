import os

import urllib
import regex
import zipfile

#

def download_webdriver(root_path: str) -> None:
    zip_file_name = "chromedriver.zip"

    urllib.request.urlretrieve("https://chromedriver.storage.googleapis.com"
                               "/2.41/chromedriver_win32.zip",
                               root_path + '\\' + zip_file_name)    
    chromeDriverZip = zipfile.ZipFile(root_path + '\\' + zip_file_name, 'r')
    chromeDriverZip.extractall(root_path)
    chromeDriverZip.close()
    os.remove(root_path + '\\' + zip_file_name)
