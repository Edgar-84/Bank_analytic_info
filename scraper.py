import os
from datetime import datetime

from config import params
from logger_settings import logger
from logic_methods import (
    save_html_page,
    work_with_page,
    get_pdf,
    dump_json,
)
from utils import delete_files_in_temp, get_finish_result, get_years_period


def validate_search_doc_types(document_types: list) -> bool:
    result = True

    for doc_type in document_types:
        if params.document_types.get(doc_type) is None:
            result = False
            logger.warning(f"You have entered non-existent document types: {document_types},"
                           f"you can use the following types {params.document_types}")

    return result


def run_scrape(start_date: datetime, finish_date: datetime, document_types: list):
    logger.info(f'{"=" * 15} The script starts running! {"=" * 15}')

    if validate_search_doc_types(document_types) is False:
        logger.info(f'{"=" * 15} The script has finished! {"=" * 15}')
        return None

    years = [str(year) for year in get_years_period(start_date, finish_date)]
    work_url = params.document_types.get(document_types[0])
    finish_result = []

    for year in years:
        save_html_page(
            url=work_url + year,
            headers=params.headers,
            path_save=params.temporary_html_all_press,
        )
        work_with_page(
            start_date=start_date,
            finish_date=finish_date,
            path_page=params.temporary_html_all_press,
            json_name=params.temporary_json_all_press,
        )
        result = get_pdf(
            json_path=params.temporary_json_all_press,
            headers=params.headers,
        )

        for _, value in result.items():
            finish_result.append(value)

    finish_data = get_finish_result(
        start_date=start_date.strftime("%d.%m.%Y"),
        end_date=finish_date.strftime("%d.%m.%Y"),
        errors_info=params.errors_during_work,
        successes=finish_result,
    )

    dump_json(
        data=finish_data,
        json_name=os.path.join(params.results_path, 'result.json'),
    )

    delete_files_in_temp()
    logger.info(f'{"=" * 15} The script has finished! {"=" * 15}')

    return finish_data
