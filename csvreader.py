import pandas as pd

# Открываем файл с игнорированием ошибок
with open("at_part_1.csv", "r", encoding="utf-8", errors="replace") as file:
    data = file.read()

# Записываем обратно в файл для работы
with open("temp_cleaned_file.csv", "w", encoding="utf-8") as cleaned_file:
    cleaned_file.write(data)

# 1. Чтение файла с обработкой ошибок
df = pd.read_csv("temp_cleaned_file.csv", delimiter=";")
print("Файл успешно загружен!")

# Подготовка словаря стран и номеров
country_codes = {
    "ES": {"code": "34", "length": 9},  # Spain
    "AR": {"code": "54", "length": 9},  # Argentina
    "CL": {"code": "56", "length": 9},  # Chile only mobile
    "MX": {"code": "52", "length": 10}, # Mexico
    "CO": {"code": "57", "length": 10}, # Columbia only mobile
    "AT": {"code": "43", "length": 10}, # Austria
    "RO": {"code": "40", "length": 9}   # Romania
}

# Функция для обработки номеров телефонов по стране
def process_phone_number(phone, country, ID, phones_dict, country_codes):
    phone = str(phone).strip()

    # Проверяем, если страна есть в словаре кодов
    if country in country_codes:
        numberInfo = country_codes[country]
        code = numberInfo["code"]
        length = numberInfo["length"]

        # Обрабатываем номер телефона в зависимости от формата
        if phone.startswith(f"+{code}") and len(phone[len(code)+1:]) == length:
            phones_dict[country]["phonesWithCountryCode"].append(f"{ID}:{phone[1:]}")
        elif phone.startswith(code) and len(phone[len(code):]) == length:
            phones_dict[country]["phonesWithCountryCode"].append(f"{ID}:{phone}")
        elif phone.isdigit() and len(phone) == length:
            phones_dict[country]["phonesWithoutCountryCode"].append(f"{ID}:{country}:{phone}")

# 2. Подготовка словаря для телефонов по странам
phones_dict = {}

# Итерация по строкам и фильтрация по странам
for _, row in df.iterrows():
    phone = row['phone']
    countries = [row['country'].upper()]  # Список стран для обработки
    if row['last_ip_country']:  # Если есть дополнительная страна
        countries.append(row['last_ip_country'].upper())
    
    ID = row['id']

    # Добавляем страну в словарь, если её ещё нет
    for country in countries:
        if country not in phones_dict:
            phones_dict[country] = {"phonesWithCountryCode": [], "phonesWithoutCountryCode": []}

        # Вызываем функцию обработки номеров для каждой страны
        process_phone_number(phone, country, ID, phones_dict, country_codes)

# Функция для записи номеров в Excel
def writeNumbersIntoTables(writer, country, phone_lists, dictType):
    if phone_lists[dictType]:
        output_data = []
        start_id = 701120240001
        rfm_segment = "cold_21_11"
        
        for entry in phone_lists[dictType]:
            split_entry = entry.split(":")
            
            if len(split_entry) == 2:
                ID, phone = split_entry
            else:
                print(f"Неверный формат для записи: {entry}")
                continue
            
            output_data.append({
                "phone": phone,
                "full_name": "",
                "age": 1995,
                "city": "",
                "import_id": start_id,
                "gender": "",
                "rfm_segment": rfm_segment,
                "game_id": start_id,
            })
            start_id += 1
        
        if output_data:  # Проверяем, есть ли данные для записи
            output_df = pd.DataFrame(output_data)
            output_df.to_excel(writer, sheet_name=f"{country} {'undefined' if dictType == 'phonesWithoutCountryCode' else ''}".strip(), index=False)

# 4. Создание Excel файлов для каждой страны
with pd.ExcelWriter('output_all_countries.xlsx') as writer:
    sheet_added = False
    
    # Для каждой страны создаем два листа
    for country, phone_lists in phones_dict.items():
        # Для номеров с кодом страны
        writeNumbersIntoTables(writer, country, phone_lists, "phonesWithCountryCode")

        # Для номеров без кода страны
        writeNumbersIntoTables(writer, country, phone_lists, "phonesWithoutCountryCode")

        # Если хотя бы один лист был добавлен, установим флаг
        sheet_added = sheet_added or (phone_lists["phonesWithCountryCode"] or phone_lists["phonesWithoutCountryCode"])

    if not sheet_added:
        print("Ошибка: Нет данных для сохранения в Excel")
    else:
        print("Данные успешно сохранены в output_all_countries.xlsx")
