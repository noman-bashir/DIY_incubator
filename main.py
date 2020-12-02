from incubator import Incubator


if __name__ == "__main__":
    config_file_name = "configs.json"
    trace_number = 0 
    incubator = Incubator(config_file=config_file_name)
    incubator.run_temperature_trace(trace_number=trace_number)