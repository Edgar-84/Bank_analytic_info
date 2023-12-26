import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Params:
    temp_dir: str
    logs_path: str
    temporary_html_all_press: str
    temporary_json_all_press: str
    headers: dict
    pause_before_request: float
    bank_url: str
    errors_during_work: list
    results_path: str
    time_start_script: str
    document_types: dict


base_dir = Path(__file__).resolve().parent

temp_dir = os.path.join(base_dir, "Temp")
logs_path = os.path.join(base_dir, "logs")
temporary_html_all_press = os.path.join(temp_dir, "temporary_html_all_press.html")
temporary_json_all_press = os.path.join(temp_dir, "temporary_json_all_press.json")
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}
pause_before_request = 0.1
bank_url = "https://www.eestipank.ee"
errors_during_work = []
results_path = os.path.join(base_dir, "results")
time_start_script = datetime.now().isoformat()
document_types = {
    "PRESS_RELEASE": "https://www.eestipank.ee/press/majanduskommentaarid/",
}

params = Params(temp_dir, logs_path, temporary_html_all_press, temporary_json_all_press, headers, pause_before_request,
                bank_url, errors_during_work, results_path, time_start_script, document_types)
