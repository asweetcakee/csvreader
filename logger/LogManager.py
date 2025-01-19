import os
import shutil
from tkinter import messagebox

class LogManager:
    def __init__(self, app_name):
        """
        Initializes the LogManager.
        :param app_name: Name of the application, used for the logs folder.
        """
        self.app_name = app_name
        self.logs_folder = self.__get_logs_folder()
    
    def __get_logs_folder(self) -> str:
        """
        Gets the appropriate logs folder path.
        :return: Path to the logs folder.
        """
        logs_folder = os.path.join(os.getenv("LOCALAPPDATA"), self.app_name, "logs")
        os.makedirs(logs_folder, exist_ok=True)  # Ensures the folder exists
        return logs_folder

    def archive_logs(self):
        """
        Retrieves all logs and archive them into a .zip file.
        """
        try:
            archive_name = os.path.join(self.logs_folder, "logs_archive")  # Archive name (without extension)
            shutil.make_archive(archive_name, 'zip', self.logs_folder)  # Create the .zip archive
            messagebox.showinfo("Успех", f"Логи были заархивированы в:\n{archive_name}.zip")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось заархивировать логи:\n{str(e)}")

    def get_logs_folder(self) -> str:
        """
        Gets the path to the logs folder (public method for external use).
        :return: Path to the logs folder.
        """
        return self.logs_folder

    def add_log_file(self, file_name: str, content: str):
        """
        Creates a log file and add content to it.
        :param file_name: Name of the log file.
        :param content: Content to write into the log file.
        """
        try:
            file_path = os.path.join(self.logs_folder, file_name)
            with open(file_path, "a") as log_file:  # Opens in append mode
                log_file.write(content + "\n")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось записать логи:\n{str(e)}")