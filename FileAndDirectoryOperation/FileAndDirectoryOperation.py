""" Module serving common file and folder operations """
import os
import shutil


class FileAndDirectoryOperation:
    def __init__(self):
        """
        Class constructor method
        """
        pass

    @staticmethod
    def copy_file_object(src: str, dst: str) -> bool:
        """
        Copy a given file or directory, based on th source and destination paths
        :param src: String containing the source file or directory to be copied
        :param dst: String containing the destination where the file or directory will be copied
        :return: Boolean indicating the status of the copy operation
        """
        try:
            if os.path.isfile(src):
                shutil.copy(src=src, dst=dst)
            else:
                shutil.copytree(src=src, dst=dst)
                return True
        except OSError:
            return False

    @staticmethod
    def rename_file_object(file_object: str, new_file_object: str) -> bool:
        """
        Rename the specified file or directory with the give new name
        :param file_object: String containing the path to the file or directory to be renamed
        :param new_file_object: String containing the new name of the file object that needs to be renamed
        :return: Boolean indicating the status of the rename operation
        """
        try:
            os.rename(file_object, new_file_object)
            return True
        except OSError:
            return False

    @staticmethod
    def remove_file_object(file_object: str) -> bool:
        """
        Remove a given file or directory, based on its path
        :param file_object: String containing the path to the desired file or directory to be removed
        :return: Boolean indicating the status of the remove operation
        """
        try:
            if os.path.isfile(file_object):
                os.unlink(file_object)
            else:
                shutil.rmtree(file_object)
                return True
        except OSError:
            return False


