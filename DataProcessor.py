import re
import phonenumbers
from CountriesEnum import CountriesEnum

class DataProcessor:
    def __init__(self, selected_regions):
        ''' 
            details format:
            {AT: {"label": "Austria", "phone": "43", "phoneLength": [10, 11]}}        
        '''
        self.details = CountriesEnum.get_region_details(selected_regions)
        self.valid_numbers = {}
        self.invalid_numbers = {} 
    
    def process_row(self, phone):
        # Removes unwanted symbols
        phone = self.clean_phone(str(phone))
        
        # Gets first key
        allowed_region = list(self.details.keys())[0]
        # Gets key value 'phone'
        allowed_code = self.details[allowed_region]['phone']   
        
        try:
            # Parses the number
            parsed_number = phonenumbers.parse(phone, None)  # None означает международный формат
            
            # Is a number valid? 
            if phonenumbers.is_valid_number(parsed_number):
                # Does the number has valid country speicific code
                if str(parsed_number.country_code).strip() == allowed_code:
                    # Formats number into valid
                    formatted_number = phonenumbers.format_number(
                        parsed_number, phonenumbers.PhoneNumberFormat.E164
                    )[1:]  # Gets rid of "+"                    
                    self._add_to_list(allowed_region, formatted_number, self.valid_numbers)
                else:
                    # Number doesn't match the speicific country code
                    self._add_to_list(allowed_region, phone, self.invalid_numbers)
            else:
                # Number is invalid
                self._add_to_list(allowed_region, phone, self.invalid_numbers)
        except phonenumbers.NumberParseException:
            #print("EXCEPTION: " + phone)
            self._add_to_list(allowed_region, phone, self.invalid_numbers)
            
        # print("--T | invalid dict: ")
        # print(self.invalid_numbers)
        # print("--T | valid dict: ")
        # print(self.valid_numbers)

    def _add_to_list(self, allowed_region, phone, list):
        if allowed_region not in list:
            list[allowed_region] = []
        list[allowed_region].append(phone)
    
    
    def clean_phone(self, phone):
        """Removes unwanted trailing characters from the phone number."""
        # Removes unwanted symbols at the end of the string
        return re.sub(r'[^\d+]$', '', phone)  # Ensures phone ends in a digit
    
    def print_details(self):
        print("--T | Details: ")
        print(self.details)

