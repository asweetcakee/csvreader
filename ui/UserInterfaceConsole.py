from parser.CSVParser import CSVParser
from processor.DataProcessor import DataProcessor
from writer.ExcelWriter import ExcelWriter
from enums.CountriesEnum import CountriesEnum

class UserInterfaceConsole:
    def __init__(self):
        self.csv_parser = None
        self.processed_data = None
        self.excel_writer = None    
        self.region_column = None
        self.phone_column = None
    
    def start(self):
        print("Reading the csv file...")
        self.read_csv()
        
        print("Выберите столбцы, которые содержат код региона и номера:")
        self.select_columns()
        
    def read_csv(self):
        file_path = "at_part_1.csv"
        try:
            self.csv_parser = CSVParser(file_path)
            self.csv_parser.read_csv()
        except Exception as e:
            print("Ошибка", f"Не удалось загрузить файл: {e}")
    
    def select_columns(self):
        self.csv_parser.get_columns()
        
        self.region_column = input("Введите столбец региона: ").strip()
        self.phone_column = input("Введите столбец номера: ").strip()
        
        # Prints unique regions
        self.get_unique_regions(self.region_column)
        
        # Gets selected regions
        selected_regions = self.select_region()
        
        # Processes the data by selected regions
        self.process_data(selected_regions)            
        
    def get_unique_regions(self, region_col):
        unique_regions = self.csv_parser.get_unique_regions(region_col)
        print(f"В этом файле по столбцу {region_col} найдены следующие уникальные регионы:")
        print(", ".join(unique_regions))
    
    def select_region(self):
        selected_input = input("Выберите интересующий вас регион: ").upper()
        
        if "," in selected_input:
            regions = [region.strip() for region in selected_input.split(",")]
        else:
            regions = [selected_input.strip()]
        return regions
                
    def process_data(self, selected_regions):
        self.processed_data = DataProcessor(selected_regions)
                
        # DEBUGGING PURPOSE DELETE ONCE FINISHED
        #self.processed_data.print_details()
        
        # Makes sure self.csv_parser is safe to use and not None
        if self.csv_parser and self.csv_parser.data is not None:
            for _, row in self.csv_parser.data.iterrows():
                self.processed_data.process_row(row[self.phone_column])
            self.write_to_excel()
        else:
            print("Ошибка", "Данные CSV не загружены.")
        
            # for _, row in self.csv_parser.data.iterrows():
            #     self.processor.process_row(str(row[self.region_col]).upper(), str(row[self.phone_col]).upper())
            # self.write_to_excel()
        
    def write_to_excel(self):
        writer_valid = ExcelWriter("valid_phones.xlsx")
        writer_invalid = ExcelWriter("invalid_phones.xlsx") 
        writer_valid.write_to_excel({**self.processed_data.valid_numbers})
        writer_invalid.write_to_excel({**self.processed_data.invalid_numbers})
        print("Готово", "Файл успешно обработан и сохранён.")    