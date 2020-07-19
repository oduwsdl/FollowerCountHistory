import pickle
import configparser
import os


class ConfigurationWriter:
    """
    This class is for writing Configuration of the program

    Attributes:
        __config (ConfigParser): ConfigParser object
        __conf_path (str): Path to configuration file
        __conf_record (dict): Stores configuration dictionary
    """

    def __init__(self, **kwargs):
        """
        This is constructor for ConfigurationWriter class

        Parameters:
            kwargs(list): Variable argument for configuration
        """
        self.__config = configparser.ConfigParser()
        self.__conf_path = os.path.join(os.path.dirname(__file__), "data")
        if len(self.__config.read(os.path.join(self.__conf_path, "config.ini"))) == 0:
            self.__config.read(os.path.join(self.__conf_path, "config.ini"))
        self.__conf_record = dict(Start_Timestamp=kwargs.get('sttime', int(self.__config['SETUP']['START_TIMESTAMP'])),
                                  End_Timestamp=kwargs.get('sttime', int(self.__config['SETUP']['END_TIMESTAMP'])),
                                  Mode=kwargs.get('mode', int(self.__config['SETUP']['MODE'])),
                                  Output_Dir=kwargs.get('out_dir', self.__config['SETUP']['OUTPUT_DIR']),
                                  Log_Dir=kwargs.get('log_dir', self.__config['SETUP']['LOG_DIR']),
                                  URL_Canonicalization=kwargs.get("url_can", True
                                  if self.__config['SETUP']['URL_CANONICALIZATION'] == "True" else False),
                                  Database=kwargs.get("db_conf", "deletedtweets"),
                                  Debug_Mode=kwargs.get("debug", True if self.__config['SETUP']['DEBUG_MODE'] == "True"
                                  else False),
                                  Twitter_Languages=self.__config['TWITTER']['LANGUAGES'].split(" "),
                                  Twitter_Domain=self.__config['TWITTER']['DOMAIN'].split(" "),
                                  Twitter_Path=self.__config['TWITTER']['PATH'],
                                  Twitter_Url=self.__config['TWITTER']['URL'],
                                  Backup_Logs=self.__config['SETUP']['BACKUP_LOGS'])
        with open(os.path.join(self.__conf_path, self.__conf_record["Database"]), "wb") as ofile:
            pickle.dump(self.__conf_record, ofile)
