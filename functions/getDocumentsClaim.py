import calendar, os, shutil, time, mimetypes
import json
from pprint import pprint
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from functions import dbInsertFileClaim
from functions.SendEmail import SendEmail
from functions.dbUpdateImportClaim import UpdateLogClaim


def GetMenuDocumentSinistro(driver, row):
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, "//*[text() = '\n\t\t\t\tRicerca e lavorazione incarichi ']").click()
        driver.find_element(By.NAME, "idIncarico").send_keys(row['idIncarico'])
        driver.find_element(By.NAME, "operazione").click()
        action = ActionChains(driver)
        menu = driver.find_element(By.XPATH, '//*[@id="Stm0p0i4eTX"]')
        action.move_to_element(menu).perform()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="Stm0p2i1eHR"]').click()
        time.sleep(2)
    except Exception as err:
        SendEmail('Error GetMenuDocument' + str(row['codicewrenetelenco']),
                  "Error Unexpected " + str(err) + " " + json.dumps(type(err)))
        print(f"GetMenuDocument  {err=}, {type(err)=}")
    finally:
        GetListDocuemnts(driver, row['directory'], row['codicewrenetelenco'], 'GetMenuDocumentSinistro')
        # pprint('return all documents')
        # pprint(row['idIncarico'])
        # pprint(row)
        # pprint(array_return)


def GetMenuDocumentIncarico(driver, row):
    time.sleep(2)
    try:
        action = ActionChains(driver)
        menu = driver.find_element(By.XPATH, '//*[@id="Stm0p0i4eTX"]')
        action.move_to_element(menu).perform()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="Stm0p2i0eDR"]').click()
        time.sleep(2)
    except Exception as err:
        SendEmail('Error GetMenuDocument' + str(row['codicewrenetelenco']),
                  "Error Unexpected " + str(err) + " " + json.dumps(type(err)))
        print(f"GetMenuDocument  {err=}, {type(err)=}")
    finally:
        GetListDocuemnts(driver, row['directory'], row['codicewrenetelenco'], 'GetMenuDocumentIncarico')


def GetListDocuemnts(driver, directory, codicewrenetelenco, tab):
    try:
        page_source = driver.page_source
        time.sleep(3)
        soup = BeautifulSoup(page_source, features="lxml")
        time.sleep(3)
        table = soup.find('table', attrs={'class': 'elenco'})
        getDocumentList = True
        if (table == None):
            getDocumentList = False
        else:
            print('bbbb')
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            # print(tab)
            # print(rows)
    except Exception as err:
        SendEmail(
            'Error GetListDocuemnts codicewrenetelenco=>' + str(codicewrenetelenco) + ' directory=>' + str(
                directory) + ' tab=>' + str(tab),
            "Error Unexpected " + str(err) + " " + json.dumps(type(err)))
        print(f"Error GetListDocuemnts  {err=}, {type(err)=}")
    finally:
        print('NormalizeListDocumentsNormalizeListDocuments' + str(tab))
        if (getDocumentList):
            return NormalizeListDocuments(driver, rows, directory, codicewrenetelenco)


def NormalizeListDocuments(driver, rows, directory, codicewrenetelenco):
    try:
        data = []
        x = 0
        array_return = []
        # *******************************************************
        # SETTING DIRECTORY FOR LOCAL TEST
        # *******************************************************
        if os.getenv('ENVIROMENT_PLACEHOLDER') != 'T':
            pass
        else:
            directory = os.getenv('MAPFOLDER2')
        # *******************************************************
        for row in rows:
            if x > 0:
                y = 0
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                len_check = len(cols)
                pprint(len_check)
                n = 0
                if len_check == 6:
                    n = -1
                filename: object = cols[1 + n]
                title = cols[2 + n]
                for a in row.find_all('a', href=True):
                    if a.get('href') != None:
                        if y == 0:
                            link = 'https://portaleprofessionisti.generali.it' + a.get('href')
                    file_moved = GetDocumentDownload(driver, link, filename, title, directory, codicewrenetelenco)
                    array_return.append(file_moved)
                    # pprint(array_return)
                    y = y + 1
                data.append([ele for ele in cols if ele])
            x = x + 1
        RevoveInitialFolderDownload(directory)
        # //==========================================================
        # UPDATE cms_statistiche_dati -cms_generali_api_claim_log
        UpdateLogClaim(codicewrenetelenco, json.dumps(array_return))
        return array_return
    except Exception as err:
        SendEmail('Error NormalizeListDocuments codicewrenetelenco=>' + str(codicewrenetelenco),
                  "Error Unexpected " + str(err))
        print(f"Error NormalizeListDocuments{err=}, {type(err)=}")


def GetDocumentDownload(driver, link, filename, title, directory, codicewrenetelenco):
    try:
        file_name, file_extension = os.path.splitext(filename)
        driver.get(link)
        current_gmt = time.gmtime()
        time.sleep(3)
        return FileRenameMove(title + str(calendar.timegm(current_gmt)) + file_extension, os.getenv('MAPFOLDER'),
                              directory, title, codicewrenetelenco)
    except Exception as err:
        SendEmail('Error GetDocumentDownload' + codicewrenetelenco,
                  "Error Unexpected " + str(err) + " " + json.dumps(type(err)))
        print(f"Error GetDocumentDownload {err=}, {type(err)=}")


def FindFile(folder_of_download, n):
    try:
        filename = max([f for f in os.listdir(folder_of_download)],
                       key=lambda xa: os.path.getctime(os.path.join(folder_of_download, xa)))
        if n < 60:
            if '.part' in filename or '.tmp' in filename or '.crdownload' in filename:
                time.sleep(1)
                filename = FindFile(folder_of_download, n + 1)
        return filename
    except Exception as err:
        print(f"Error FindFile {err=}, {type(err)=}")


def FileRenameMove(newname, folder_of_download, directory, title, codicewrenetelenco):
    try:
        time.sleep(2)
        filename = FindFile(folder_of_download, 0)
        os.rename(os.path.join(folder_of_download, filename), os.path.join(directory, newname))

        mime = DetectMimeType(os.path.join(directory, newname))
        # print("mime- DetectMimeType ", str(mime[0]))
        dbInsertFileClaim.SaveinDb(title, codicewrenetelenco, newname, str(mime[0]))
        return newname
    except Exception as err:
        SendEmail('Error FileRenameMove' + codicewrenetelenco,
                  "Error Unexpected " + str(err) + " " + json.dumps(type(err)))
        print(f"Error  FileRenameMove {err=}, {type(err)=}")


def RevoveInitialFolderDownload(dir_paht):
    if os.getenv('ENVIROMENT_PLACEHOLDER') == 'T':
        return False
    shutil.rmtree(dir_paht)
    os.makedirs(dir_paht, 0o777)


def DetectMimeType(path):
    # print("DIRECTORY- DetectMimeType ", path)
    return list(mimetypes.guess_type(path))
