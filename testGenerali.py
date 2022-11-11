from datetime import datetime
from pathlib import Path

import json
import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

from functions import SendEmail
from functions import login, queryClaims, getDocumentsClaim
from functions.dbHeaderLogScraping import Insert_cms_generali_scraping_header_log


class TestGenerali:

    @pytest.fixture(autouse=True)
    def browser_setup_and_teardown(self):
        dotenv_path = Path('C:\scraping\scrapingGenerali.env.development')
        load_dotenv(dotenv_path=dotenv_path)

        options = webdriver.ChromeOptions()

        options.add_argument("--window-size=1920,1200")
        options.add_experimental_option("prefs", {
            "download.default_directory": os.getenv('MAPFOLDER'),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "headless": True

        })

        self.browser = webdriver.Chrome(executable_path=os.getenv('CROME_PATH'), chrome_options=options)
        # self.browser.maximize_window()
        self.browser.implicitly_wait(2)

        yield
        # print('*************************************clooooooooose')
        self.browser.close()
        self.browser.quit()

    def test_scraping(self):
        # //===========================================================================
        # // DETECT CLAIMS NOT SCRAPED (idIncarico,codicewrenetelenco,directory)
        # //===========================================================================
        try:
            results = queryClaims.QueryClaimsToIterate()
        except Exception as err:
            # print('NUMERO DI PRATICHE DA EFFETTUARE SCRAPING <=10 (LIMIT): ' + str(len(results)))
            SendEmail('Error queryClaims.QueryClaimsToIterate ', "Error  Unexpected " + str(err))
            print(f"Error queryClaims.QueryClaimsToIterate Unexpected {err=}, {type(err)=}")
        finally:
            if len(results) > 0:
                try:
                    login.LoginSubmit(self.browser)
                except Exception as err:
                    SendEmail('Error login.LoginSubmit',
                              "Error Unexpected " + str(err))
                    print(f"Error login.LoginSubmit {err=}, {type(err)=}")
                finally:
                    try:
                        self.browser.find_element(By.CSS_SELECTOR, "input[value=\"Incarichi\"]").click()
                    except Exception as err:
                        SendEmail('Error find_element(By.CSS_SELECTOR input.Incarichi',
                                  "Error Unexpected " + str(err))
                        print(f"Error find_element(By.CSS_SELECTOR input.Incarichi  {err=}, {type(err)=}")
                    finally:

                        data_start = datetime.now()
                        for row in results:
                            try:
                                getDocumentsClaim.GetMenuDocumentSinistro(self.browser, row)
                            except Exception as err:
                                print(f"Error getDocumentsClaim.GetMenuDocument {err=}, {type(err)=}")
                                SendEmail('Error getDocumentsClaim.GetMenuDocument' + str(row['codicewrenetelenco']),
                                          "Error Unexpected " + str(err))

                        results = json.dumps(results)

                        data_end = datetime.now()
                        Insert_cms_generali_scraping_header_log(data_start, data_end, results)
            else:
                print('Nessun Sinistro da Elaborare')
