import os
import configparser

config = configparser.ConfigParser()
proj_dir = os.getcwd()
config["DEFUALT"] = {"proj_dir":proj_dir}

with open('config.ini','w') as file:
    config.write(file)