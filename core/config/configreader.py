import pickle
import os


class ConfigurationReader:
    """
    This class is for reading Configuration of the program.

    Attributes:
        __conf_record (dict): Configuration Dictionary
        mode (int): Sets mode of the program
        start_time (int): Start Time of the analysis
        end_time (int): End Time of the Analysis
        out_dir (str): Default path for output
        debug (bool): Sets Debug Mode
        url_can (bool): Sets URL Canonicalization
        tlangs (list): List of Twitter languages
        dbname (str): Database Name
        tdomain (list): List of Twitter Domains
        tpath (list): List of Twitter paths
        backup_logs (bool): Back Up Logs
    """
    def __init__(self, db_config=None):
        """
        This is the constructor for ConfigurationReader class.

        Parameters:
            db_config (str): Name of Configuration File
        """
        if not db_config:
            self.db_config = "followercount"
        with open(os.path.join(os.path.dirname(__file__), "data", self.db_config), "rb") as self.__ofile:
            self.__conf_record = pickle.load(self.__ofile)
            self.start_time = self.__conf_record["Start_Timestamp"]
            self.end_time = self.__conf_record["End_Timestamp"]
            self.out = self.__conf_record["Output_Dir"]
            self.debug = self.__conf_record["Debug_Mode"]
            self.tlangs = self.__conf_record["Twitter_Languages"]
            self.dbname = self.__conf_record["Database"]
            self.tdomain = self.__conf_record["Twitter_Domain"]
            self.tpath = self.__conf_record["Twitter_Path"]
            self.turl = self.__conf_record["Twitter_Url"]
            self.frequency = self.__conf_record["Frequency"]
            self.intermediate = self.__conf_record["Internediary_Dir"]