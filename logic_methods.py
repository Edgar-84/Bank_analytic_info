import json
import os
from datetime import datetime, date

from bs4 import BeautifulSoup

from config import params
from logger_settings import logger
from utils import (
    save_pdf_file,
    get_author,
    send_request,
)


def dump_json(data: dict, json_name: str) -> bool:
    try:
        with open(json_name, "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            return True

    except Exception as ex:
        logger.error(f"Mistake during dump_json: {ex}")
        return False


def save_html_page(url: str,
                   headers: dict,
                   path_save: str) -> bool:
    result = send_request(url=url, headers=headers)
    if result is None:
        return False

    try:
        with open(path_save, 'w', encoding="utf-8") as file:
            file.write(result.text)
            logger.info(f"URL {url} is done to html.page")
            return True

    except Exception as ex:
        logger.error(f"Mistake during save_html_page: {ex}")
        return False


def work_with_page(start_date: datetime,
                   finish_date: datetime,
                   path_page: str,
                   json_name: str) -> bool:
    try:
        with open(path_page) as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        all_news_hrefs = soup.find_all(class_="DescriptionList_list__link__8pnZH")
        hrefs = [params.bank_url + item.get("href") for item in all_news_hrefs]
        all_data = [item.text for item in soup.find_all('dt')]
        all_titles = [item.text for item in soup.find_all('dd')]
        news_info_dict = {}

        for index in range(len(hrefs)):
            document_date = '-'.join(all_data[index].split('.')[::-1])
            logger.debug(f"Check date: {date.fromisoformat(document_date)}, "
                         f"RESULT: {start_date <= date.fromisoformat(document_date) <= finish_date}, {start_date}-{finish_date}")
            if start_date <= date.fromisoformat(document_date) <= finish_date:
                news_info_dict[index + 1] = {
                    "datetime_accessed": "",
                    "language": "In progress...",
                    "document_type": "In progress...",
                    "document_author": "",
                    "document_date": document_date,
                    "document_title": all_titles[index],
                    "document_text": "In progress...",
                    "document_html": src,
                    "document_url": "",
                    "document_pdf_encoded": "In progress...",
                    "document_tables": "In progress...",
                    "href": hrefs[index],
                }

        return dump_json(data=news_info_dict, json_name=json_name)

    except Exception as ex:
        logger.error(f"Mistake during work_with_page: {ex}")
        return False


def get_pdf(json_path: str,
            headers: dict) -> dict:
    try:
        with open(json_path) as file:
            all_press = json.load(file)

        for key, value in all_press.items():
            result = send_request(url=value['href'], headers=headers)
            if result is None:
                raise Exception(f"Didn't find page {value['href']}")

            name_file = os.path.join(params.temp_dir, f"{value['document_title']}")

            with open(f"{name_file}.html", "w", encoding="utf-8") as file:
                file.write(result.text)

            with open(f"{name_file}.html") as file:
                page_info = file.read()

            soup = BeautifulSoup(page_info, "lxml")

            try:
                pdf_href = soup.find(class_="Filelist_filelist__2jzRB").find(class_="link--external").get("href")
                file_name = pdf_href.split('/')[-1]
                save_pdf_file(url_file=pdf_href, save_name=os.path.join(params.results_path, file_name))

            except Exception as ex:
                logger.debug(f"Didn't find PDF file on page, mistake: {ex}")
                pdf_href = ''

            p_tags_info = [item.text for item in soup.find_all('p')]
            author = get_author(p_tags_info)
            author = author if author else ''

            all_press[key]["datetime_accessed"] = datetime.now().isoformat()
            all_press[key]['document_author'] = author
            all_press[key]['document_url'] = pdf_href

            if pdf_href != '':
                all_press[key]['document_html'] = ''

            del all_press[key]['href']

        return all_press

    except Exception as ex:
        logger.error(f"Mistake during get_pdf: {ex}")
        return False
