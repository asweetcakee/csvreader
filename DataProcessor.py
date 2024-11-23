class DataProcessor:
    def __init__(self, params):
        """
        :param params: Paramateres Dictionary:
            {"AT": {"code": "43", "length": 10}, "MX": {"code": "52", "length": 10}}
        """
        self.params = params
        self.processed_data = {region.upper(): set() for region in params}
        self.partial_data = {f"{region.upper()}-неполные номера": set() for region in params}

    def process_row(self, region, phone):
        """Processes 1 row"""
        # print("--REGION: " + row[region_col])
        # print("--PHONE: " + row[phone_col])
        
        region = region.upper()
        
        region_params = self.params.get(region)
        if not region_params:
            return # The selected region was not found in the list   

        country_code = region_params["code"]
        number_length = region_params["length"]

        if not isinstance(phone, str):
            phone = str(phone)
        
        if phone.startswith("+"):
            phone = phone.lstrip("+")  # Gets rid of "+" sign

        if phone.startswith(country_code):
            number = phone[len(country_code):] # Gets a number without a country code
            if len(number) == number_length:
                self.processed_data[region].add(phone)
            else:
                self.partial_data[f"{region}-неполные номера"].add(phone)
        else:
            self.partial_data[f"{region}-неполные номера"].add(phone)
        
    def print_params(self):
        print(self.params)
    
    def print_data(self):
        print(self.processed_data)
