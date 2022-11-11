import json

from functions import connection
from functions.SendEmail import SendEmail
from datetime import datetime


def UpdateLogClaim(idDatiPrimari, scraping_document_log):
    # if os.getenv('ENVIROMENT_PLACEHOLDER') == 'T':
    #     return False

    try:
        querySelect = ("UPDATE  cms_generali_api_claim_log "
                       "LEFT JOIN cms_statistiche_dati csd on csd.codicewrenetelenco = cms_generali_api_claim_log.codicewrenetelenco"
                       " SET  scraping_documents=1, scraping_document_log=scraping_document_log+%s,scraping_document_time=%s, csd.completo='Completo' "
                       "WHERE csd.codicewrenetelenco = %s ")

        cnx = connection.DB()
        cnx.insert(querySelect, [scraping_document_log, datetime.now(), idDatiPrimari])
    except Exception as err:
        SendEmail('Error SaveinDb UpdateLogClaim ' + str(idDatiPrimari),
                  "Error SaveinDb UpdateLogClaim " + json.dumps(err))
        print(f"Error  UpdateLogClaim {err=}, {type(err)=}")
