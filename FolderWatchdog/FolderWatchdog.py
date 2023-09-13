""" Module serving for parallel monitoring of a given folder """
import os
import threading
from typing import List
from FileAndDirectoryOperation.FileAndDirectoryOperation import FileAndDirectoryOperation
from OperationsLogger.OperationsLogger import OperationsLogger


class FolderWatchdog:
    def __init__(self, logger: OperationsLogger, source: str, folder_content: List[dict], file_and_directory_operations: FileAndDirectoryOperation):
        """
        Class constructor method
        :param logger: OperationsLogger instance for logging events
        :param source: String containing the folder that needs to be monitored
        :param file_and_directory_operations: FileAndDirectoryOperation instance object
        """
        self._folder_to_be_monitored = source
        self._monitor_thread = threading.Thread(target=self._verify_source_folder_for_changes)
        self._logger = logger
        self._previous_folder_content = folder_content
        self._list_of_operations = []
        self._is_program_running = True
        self._common_operations = file_and_directory_operations

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

    def _verify_source_folder_for_changes(self):
        """
        Monitor the source folder for any changes performed on its content,
        until a termination signal is received from the main application
        :return:
        """
        while self._is_program_running:
            generator = list(os.walk(self._folder_to_be_monitored))
            actual_folders = [item[0] for item in generator]
            actual_list_of_files = [item[2] for item in generator]
            actual_hashes = [self._common_operations.calculate_hash_for_file_object(dir_name) for dir_name in actual_folders]

            reference_folder_objects = [item for item in self._previous_folder_content]
            reference_folders = [list(item.keys())[0] for item in reference_folder_objects]
            reference_hashes = [item[dir_name]["hash"] for item, dir_name in zip(reference_folder_objects, reference_folders)]

            # Verify if any directory was removed from the folder
            for r_folder, r_hash in zip(reference_folders, reference_hashes):
                if r_folder not in actual_folders and r_hash not in actual_hashes:
                    operation = {r_folder: "folder removed"}  # Folder was removed
                    self.add_new_operation(operation=operation)
                    self._remove_directory_from_previous_list(folder_object={r_folder: r_hash})

            for a_folder, a_hash, a_files in zip(actual_folders, actual_hashes, actual_list_of_files):
                if a_folder in reference_folders:
                    self._verify_files_from_folder(folder_name=a_folder, actual_files=a_files)
                elif a_hash in reference_hashes:
                    operation = {a_folder: "name changed"}  # Folder name has changed
                    self.add_new_operation(operation=operation)
                else:
                    operation = {a_folder: "new folder added"}  # New folder was added
                    self.add_new_operation(operation=operation)

    def _verify_files_from_folder(self, folder_name: str, actual_files: List[str]):
        """
        Verify if there are any differences for files in a given folder
        :param folder_name: String containing the name of the current folder
        :param actual_files: List containing the name of the files to be verified
        :return:
        """
        folder_object = self._get_folder_item_by_name(folder_name=folder_name)

        reference_file_objects = folder_object[folder_name]["files"]  # E.g., [{file1: hash1}, {file2: hash2}]
        reference_files = [list(r_file.keys())[0] for r_file in reference_file_objects]  # E.g., [file1, file2]
        reference_hashes = [list(r_file.values())[0] for r_file in reference_file_objects]  # E.g.,  [hash1, hash2]

        actual_hashes = [self._common_operations.calculate_hash_for_file_object(file_object=file) for file in actual_files]

        # Verify if any file was removed from the folder
        for r_file, r_hash in zip(reference_files, reference_hashes):
            if r_file not in actual_files and r_hash not in actual_hashes:
                operation = {r_file: "file removed"}  # File was removed
                self.add_new_operation(operation=operation)
                self._remove_file_from_previous_list(folder_name=folder_name, file_object={r_file: r_hash})

        for a_file, a_hash in zip(actual_files, actual_hashes):
            if a_file in reference_files:
                if a_hash in reference_hashes:
                    pass  # No change was performed for the current file
                else:
                    operation = {a_file: "content changed"}  # Content file has changed
                    self.add_new_operation(operation=operation)
            else:
                if a_hash in reference_hashes:
                    operation = {a_file: "name changed"}  # Name of the file was changed
                    self.add_new_operation(operation=operation)
                else:
                    operation = {a_file: "new file added"}  # Added new file
                    self.add_new_operation(operation=operation)

    def add_new_operation(self, operation: dict):
        """
        Add a new operation that was performed to a file or directory
        :param operation: Dictionary containing the name of the file/directory and the type of operation performed
        :return:
        """
        if operation not in self._list_of_operations:
            self._list_of_operations.append(operation)
            for file, change in operation.items():
                message = f"Detected change! {change} for file {file}"
                self._logger.log_message(message=message)

    def _get_folder_item_by_name(self, folder_name) -> dict or None:
        """
        Iterate through the previous folder structure and return the folder dictionary object that has the specified name
        :param folder_name: String containing the name of the folder
        :return: Dictionary containing the item that has as key the name of the specified folder
        """
        for item in self._previous_folder_content:
            dir_name = list(item.keys())[0]
            if dir_name == folder_name:
                return item
        return None

    def _remove_file_from_previous_list(self, folder_name: str, file_object: dict):
        """
        Remove the entry of a file from a given folder, from the internal list
        :param folder_name: String containing the parent folder of the file
        :param file_object: Dictionary containing the name of the file and its corresponding hash value
        :return:
        """
        for index in range(len(self._previous_folder_content)):
            self._previous_folder_content[index][folder_name]["files"].remove(file_object)
            message = f"Removed instance {file_object} from internal list"
            self._logger.log_message(message=message, level=10)

    def _remove_directory_from_previous_list(self, folder_object: dict):
        """
        Remove the entry of a directory, from the internal list
        :param folder_object: Dictionary containing the name of the directory and its corresponding hash value
        :return:
        """
        for index in range(len(self._previous_folder_content)):
            r_name = list(self._previous_folder_content[index].keys())[0]
            a_name = list(folder_object.keys())[0]
            if r_name == a_name:
                del self._previous_folder_content[index]
                message = f"Removed instance {folder_object} from internal list"
                self._logger.log_message(message=message, level=10)
