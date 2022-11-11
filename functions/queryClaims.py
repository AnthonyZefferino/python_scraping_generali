from functions import connection


def QueryClaimsToIterate():
    querySelect = ("SELECT idIncarico,csd.codicewrenetelenco,csd.directory FROM cms_generali_api_claim_log "
                   "LEFT JOIN  cms_statistiche_dati csd "
                   "ON cms_generali_api_claim_log.codicewrenetelenco = csd.codicewrenetelenco "
                   "WHERE  scraping_documents IS NULL "
                   "AND  closed_portalweb IS NULL "
                   "ORDER BY id "
                   "LIMIT %s, %s")
    cnx = connection.DB()

    return cnx.query(querySelect, [0, 10]).fetchall()
