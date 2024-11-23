from CSVParser import CSVParser
from DataProcessor import DataProcessor
from ExcelWriter import ExcelWriter

def main():
    # Reads a CSV file
    csv_parser = CSVParser("es_part_1.csv")
    csv_parser.read_csv()
    #columns = csv_parser.get_columns()
    
    # Lists available columns from a CSV file
    print("Выберите столбцы, которые содержат код региона и номера:")
    # for col, examples in columns.items():
    #     print(f"{col}: {examples}")
    csv_parser.get_columns()

    region_col = input("Введите столбец региона: ")
    phone_col = input("Введите столбец номера: ")

    # Gets unique regions
    unique_regions = csv_parser.get_unique_regions(region_col)
    print(f"В этом файле по столбцу {region_col} найдены следующие уникальные регионы:")
    print(", ".join(unique_regions))

    # Selection of regions and parameters
    selected_regions = input("Выберите интересующие вас регионы (через запятую): ").split(",")
    params = {}
    for region in selected_regions:
        region = region.strip()
        code = input(f"Введите код номера страны для региона {region.upper()}: ").strip("+")
        length = int(input(f"Введите длину номера без кода страны для региона {region}: "))
        params[region.upper()] = {"code": code, "length": length}

    # Processes the data
    processor = DataProcessor(params)
    for _, row in csv_parser.data.iterrows():
        processor.process_row(str(row[region_col]), str(row[phone_col]))
    processor.print_params()

    # Writes processed data into an XLSX file
    writer = ExcelWriter("phone_numbers_output.xlsx")
    all_data = {**processor.processed_data, **processor.partial_data}
    writer.write_to_excel(all_data)
    print("Обработка завершена. Файл записан в phone_numbers_output.xlsx")

if __name__ == "__main__":
    main()
