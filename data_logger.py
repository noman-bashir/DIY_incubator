import logging
import datetime


class DataLogger:
    def __init__(self, file_name_str: str, add_timestamp: bool = True):
        if add_timestamp == True:
            file_name = (
                "logged_data/"
                + "{utc_time}".format(utc_time=int(datetime.datetime.now().timestamp()))
                + "_"
                + file_name_str
            )
        else:
            file_name = "logged_data/" + file_name_str

        logging.basicConfig(
            filename=file_name,
            filemode="w",
            level=logging.INFO,
            format="%(asctime)s,%(message)s",
            datefmt="%d-%m-%y %H:%M:%S",
        )

    def log_data(self, data: str):
        logging.info("{data_string}".format(data_string=data))
