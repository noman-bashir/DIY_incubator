import datetime
import time
import json
import pandas as pd
from temperature import Temperature


class Incubator:
    def __init__(self, config_file: str):
        self.configs = json.load(open(config_file))
        self.temperature_controller = Temperature(config_file) 


    def _wait_until(self, next_timestamp=0):
        while datetime.datetime.now() < next_timestamp:
            time.sleep(0.01)
        return next_timestamp


    def _read_temperature_trace(self, trace_number=0):
        temperature_trace_file_path = self.configs[
            "temperature_trace_path"
        ] + "trace{trace_number}.csv".format(trace_number=trace_number)
        temperature_trace_data = pd.read_csv(temperature_trace_file_path, header=None)
        temperature_trace_data.columns = ["time_in_seconds", "temp_in_C"]
        return temperature_trace_data


    def run_temperature_trace(self, trace_number=0):
        temperature_trace = self._read_temperature_trace(trace_number=trace_number)
        trace_time_granularity_sec = self.configs["trace_time_granularity_sec"]
        temperature_scale = self.configs["temperature_scale"]

        last_timestamp = datetime.datetime.now()
        for _, row in temperature_trace.iterrows():

            self.temperature_controller.set_temperature(setpoint=row["temp_in_C"], scale=temperature_scale)

            last_timestamp = self._wait_until(
                next_timestamp=last_timestamp
                + datetime.timedelta(seconds=trace_time_granularity_sec)
            )

