from pathlib import Path
import os
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from functions.startScraping import Startscraping


def reset_browser():
    if os.getenv('ENVIROMENT_PLACEHOLDER') != 'T':
        browser_exe = "chrome"
        os.system("pkill " + browser_exe)


def Dashboard():
    print('dashboard')

    dotenv_path = Path('C:\scraping\scrapingGenerali.env.development')
    load_dotenv(dotenv_path=dotenv_path)
    reset_browser()
    options = webdriver.ChromeOptions()

    options.add_argument("--window-size=1920,1200")
    # # options.add_argument("--headless")
    options.add_experimental_option("prefs", {
        "download.default_directory": os.getenv('MAPFOLDER'),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "headless": True

    })

    driver = webdriver.Chrome(executable_path=os.getenv('CROME_PATH'), chrome_options=options)
    driver.maximize_window()
    driver.implicitly_wait(2)
    Startscraping(driver)
    # yield
    # # print('*************************************clooooooooose')
    driver.close()
    driver.quit()
