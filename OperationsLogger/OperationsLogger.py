""" Module serving logging event messages from the application """
import logging
import os


class OperationsLogger:
    def __init__(self, logger_file_path: str):
        """
        Class constructor method
        :param logger_file_path: String containing the path to the desired log file
        """
        # Define logger name and create folder structure if necessary
        self._logger_file_path = logger_file_path
        self._logging_format = '[%(asctime)s.%(msec)03d] [%(pathname)s] [%(levelname)s] - %(message)s'
        current_dir = ""
        for item in logger_file_path.split("/"):
            current_dir += item
            if os.path.isfile(current_dir):
                with open(current_dir, 'w+') as f:
                    f.close()
                self._logger_file = item
            elif not os.path.exists(current_dir):
                os.mkdir(current_dir)

        # Define generic logger
        logging.basicConfig(
            filename=self._logger_file,
            level=logging.INFO,
            format=self._logging_format,
            datefmt='%H:%M:%S:',
            handlers=[logging.StreamHandler()]
        )

        # Define console logger
        self._console_logging = logging.StreamHandler()
        self._console_logging.setLevel(logging.INFO)
        self._console_logging.setFormatter(logging.Formatter(self._logging_format))

        # Define file logger with console logger handler
        self._logger_name = logging.getLogger(__name__)
        self._logger_name.addHandler(self._console_logging)

    def log_message(self, message: str, level: int = 20):
        """
        Log an event message from the application, according to its log type (INFO, WARNING, ERROR, DEBUG)
        :param message: String containing the message that needs to be logged
        :param level: Integer containing the log type, as defined in the logging package
        """
        self._logger_name.log(level=level, msg=message)
