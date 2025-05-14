import requests
from typing import Dict, Any

from utils import logger


def fetch_data(vendor: str, headers: dict, params: dict) -> Dict[str, Any]:
    response = requests.post(vendor, headers=headers, params=params)
    logger.info(f'Fetching data: {response.url}')
    if response.status_code == 200:
        data = response.json()
    else:
        # error is of content-type: text/html; charset=utf-8
        raise Exception(f'An error has occurred with status {response.status_code}. '
                        f'Please find the details: {response.text}')
    return data

