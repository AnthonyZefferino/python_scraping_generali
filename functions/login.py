import os

from selenium.webdriver.common.by import By
from functions.screenshot import screen


def EcomUser(driver):
    driver.find_element(By.NAME, "Ecom_User_ID").send_keys(os.getenv("USERPORTALEGENERALI"))


def EcomPassword(driver):
    driver.find_element(By.NAME, "Ecom_Password").send_keys(os.getenv("PASSWORDPORTALGENERALI"))


def ClickSubmit(driver):
    if os.getenv('ENVIROMENT_PLACEHOLDER') == 'T':
        screen(driver, '_login')
    driver.find_element(By.XPATH, "//input[@type=\"submit\"]").click()


def LoginSubmit(driver):
    driver.get("https://portaleprofessionisti.generali.it/")
    EcomUser(driver)
    EcomPassword(driver)
    ClickSubmit(driver)
