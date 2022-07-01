import os
import configparser

import simplejson as json

filepath = os.path.abspath(os.path.dirname(__file__))
project_path = os.path.dirname(filepath)

images_path = os.path.join(project_path, 'images')

base_config_path = os.path.join(filepath, 'base.ini')
base_cf = configparser.ConfigParser()
base_cf.read(base_config_path)

dev = 'dev'  # 测试环境
prod = 'prod'  # 正式环境
env = base_cf['base']['env']
cf = configparser.ConfigParser(interpolation=None)
config_path = os.path.join(filepath, env, 'configs.ini')
cf.read(config_path)

"""
业务无关配置
"""

mongodb_config = {
    "host": cf["mongodb"]["host"],
    "port": cf["mongodb"]["port"],
    "user": cf["mongodb"]["user"],
    "password": cf["mongodb"]["password"],
}
