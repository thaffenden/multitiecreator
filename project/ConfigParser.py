from os.path import abspath
from yaml import load


def _read_config_file(file_path):
    """
    Reads the contents of a specified YAML config file.
    :param file_path:
    :return:
    """
    with open(file_path, "r") as yaml_config:
        file_contents = load(yaml_config)
        return file_contents


class WindowConfig(object):
    """
    Reads values from the window_settings.yml config file to set the values
    for window creation.
    """
    def __init__(self):
        self.config_file = abspath("./config/window_settings.yml")

    def read_config(self):
        return _read_config_file(self.config_file)


class ProviderList(object):
    """
    Reads the provider names from the providers.yml file.
    """
    def __init__(self):
        self.config_file = abspath("./config/providers.yml")

    def read_config(self):
        return _read_config_file(self.config_file)


class PlanTypesList(object):
    """
    Reads the provider names from the providers.yml file.
    """
    def __init__(self):
        self.config_file = abspath("./config/plan_types.yml")

    def read_config(self):
        return _read_config_file(self.config_file)
