import glob
import time
import sys
import datetime
import json
from heating_and_cooling_control import HeatingAndCoolingControl


class Temperature:
    def __init__(self, config_file):
        self.configs = json.load(open(config_file))
        self.heat_controller = HeatingAndCoolingControl(config_file) 

    def _get_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    def _print_stderr(self, *message):
        print(
            self._get_timestamp() + "\t" + "\t".join(message),
            file=sys.stderr,
            flush=True,
        )

    def _read_device_data(self):
        base_directory_path = self.configs["base_directory_path"]

        device_folder_glob = glob.glob(base_directory_path)

        num_devices_found = len(device_folder_glob)
        if num_devices_found != 1:
            self._print_stderr(
                "Found {num_device} matching devices for {base_directory}".format(
                    num_devices=num_devices_found, base_directory=base_directory_path
                )
            )
            exit(1)

        device_file = device_folder_glob[0] + "/w1_slave"

        f = open(device_file, "r")
        lines = f.readlines()
        f.close()
        return lines

    def _read_temperature_in_c(self):
        device_data = self._read_device_data()
        while device_data[0].strip()[-3:] != "YES":
            retry_seconds = 5
            self._print_stderr(
                "Bad crc checksum; retry in {seconds}s".format(seconds=retry_seconds)
            )
            time.sleep(retry_seconds)
            device_data = self._read_device_data()

        temperature_index = device_data[1].find("t=")
        if temperature_index != -1:
            temperature_string = device_data[1][temperature_index + 2 :]
            temperature_C = float(temperature_string) / 1000.0
            return temperature_C
        else:
            self._print_stderr("Temperature data not found on device")
            exit(1)

    def _convert_to_f(self, temperature_in_C):
        return temperature_in_C * 9.0 / 5.0 + 32.0

    def get_temperature(self, scale="C"):
        if scale == "C":
            return self._read_temperature_in_c()
        elif scale == "F":
            return self._convert_to_f(self._read_temperature_in_c())
        else:
            print("Only C and F scales are implemmented")

    def set_temperature(self, setpoint=0, scale="C"):
        setpoint_tolerance = self.configs["setpoint_tolerance"]
        lower_bound = setpoint - setpoint_tolerance
        upper_bound = setpoint + setpoint_tolerance

        current_temperature = self.get_temperature(scale)

        if current_temperature < lower_bound:
            self.heat_controller.turn_ON_heating()
        elif current_temperature > upper_bound:
            self.heat_controller.turn_ON_cooling()
        else:
            pass
