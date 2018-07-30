# -*- coding: utf-8 -*-

import csv
import json

from converter.logic import format_trades
from errors import TradeAppError

_CSV_FILE = "converter/csv_folders/trades.csv"
_JSON_FILE = "converter/json_folders/results.json"
_ERROR_LOG_FILE = "converter/log/error.log"

def convert():
    try:
        data_list = []
        with open(_CSV_FILE, "r") as csv_file, open(_JSON_FILE, "w") as json_file, \
            open(_ERROR_LOG_FILE, 'w') as error_log_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data_list.append(row)
            formated_data = format_trades(data_list)
            json.dump(formated_data, json_file)
        return formated_data
    except TradeAppError as error:
        error_log_file.write(unicode(error))


if __name__ == "__main__":
    convert()