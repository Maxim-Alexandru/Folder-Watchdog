""" Module serving the synchronization process between two folders """
import os
import checksum
from typing import List, Any
from FolderWatchdog.FolderWatchdog import FolderWatchdog
from OperationsLogger.OperationsLogger import OperationsLogger


class FolderSynchronizer:
    def __init__(self, source: str, replica: str, logger: OperationsLogger, period: int):
        """
        Class constructor method
        :param source: String containing the path to the folder that needs to be monitored
        :param replica: String containing the path to the folder that needs to be synchronized
        :param logger: OperationsLogger instance for logging events
        :param period: Integer containing the synchronization period in seconds
        """
        self._source_folder = source
        self._replica_folder = replica
        self._current_source_folder_structure = []
        self._logger = logger
        self._synchronization_period = period
        self._is_program_running = True
        self._folder_watchdog = FolderWatchdog()

    def stop_synchronization(self):
        """
        Sets the protected attribute 'is_program_running' to False
        """
        self._is_program_running = False

    def parse_source_folder_tree(self):
        """
        Parse the content of the source folder and extract each individual element
        :return:
        """
        message = f"Parsing monitored source folder {self._source_folder}"
        self._logger.log_message(message=message)
        try:
            for root, _, files in os.walk(self._source_folder):
                self.add_current_folder_tree_to_list(root, files)
            message = "Parsing complete!"
            self._logger.log_message(message=message)
            self.run_synchronization()
        except RuntimeError as e:
            level = 40
            message = f"An error occurred when parsing the source folder: {e}"
            self._logger.log_message(message=message, level=level)

    def add_current_folder_tree_to_list(self, current_dir: str, files: List[str]):
        """
        Add the current folder and its files to the internal list of a FolderSynchronizer object
        :param current_dir: String containing the path to the current directory that it's parsed
        :param files: List containing the name of the files from the current directory
        :return:
        """
        dir_item = {
            current_dir: {
                "hash": self._calculate_hash_for_file_object(current_dir),
                "files": []
            }
        }
        for file in files:
            path_to_file = current_dir + '/' + file
            message = f"Found file: {path_to_file}"
            self._logger.log_message(message=message)
            file_item = {
                file: self._calculate_hash_for_file_object(path_to_file)
            }
            dir_item[current_dir]["files"].append(file_item)
        self._current_source_folder_structure.append(dir_item)

    @staticmethod
    def _calculate_hash_for_file_object(file_object: str) -> Any:
        """
        Calculate the corresponding hash value for the given file or directory
        :param file_object: String containing the path to the file or directory that needs its hash to be calculated
        :return: The corresponding hash string for the file object
        """
        if os.path.isfile(file_object):
            return checksum.get_for_file(fp=file_object)
        return checksum.get_for_directory(dp=file_object)

    def run_synchronization(self):
        """
        Method that deals with the synchronization operations on the replica folder
        :return:
        """
        try:
            ...
        finally:
            self.stop_synchronization()
