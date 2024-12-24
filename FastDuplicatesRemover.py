import csv
import phonenumbers
from phonenumbers import geocoder   

# Функция для чтения номеров из файла
def read_phones(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {row['phone'] for row in reader}

# Функция для фильтрации первого файла
def filter_phones(file1, file2, output_file):
    used_phones = read_phones(file2)  # Считываем номера из второго файла

    with open(file1, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

        # Создаем новый файл для результатов
        with open(output_file, mode='w', encoding='utf-8', newline='') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            writer.writeheader()

            # Проходим по строкам первого файла и записываем только те, что не содержатся во втором файле
            for row in reader:
                if row['phone'] not in used_phones:
                    writer.writerow(row)

# # Путь к файлам
# file1_path = 'file1.csv'  # Первый файл (рабочие номера)
# file2_path = 'file2.csv'  # Второй файл (использованные номера)
# output_path = 'filtered_file.csv'  # Результат

# # Запускаем фильтрацию
# filter_phones(file1_path, file2_path, output_path)

number = phonenumbers.parse("+48501785490", "pl")
location = geocoder.description_for_number(number, "en")
print("location:", location)