import re
import phonenumbers
import logging

from enums.CountriesEnum import CountriesEnum
from typing import Union

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataProcessor:
    def __init__(self, selected_regions: list[str]):
        ''' 
            details format:
            {AT: {"label": "Austria", "phone": "43", "phoneLength": [10, 11]}}        
        '''
        self.details: dict[str, dict[str, Union[str, list[int]]]] = CountriesEnum.get_region_details(selected_regions)
        self.valid_numbers: dict[str, list[str]] = {}
        self.invalid_numbers: dict[str, list[str]] = {}
        logging.info(f"Инициализирован DataProcessor с регионами: {selected_regions}")
    
    def process_row(self, phone: str):
        phone = self.__clean_phone(str(phone))
        
        # logging.debug(f"Processing phone: {phone}")
        
        for allowed_region, region_details in self.details.items():
            allowed_code = region_details.get('phone', '')

        try:
            # Parse the phone number using the allowed region
            parsed_number = phonenumbers.parse(phone, allowed_region)

            # Check if the phone number is valid
            if phonenumbers.is_valid_number(parsed_number):
                # Get the region code for the parsed number
                region_code = phonenumbers.region_code_for_number(parsed_number)

                # Ensure the number belongs to the allowed region
                if str(parsed_number.country_code).strip() == allowed_code and region_code == allowed_region:
                    # Format the number in E.164 format and remove "+"
                    formatted_number = phonenumbers.format_number(
                        parsed_number, phonenumbers.PhoneNumberFormat.E164
                    )[1:]

                    # Apply specific logic for AR region (Argentina), if necessary
                    if allowed_region == "AR":
                        formatted_number = self.__get_correct_AR_phone(formatted_number)

                    # Add the valid number to the list
                    self.__add_to_list(allowed_region, formatted_number, self.valid_numbers)
                    # logging.debug(f"Valid phone: {formatted_number} for region: {allowed_region}")
                    return
                else:
                    # If region or country code does not match, add to invalid numbers
                    self.__add_to_list(allowed_region, phone, self.invalid_numbers)
                    # logging.debug(f"Invalid phone: {phone} for region: {allowed_region}")
            else:
                # If the phone number is not valid, add to invalid numbers
                self.__add_to_list(allowed_region, phone, self.invalid_numbers)
                # logging.debug(f"Invalid phone: {phone} for region: {allowed_region}")
                
        except phonenumbers.NumberParseException as e:
            # Handle parsing errors by adding the number to invalid numbers
            self.__add_to_list(allowed_region, phone, self.invalid_numbers)
            # logging.debug(f"Error parsing phone: {phone}, Exception: {e} \\nInvalid phone: {phone} for region: {allowed_region}")

    def __add_to_list(self, allowed_region: str, phone: str, list: dict[str, list[str]]):
        list.setdefault(allowed_region, []).append(phone)
    
    def __get_correct_AR_phone(self, phone: str) -> str:
        if len(phone) == 12:
            return (f'{phone[:2]}9{phone[2:]}')
        else:
            return phone
    
    # def get_key(self):
    #     for key  in self.valid_numbers.items():
    #         return key
    #     return "key doesn't exist"
        
    def __clean_phone(self, phone: str) -> str:
        """Removes all unwanted characters from the phone number, correctly handling '.0' at the end."""
        phone = re.sub(r'\.0$', '', phone)  # Removes trailing .0
        return re.sub(r'\D', '', phone)    # Removes all non-digit characters

    def print_details(self):
        logging.info(f"Details: {self.details}")


