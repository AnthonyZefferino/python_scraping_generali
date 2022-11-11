import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
from bs4 import BeautifulSoup
import time
import calendar


def Wait(driver, row):

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[text() = '\n\t\t\t\tRicerca e lavorazione incarichi ']")).click())

    except Exception as err:
        print(f"Ricerca e lavorazione incarichi - Unexpected {err=}, {type(err)=}")
    finally:
        driver.find_element(By.NAME, "idIncarico").send_keys(row['idIncarico'])


