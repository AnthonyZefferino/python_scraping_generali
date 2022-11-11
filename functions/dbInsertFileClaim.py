from functions import connection
from functions.SendEmail import SendEmail
import json

def FindCategory(title):
    querySelect = ("SELECT id FROM cms_generali_tipo_documento "
                   "WHERE  descrizione =%s "
                   "LIMIT %s, %s")
    cnx = connection.DB()

    return cnx.fetch(querySelect, [title, 0, 1])


def InsertDb(name, idDatiPrimari, id_cms_generali_tipo_documento, mime):
    querySelect = ("INSERT INTO  cms_generali_files"
                   " (`name`, `idDatiPrimari`, `id_cms_generali_tipo_documento`, `type`,`insert_scraping`) "
                   "VALUES (%s, %s, %s, %s, '1')")
    cnx = connection.DB()
    cnx.insert(querySelect, [name, idDatiPrimari, id_cms_generali_tipo_documento, mime])


def SaveinDb(title, idDatiPrimari, name, mime):
    try:
        category = FindCategory(title)
        if len(category) == 0:
            id_cms_generali_tipo_documento = 38
        else:
            id_cms_generali_tipo_documento = category[0]['id']

        InsertDb(name, idDatiPrimari, id_cms_generali_tipo_documento, mime)
    except Exception as err:
        SendEmail('Error SaveinDb' + idDatiPrimari,
                  "Error SaveinDb "+json.dumps(err))
        print(f"Error  FileRenameMove {err=}, {type(err)=}")
