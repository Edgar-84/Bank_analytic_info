import os
import time
from datetime import datetime

import requests
from requests.models import Response

from config import params
from logger_settings import logger


def add_work_error(document_url: str, processing_error: str):
    result = {
        "datetime_accessed": datetime.now().isoformat(),
        "document_url": document_url,
        "processing_error": processing_error,
    }
    params.errors_during_work.append(result)


def send_request(url: str,
                 headers: dict = None,
                 pause: float = params.pause_before_request) -> Response or None:
    """
    Get Response object for url, with pause before requests and repeat
    request if we catch mistake 400 - 599
    """

    mistake_pause = 0
    time.sleep(pause)

    try:
        response = requests.get(url=url, headers=headers)

        if 400 <= response.status_code <= 599:
            while mistake_pause != 600:
                time.sleep(mistake_pause)
                response = requests.get(url=url, headers=headers)
                if 400 <= response.status_code <= 599:
                    mistake_pause += 1
                    continue

                else:
                    return response

            error_message = (f"Catch mistake during load url: {url}, status_code: {response.status_code}"
                             f"mistake: {response.text}")
            logger.error(error_message)
            add_work_error(document_url=url, processing_error=error_message)
            return None

        else:
            logger.info(f"The site {url} has been successfully loaded.")
            return response

    except Exception as ex:
        error_message = f"Catch mistake during load url: {url}, mistake: {ex}"
        logger.critical(error_message)
        add_work_error(document_url=url, processing_error=error_message)
        return None


def save_pdf_file(url_file: str, save_name: str) -> bool:
    response = send_request(url=url_file)
    if response is not None:
        with open(save_name, "wb") as file:
            file.write(response.content)
            return True

    return False


def get_author(data_search: list):
    try:
        phrase_es_page = "Lisateave"
        phrase_en_page = "For further information:"
        filtered_list = list(filter(lambda x: phrase_es_page in x or phrase_en_page in x, data_search))

        if len(filtered_list) == 0:
            logger.debug(f"AUTHOR LIST: {data_search}")
            return None

        result = filtered_list[0].split('\n')[1]
        return result.replace('\t', '')

    except Exception as ex:
        logger.debug(f"Didn't find name author on page, mistake: [{ex}]")
        return None


def delete_files_in_temp():
    for filename in os.listdir(params.temp_dir):
        if filename == '.gitkeep':
            continue

        file_path = os.path.join(params.temp_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as ex:
            logger.error(f"Mistake during delete file: {file_path}, mistake: {ex}")

    logger.info("Clearing of the Temp directory is finished!")


def get_finish_result(start_date: str,
                      end_date: str,
                      errors_info: list,
                      successes: list) -> dict:
    """
    Prepare data for the final report
    """

    result = {
        "metadata": {
            "query_start_date": start_date,
            "query_end_date": end_date,
            "run_start_datetime": params.time_start_script,
            "schema": "v2",
        },
        "errors": errors_info,
        "successes": successes,
    }

    return result


def get_years_period(start_date: datetime, finish_date: datetime) -> list:
    return [year for year in range(start_date.year, finish_date.year + 1)]


def validate_date_period(start_date: datetime, finish_date: datetime, date_to_check: datetime) -> list:
    return start_date <= date_to_check <= finish_date
