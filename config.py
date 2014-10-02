"""
This was seperated out from mailfetch since other stages will need configuration files too.
I figured we could use one file for everything.
"""
import configparser   # Used to read/write configuration values from/to file
# Uses the configparser module to read configuration variable values from mailfetch.conf
import os
cache = None
config_filename = "mailfetch.conf"

def read_config():
	global cache
	if cache != None:
		return cache
    config = configparser.ConfigParser()
    config.read(config_filename)
    print("Configuration data read from",config_filename,"...")
	cache = config
    return config

	
# Helper function to display config values.
# This function will disappear in the future.
def print_config(config):
    for key in config["Mailfetch"]:
        print(key,config["Mailfetch"][key])
    return 0

# Write current configuration values back to mailfetch.conf
# May or may not be used in the future.
def write_config(config,filename):
    with open(filename,"w") as confFile:
        config.write(confFile)
    print("Configuration data written to",filename,"...")
    return 0