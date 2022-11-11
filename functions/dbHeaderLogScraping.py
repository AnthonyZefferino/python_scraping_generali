from functions import connection
from functions.SendEmail import SendEmail


def Insert_cms_generali_scraping_header_log(data_start, data_end, results):
    try:
        querySelect = ("INSERT INTO   cms_generali_scraping_header_log "
                       " (`data_start`, `data_end`, `results`) "
                       "VALUES (%s, %s, %s)")

        cnx = connection.DB()
        cnx.insert(querySelect, [data_start, data_end, results])
    except Exception as err:
        SendEmail('Error Insert_cms_generali_api_header_log' + data_start,
                  "Error Insert_cms_generali_api_header_log {err=}, {type(err)=}")
        print(f"Error  Insert_cms_generali_api_header_log {err=}, {type(err)=}")
