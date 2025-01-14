import os
import logging
from parser.CSVParser import CSVParser
from processor.DataProcessor import DataProcessor
from writer.ExcelWriter import ExcelWriter
from logger.TimeLoggerExcel import TimeLoggerExcel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataProcessorManager:
    def __init__(self, result_folder: str = "result"):
        self.csv_parser: CSVParser | None = None
        self.data_processor: DataProcessor | None = None
        self.time_logger = TimeLoggerExcel()
        self.file_rows: int = 0
        self.total_rows: int = 0
        self.file_title: str = ""
        self.FTD: str = ""
        
        # CONSTANTS
        self.TIME_LOGGER_PARSING = "parsing"
        self.TIME_LOGGER_PROCESSING = "processing"
        self.TIME_LOGGER_WRITING = "writing"
        
        # Result folder initialization
        self.result_folder = result_folder
        os.makedirs(self.result_folder, exist_ok=True)

    def load_csv(self, file_path: str, required_headers: list[str]) -> str:
        """
        Loads a CSV file, validates headers, and returns a preview of the data.
        :param file_path: Path to the CSV file.
        :param required_headers: List of required headers to validate.
        :return: A string representation of the preview (first 3 rows) for TextBox.
        """
        try:
            logging.info("Начинаем загрузку CSV файла.")
            
            # Starts the time logger for parsing
            self.time_logger.start_timer(self.TIME_LOGGER_PARSING)
            
            # Loads and displays CSV preview
            self.csv_parser = CSVParser(file_path)
            self.csv_parser.read_csv()
            
            # Stops the time logger for parsing
            self.time_logger.stop_timer(self.TIME_LOGGER_PARSING)
            
            # Validates headers
            if not self.__validate_headers(required_headers):
                raise ValueError(f"Файл не содержит обязательных колонок: {', '.join(required_headers)}")
            
            # Updates file metadata
            self.file_rows = self.csv_parser.get_rows_quantity()
            self.file_title = self.csv_parser.get_file_name()

            # Returns first 3 entries preview
            return self.csv_parser.get_columns()
        except Exception as e:
            logging.error(f"Ошибка загрузки CSV файла: {e}")
            raise
    
    def load_csv_manual(self, file_path: str) -> dict[str, list[str]]:
        """
        Loads the CSV file and determines eligible columns for manual processing.
        """
        try:
            logging.info("Начинаем загрузку CSV для ручной обработки.")
            
            # Starts the time logger for parsing
            self.time_logger.start_timer(self.TIME_LOGGER_PARSING)
            
            # Loads and displays CSV preview
            self.csv_parser = CSVParser(file_path)
            self.csv_parser.read_csv()
            
            # Stops the time logger for parsing
            self.time_logger.stop_timer(self.TIME_LOGGER_PARSING)
            
            if self.csv_parser.data is None or self.csv_parser.data.empty:
                raise ValueError("CSV file is empty or not loaded.")
            
            # Analyzes the first 5 rows for eligible columns
            first_rows = self.csv_parser.data.head(5)
            columns = first_rows.columns.tolist()

            eligible_countries = []
            eligible_phones = []

            for col in columns:
                if self.__is_eligible_country_column(first_rows[col]):
                    eligible_countries.append(col)
                if self.__is_eligible_phone_column(first_rows[col]):
                    eligible_phones.append(col)

            return {
                "eligible_countries": eligible_countries,
                "eligible_phones": eligible_phones
            }
        except Exception as e:
            logging.error(f"Ошибка загрузки CSV файла для ручной обработки: {e}")
            raise

    def __is_eligible_country_column(self, column_data) -> bool:
        """
        Checks if a column is eligible to be a country column.
        """
        try:
            # Drop NaN and check for valid 2-letter country codes
            valid_country_codes = column_data.dropna().str.match(r"^[a-zA-Z]{2}$")
            # Ensure at least 60% of the rows match
            return valid_country_codes.sum() >= len(column_data.dropna()) * 0.6
        except Exception:
            return False

    def __is_eligible_phone_column(self, column_data) -> bool:
        """
        Checks if a column is eligible to be a phone column.
        """
        try:
            valid_phone_numbers = column_data.dropna().str.match(r"^\+?[0-9]{6,15}$")
            return valid_phone_numbers.sum() >= len(column_data) * 0.6  # At least 60% match
        except Exception:
            return False
    
    def __process_ftd_case(self, ftd_column) -> str:
        # Creates a mask for rows with FTD (not null and not empty)
        mask = self.csv_parser.data[ftd_column].notnull() & (self.csv_parser.data[ftd_column] != '')
        self.csv_parser.data = self.csv_parser.data[mask]
        return "FTD_"
    
    def __process_no_ftd_case(self, ftd_column) -> str:
        # Creates a mask for rows without FTD (null or empty)
        mask = self.csv_parser.data[ftd_column].isnull() | (self.csv_parser.data[ftd_column] == '')
        self.csv_parser.data = self.csv_parser.data[mask]
        return "NoFTD_"
    
    def process_data(self, region_column: str, phone_column: str, ftd_column: str, ftd_filter: str):
        """
        Filters and processes data based on the provided FTD filter.
        :param region_column: The column for region codes.
        :param phone_column: The column for phone numbers.
        :param ftd_filter: "FTD" for rows with first deposit times, "No FTD" for rows without.
        """
        try:
            if not self.csv_parser or self.csv_parser.data is None:
                raise ValueError("CSV файл не загружен или пуст.")
            
            # Starts the time logger for processing
            self.time_logger.start_timer(self.TIME_LOGGER_PROCESSING)
            
            # Applies FTD filtering
            if ftd_filter == "FTD":
                self.FTD = self.__process_ftd_case(ftd_column)
            elif ftd_filter == "No FTD":
                self.FTD = self.__process_no_ftd_case(ftd_column)
            else:
                self.FTD = ""

            # Gets unique regions for processing
            unique_regions = self.csv_parser.get_unique_regions(region_column)
            if not unique_regions:
                raise ValueError("Регион для фильтрации не обнаружен.")
            
            # Starts processing
            self.data_processor = DataProcessor(unique_regions[0])
            for row in self.csv_parser.data.itertuples(index=False):
                self.data_processor.process_row(getattr(row, phone_column))
            
            # Stops the time logger for processing
            self.time_logger.stop_timer(self.TIME_LOGGER_PROCESSING)
        except Exception as e:
            logging.error(f"Ошибка обработки данных: {e}")
            raise

    def __reset_values(self):
        logging.info("Значения переменных сброшены.")
        # Resets all variable values
        self.file_path = ""
        self.file_title = ""
        self.csv_parser = None
        self.data_processor = None
        self.FTD = ""
        self.file_rows = 0
        self.total_rows = 0
    
    def write_to_excel(self) -> tuple[str, str]:
        """
        Writes processed data to Excel files and returns the file paths.
        :return: Tuple containing valid and invalid file paths.
        """
        try:
            if not self.data_processor:
                raise ValueError("Нет обработанных данных для записи.")

            # Starts the time logger for writing
            self.time_logger.start_timer(self.TIME_LOGGER_WRITING)
            
            logging.info("Создаем первичные xlsx файлы.")
            valid_writer = ExcelWriter(f"{self.result_folder}/valid_phones.xlsx")
            invalid_writer = ExcelWriter(f"{self.result_folder}/invalid_phones.xlsx")

            # Writes valid and invalid numbers
            valid_writer.write_to_excel(self.data_processor.valid_numbers)
            invalid_writer.write_to_excel(self.data_processor.invalid_numbers)

            # Renames and log file paths
            valid_file_path = self.__rename_file(valid_writer, "val")
            invalid_file_path = self.__rename_file(invalid_writer, "inval")
            
            # Stops the time logger for writing
            self.time_logger.stop_timer(self.TIME_LOGGER_WRITING)

            # Log time in Excel VALID ONLY
            self.time_logger.log(
                file_rows=self.file_rows,
                file_name=self.file_title,
                corrupted=self.csv_parser.is_encoding_corrupted(),
                FTD=self.FTD,
                total_rows=self.total_rows
            )
            
            # Resets all values
            self.__reset_values()
            
            return valid_file_path, invalid_file_path
        except Exception as e:
            logging.error(f"Ошибка записи в Excel: {e}")
            raise

    def __validate_headers(self, required_headers: list[str]) -> bool:
        """
        Validates that the required headers exist in the CSV file.
        :param required_headers: List of required headers.
        :return: True if headers are valid, False otherwise.
        """
        if not self.csv_parser or self.csv_parser.data is None:
            raise ValueError("Данные CSV не загружены.")
        
        actual_headers = self.csv_parser.data.columns.tolist()
        missing_headers = [header for header in required_headers if header not in actual_headers]
        
        logging.info(f"Available headers: {actual_headers}")
        
        if missing_headers:
            logging.error(f"Отсутствующие колонки: {missing_headers}")
            return False
        return True

    def get_available_columns(self) -> list[str]:
        """
        Returns the column names from the loaded CSV.
        :return: List of column names.
        """
        if not self.csv_parser or not self.csv_parser.data:
            raise ValueError("CSV data is not loaded.")
        return self.csv_parser.data.columns.tolist()

    def get_unique_values(self, column_name: str) -> list[str]:
        """
        Returns unique values from the specified column.
        :param column_name: The column to extract unique values from.
        :return: List of unique values.
        """
        if not self.csv_parser or self.csv_parser.data is None or self.csv_parser.data.empty:
            raise ValueError("CSV data is not loaded or is empty.")
        try:
            return self.csv_parser.get_unique_regions(column_name)
        except Exception as e:
            logging.error(f"Error getting unique values from column {column_name}: {e}")
            raise
    
    def __rename_file(self, writer: ExcelWriter, prefix: str) -> str:
        """
        Renames an Excel file with the appropriate prefix and metadata.
        :param writer: ExcelWriter instance.
        :param prefix: Prefix for the filename (e.g., "val" or "inval").
        :return: New file path.
        """
        date = writer.get_date()
        self.total_rows = writer.get_total_rows()
        new_file_name = os.path.join(self.result_folder, f"{self.FTD}{prefix}_{self.file_title}_{date}_{self.total_rows}.xlsx")
        os.rename(writer.output_file, new_file_name)
        logging.info(f"Файл переименован: {writer.output_file} -> {new_file_name}")
        return new_file_name
