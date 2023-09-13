""" Module serving for parallel monitoring of a given folder """
import threading
from OperationsLogger.OperationsLogger import OperationsLogger


class FolderWatchdog:
    def __init__(self, logger: OperationsLogger, source: str):
        """
        Class constructor method
        :param logger: OperationsLogger instance for logging events
        :param source: String containing the folder that needs to be monitored
        """
        self._folder_to_be_monitored = source
        self._monitor_thread = threading.Thread()
        self._logger = logger
        self._list_of_operations = []
        self._is_program_running = True

    def stop_monitoring(self):
        """
        Sets the protected attribute 'is_program_running' to False and collect status of the monitoring thread
        :return:
        """
        self._is_program_running = False
        self._monitor_thread.join()

    def run_monitoring(self):
        """
        Start the monitoring thread
        :return:
        """
        self._monitor_thread.start()

