import os
import pandas as pd
import logging

from charset_normalizer import from_path
from tabulate import tabulate

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CSVParser:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.data: pd.DataFrame | None = None
        self.chunk_size = 10000

    def read_csv(self):
        """Reads the CSV file in chunks for efficiency with automatic encoding and delimiter detection."""
        try:
            encoding = self.__detect_encoding()
            delimiter = self.__detect_delimiter()
            chunks = self.__read_in_chunks(delimiter, encoding, self.chunk_size)
            self.data = self.__combine_chunks(chunks)
            
        except Exception as e:
            logging.error(f"Ошибка при чтении CSV файла: {e}")
            raise

    def __detect_encoding(self):
        """
        Detects the encoding of the CSV file using charset-normalizer.
        Falls back to 'utf-8' if detection fails.
        """
        try:
            result = from_path(self.file_path).best()
            encoding = result.encoding if result else "utf-8"
            logging.info(f"Обнаружена кодировка: {encoding}")
            return encoding
        except Exception as e:
            logging.warning(f"Ошибка определения кодировки. Применяем 'utf-8'. Ошибка: {e}")
            return "utf-8"
    
    def __detect_delimiter(self):
        """
        Detects the delimiter used in the CSV file by analyzing multiple lines.
        Falls back to ',' if detection fails.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [f.readline() for _ in range(3)]  # Analyzes first 3 lines

            delimiters = [",", ";", "\t", "|"] # Common delimiters
            
            # counts = {',': 25, ';': 10, '\t': 5, '|': 0}
            counts = {delim: sum(line.count(delim) for line in lines) for delim in delimiters}
            detected_delimiter = max(counts, key=counts.get)
            
            if counts[detected_delimiter] > 0:
                logging.info(f"Обнаружен разделитель: '{detected_delimiter}'")
                return detected_delimiter
            else:
                raise ValueError("Ни один правильный разделитель не обнаружен.")
        except Exception as e:
            logging.warning(f"Ошибка обнаружения разделителя. Применяем ','. Ошибка: {e}")
            return ","
    
    def __read_in_chunks(self, delimiter: str, encoding: str, chunk_size: int):
        """Reads the CSV file in chunks for memory efficiency."""
        try:
            logging.info("Приступаем к чтению CSV файла чанками...")
            chunks = pd.read_csv(
                self.file_path,
                sep=delimiter,
                encoding=encoding,
                chunksize=chunk_size,
                on_bad_lines="skip",
                engine="c",
            )
            return chunks
        except Exception as e:
            logging.error(f"Ошибка чтения файла чанками: {e}")
            raise
    
    def __combine_chunks(self, chunks: int) -> pd.DataFrame:
        """Combines the chunks into a single DataFrame."""
        try:
            df = pd.concat(chunks, ignore_index=True)
            logging.info("Успешно удалось соединить чанки в один DataFrame.")
            return df
        except Exception as e:
            logging.error(f"Ошибка объединения чанков в один DataFrame: {e}")
            raise
    
    def get_columns(self) -> str:
        """Returns columns list and first 3 entries"""
        if self.data is None or self.data.empty:
            raise ValueError("Нет данных для отображения. CSV можеть быть пуст или неверно отформатирован.")
        
        preview = self.data.head(3)
        
        # Initialize tabulate
        table = tabulate(preview, headers=preview.columns.tolist(), tablefmt="grid", showindex=False)
        return table

    def get_unique_regions(self, region_column: str) -> list[str]:
        """Returns unique regions from a selected column"""
        if self.data is None or self.data.empty:
            raise ValueError("CSV файл не загружен.")
        return self.data[region_column].str.upper().unique().tolist()

    def get_file_name(self) -> str:
        return os.path.splitext(os.path.basename(self.file_path))[0]