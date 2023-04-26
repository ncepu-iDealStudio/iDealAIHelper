import os
import shutil
import yaml

from configparser import ConfigParser
from urllib import parse

config_file = os.path.join(os.path.dirname(__file__), "config.conf")


class Config:

    def __init__(self):
        self.configparser = ConfigParser()
        self.configparser.read(os.path.join(config_file), encoding='utf-8')

    # 读取配置文件，以字典的方式存储
    def get(self):
        # option_to_section的映射
        self.option_to_section = {}
        # 配置文件的键值对
        self.config_dict = {}

        for section in self.configparser.sections():
            for option in self.configparser.options(section):
                self.option_to_section[option] = [section]
                self.config_dict[option] = self.configparser.get(section, option)
                if self.config_dict[option] == "true" \
                        or self.config_dict[option] == "True" \
                        or self.config_dict[option] == "TRUE":
                    self.config_dict[option] = True
                if self.config_dict[option] == "false" \
                        or self.config_dict[option] == "False" \
                        or self.config_dict[option] == "FALSE":
                    self.config_dict[option] = False
                if option == 'port':
                    self.config_dict[option] = int(self.config_dict[option])
                if option == 'jwt_lifetime_seconds':
                    self.config_dict[option] = int(self.config_dict[option])
                if option == 'cookie_max_age':
                    self.config_dict[option] = int(self.config_dict[option])

        return self.config_dict

    def set(self, key, value):
        self.config_dict[key] = value

    def save(self):
        for option in self.config_dict.keys():
            self.CONFIG.set(self.option_to_section[option], option, str(self.config_dict[option]))
        with open(config_file, 'w') as configfile:
            self.CONFIG.write(configfile)
