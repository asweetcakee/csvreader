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
        phone = self.clean_phone(str(phone))
        allowed_region = list(self.details.keys())[0]
        allowed_code = self.details[allowed_region].get('phone', '')

        # print(f"Processing phone: {phone}")
        # print(f"Allowed Region: {allowed_region}, Allowed Code: {allowed_code}")

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
                        formatted_number = self.get_correct_AR_phone(formatted_number)

                    # Add the valid number to the list
                    self._add_to_list(allowed_region, formatted_number, self.valid_numbers)
                else:
                    # If region or country code does not match, add to invalid numbers
                    self._add_to_list(allowed_region, phone, self.invalid_numbers)
            else:
                # If the phone number is not valid, add to invalid numbers
                self._add_to_list(allowed_region, phone, self.invalid_numbers)
        except phonenumbers.NumberParseException as e:
            # Handle parsing errors by adding the number to invalid numbers
            self._add_to_list(allowed_region, phone, self.invalid_numbers)

        # print(f"Valid Numbers: {self.valid_numbers}")
        # print(f"Invalid Numbers: {self.invalid_numbers}")


        
        # print("--T | invalid dict: ")
        # print(self.invalid_numbers)
        # print("--T | valid dict: ")
        # print(self.valid_numbers)

    def _add_to_list(self, allowed_region, phone, list):
        if allowed_region not in list:
            list[allowed_region] = []
        list[allowed_region].append(phone)
    
    def get_correct_AR_phone(self, phone):
        if len(phone) == 12:
            return (f'{phone[:2]}9{phone[2:]}')
        else:
            return phone
    
    def get_key(self):
        for key  in self.valid_numbers.items():
            return key
        return "key doesn't exist"
    
    def clean_phone(self, phone):
        """Removes unwanted trailing characters from the phone number."""
        # Removes unwanted symbols at the end of the string
        return re.sub(r'[^\d+]$', '', phone)  # Ensures phone ends in a digit
    
    def print_details(self):
        print("--T | Details: ")
        print(self.details)

