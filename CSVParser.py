import chardet
import pandas as pd
#from tabulate import tabulate
from prettytable import PrettyTable


# Constructor receives file_path as a param
class CSVParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def read_csv(self):
        """Reads the CSV file with automatic encoding and delimiter detection."""
        try:
            # Detects the delimiter
            delimiter = self._detect_delimiter(self.file_path)
            print(f"Обнаружен разделитель: '{delimiter}'")

            # Try reading the file with UTF-8 encoding
            self.data = pd.read_csv(self.file_path, sep=delimiter, encoding='utf-8', on_bad_lines='skip')
            print(f"Файл прочитан с кодировкой: UTF-8")
        except UnicodeDecodeError:
            print("Ошибка при чтении с кодировкой UTF-8. Применяем автоопределение кодировки...")
            
            # Detects encoding and re-reads the file
            encoding = self._detect_encoding(self.file_path)
            print(f"Обнаруживаем кодировку: {encoding}")
            delimiter = self._detect_delimiter(self.file_path)
            self.data = pd.read_csv(self.file_path, sep=delimiter, encoding=encoding, on_bad_lines='skip')
            print(f"Файл прочитан с кодировкой: {encoding}")

    def _detect_encoding(self, file_path):
        """Detects the encoding of the CSV file using chardet."""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']
    
    def _detect_delimiter(self, file_path):
        """Detects the delimiter used in the CSV file."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline()
        # Common delimiters to check
        delimiters = [',', ';', '\t', '|']
        for delim in delimiters:
            if delim in first_line:
                return delim
        # Default to comma if no common delimiter is found
        return ','
    
    def get_columns(self):
        """Returns columns list and first 3 entries"""
        # if self.data is None:
        #     raise ValueError("CSV file is not uploaded.")
        # return {col: self.data[col].head(3).tolist() for col in self.data.columns}
        
        # preview = self.data.head(3)
        # #result = tabulate(preview, headers='keys', tablefmt='grid', showindex=False)
        # result = tabulate(preview, headers='keys', tablefmt='grid', showindex=False, numalign="right")
        # print(result)
        preview = self.data.head(3)
    
        # Initilizes PrettyTtable lib
        table = PrettyTable()
        table.field_names = preview.columns.tolist()
    
        # Fills in the data
        for row in preview.values:
            table.add_row(row)
        print(table)

    def get_unique_regions(self, region_column):
        """Returns unique regions from a selected column"""
        if self.data is None:
            raise ValueError("CSV file is not uploaded.")
        return self.data[region_column].str.upper().unique().tolist()
