import os

import urllib
import regex
import zipfile

#

def download_webdriver(webdriver_path: str) -> None:
    zip_file = _exe_to_zip(webdriver_path)
    zip_path = _exe_to_folder(webdriver_path)

    urllib.request.urlretrieve("https://chromedriver.storage.googleapis.com"
                               "/2.41/chromedriver_win32.zip",
                               zip_file)    
    with zipfile.ZipFile(zip_file, 'r') as chromedriver_zip:
        chromedriver_zip.extractall(zip_path)
    os.remove(zip_file)


def _exe_to_zip(exe_path: str) -> str:
    zip_path = regex.sub(r'(?<=chromedriver\.)exe', 'zip', exe_path)
    return zip_path


def _exe_to_folder(exe_path: str) -> str:
    zip_folder = regex.sub(r'(?<=\\)\w+\.\w+$', '', exe_path)
    return zip_folder
