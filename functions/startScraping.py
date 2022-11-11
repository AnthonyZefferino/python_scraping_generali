from datetime import datetime
import json
from selenium.webdriver.common.by import By
from functions.SendEmail import SendEmail
from functions import login, queryClaims, getDocumentsClaim
from functions.dbHeaderLogScraping import Insert_cms_generali_scraping_header_log
from functions.screenshot import screen


def Startscraping(driver):
    print('start')
    # //===========================================================================
    # // DETECT CLAIMS NOT SCRAPED (idIncarico,codicewrenetelenco,directory)
    # //===========================================================================
    try:
        results = queryClaims.QueryClaimsToIterate()
        print(results)
    except Exception as err:
        # print('NUMERO DI PRATICHE DA EFFETTUARE SCRAPING <=10 (LIMIT): ' + str(len(results)))
        screen(driver, '_ErrorQueryClaimsToIterate')
        SendEmail('Error queryClaims.QueryClaimsToIterate ', "Error  Unexpected " + str(err))
        print(f"Error queryClaims.QueryClaimsToIterate Unexpected {err=}, {type(err)=}")
    finally:
        if len(results) > 0:
            try:
                login.LoginSubmit(driver)
            except Exception as err:
                screen(driver, '_ErrorLoginSubmit')
                SendEmail('Error login.LoginSubmit',
                          "Error Unexpected " + str(err))
                print(f"Error login.LoginSubmit {err=}, {type(err)=}")
            finally:
                data_start = datetime.now()
                for row in results:
                    try:
                        driver.find_element(By.CSS_SELECTOR, "input[value=\"Incarichi\"]").click()
                    except Exception as err:
                        screen(driver, '_ErrorinputIncarichi')
                        SendEmail('Error find_element(By.CSS_SELECTOR input.Incarichi',
                                  "Error Unexpected " + str(err))
                        print(f"Error find_element(By.CSS_SELECTOR input.Incarichi  {err=}, {type(err)=}")
                    finally:
                        try:
                            print('getDocumentsClaim.GetMenuDocument')
                            getDocumentsClaim.GetMenuDocumentSinistro(driver, row)
                        except Exception as err:
                            print(f"Error getDocumentsClaim.GetMenuDocumentSinistro {err=}, {type(err)=}")
                            screen(driver, '_ErrorGetMenuDocumentSinistro')
                            SendEmail(
                                'Error getDocumentsClaim.GetMenuDocumentSinistro' + str(row['codicewrenetelenco']),
                                "Error Unexpected " + str(err))
                        finally:
                            try:
                                getDocumentsClaim.GetMenuDocumentIncarico(driver, row)
                            except Exception as err:
                                print(f"Error getDocumentsClaim.GetMenuDocumentIncarico {err=}, {type(err)=}")
                                screen(driver, 'GetMenuDocumentIncarico')
                                SendEmail(
                                    'Error getDocumentsClaim.GetMenuDocumentIncarico' + str(row['codicewrenetelenco']),
                                    "Error Unexpected " + str(err))

            results = json.dumps(results)

            data_end = datetime.now()
            Insert_cms_generali_scraping_header_log(data_start, data_end, results)
        else:
            print('Nessun Sinistro da Elaborare')
