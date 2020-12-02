from gpiozero import LED
import pylights3
import json


class HeatingAndCoolingControl:
    def __init__(self, config_file: str):
        self.configs = json.load(open(config_file))
        self.relay = LED(self.configs["relay_gpio_pin"])
        pylights3.device_cfg_filename = self.configs["device_configs"]
        self.dimmer = pylights3.plm(self.configs["usb_device"])
        self.dimmer_level = self.configs["dimmer_level"]

    def turn_ON_cooling(self):
        self.turn_OFF_heating()
        self.relay.on()


    def turn_OFF_cooling(self):
        self.relay.off()


    def turn_ON_heating(self):
        self.turn_OFF_cooling()
        self.set_dimmer_level(dimmer_setpoint=self.dimmer_level)

    def turn_OFF_heating(self):
        self.set_dimmer_level(dimmer_setpoint=0)

    def set_dimmer_level(self, dimmer_setpoint: int = 0):
        self.dimmer.setLevel("dimmer", self.dimmer_level)