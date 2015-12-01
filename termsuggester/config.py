"""Configuration file-related functions for Sherlock concept search"""

try:
    from ConfigParser import SafeConfigParser, Error
except:
    from configparser import SafeConfigParser, Error

import os


def read_config_file():
    """Reads the configuration file, which is in Windows INI-style format

    Try .termsuggesterrc and termsuggesterrc in the current directory,
    and then ~/.termsuggester/termsuggesterrc
    """
    CONFIG = SafeConfigParser(allow_no_value=True)

    # Try reading files in the current directory first
    files_read = CONFIG.read(['.termsuggesterrc', 'termsuggester'])

    # Read the config file in the home directory
    if len(files_read) == 0:
        CONFIG.read(os.path.expanduser("~/.termsuggester/termsuggesterrc"))

    return CONFIG


conf = read_config_file()


def get_word2vec_model():
    try:
        return conf.get('word2vec', 'path')
    except Error:
        return os.path.expanduser('~/.termsuggester/word2vec.model')
