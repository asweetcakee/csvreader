import re
import pandas as pd
import phonenumbers 


def get_numbers(file_name:str) -> list:
    df = pd.read_csv(file_name,usecols=["phone"], sep = ';', skip_blank_lines=True)

    print(df.head(100))

    return df["phone"].tolist()



# def transform_number(number, default_country_code="54"):
#     # Убираем пробелы и символы
#     number = re.sub(r"[^\d]", "", number)

#     # Проверяем наличие локального префикса (0)
#     if number.startswith("0"):
#         number = number[1:]  # Убираем "0"

#     # Убираем префикс мобильного номера (15)
#     if number.startswith("15"):
#         number = number[2:]  # Убираем "15"

#     # Предполагаем код региона, если он известен
#     # Например, для номеров длиной 7 цифр можно добавить код региона, например, "11" для Буэнос-Айреса
#     if len(number) == 7:
#         number = "11" + number  # Предположительно Буэнос-Айрес

#     # Добавляем код страны
#     transformed_number = f" неоригинал {default_country_code} {number} - оригинал{number}"
#     return transformed_number


# def transform_number(number, region_codes, default_country_code="54"):
#     # Очищаем номер от лишних символов
#     number = re.sub(r"[^\d]", "", str(number))
#     print(number)
#     def_number = number
#     this_number_geo_code = ''
#     if len(number) > 8:
#         if '0' in number[:1]:
#             number = number[1:]
#         elif '54' == number[0:2]:
#             number = number[2:]
#     else:
#         return f'{def_number} - длинна номера не подразумевает нормальный номер'
    

#     if len(number) > 8:
#         if number[:1] == '9':
#             number = number[1:]
        


#     if len(number) > 8:
#         if number[:3] in region_codes:
#             this_number_geo_code = number[:3]
#             number = number[3:]
#         elif '11' in number[:2]:
#             this_number_geo_code = '11'
#             number = number[2:]
#         else:
#             return f'{def_number} - отсутствие или неверный гео код'
#     else:
#         return f'{def_number} - длинна номера не подразумевает нормальный номер'

#     if len(number) > 6:
#         if '15' in number[:2]:
#             number = number[2:]
#     else:
#         return f'{def_number} - длинна номера не подразумевает нормальный номер'

#     if 6 <= len(number) <= 8:
#         number = f'{default_country_code}9{this_number_geo_code}{number} ---- {def_number}'
#         return number 
#     else:
#         return f'{def_number} - длинна номера не подразумевает нормальный номер'


                                   

def file_edit(numbers):
    with open('output.txt', mode ='a') as file:
        for line in numbers:
            file.write(line + '\n')


def valid_check(phone_list,region = "AR", allowed_code = '54'):

    valid_numbers = []
    invalid_numbers = []
    for phone in phone_list:
        try:
            # Парсим номер
            parsed_number = phonenumbers.parse(phone, None)  # None означает международный формат
            # Проверяем валидность номера
            if phonenumbers.is_valid_number(parsed_number):
                # Проверяем, соответствует ли номер заданному коду
                if str(parsed_number.country_code) == allowed_code:
                    valid_numbers.append(phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)[1:])
                else:
                    invalid_numbers.append(phone + "невалид")
            else:
                invalid_numbers.append(phone + "невалид")
        except phonenumbers.NumberParseException:
            invalid_numbers.append(phone + "невалид")

    print(invalid_numbers)
    
    result = []
    for number in valid_numbers:
        if len(number) == 12:
            result.append(f'{number[:2]}9{number[2:]}')
        else:
            result.append(number)
    
    result = set(result)
    return result





phone_numbers = get_numbers('ar_part_1.csv')

validating_numbers = valid_check(phone_numbers)

file_edit(validating_numbers)