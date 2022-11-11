from datetime import datetime


def screen(driver, title):
    try:
        dt = datetime.now()
        driver.save_screenshot(
            'reports/screenshots/' + str(dt).replace(" ", "_").replace(":", "").replace(".", "_").replace("-",
                                                                                                          "_") + title + '.png')
    except Exception as err:

        print(f"Error  Insert_cms_generali_api_header_log {err=}, {type(err)=}")
