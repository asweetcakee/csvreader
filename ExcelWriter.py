from openpyxl import Workbook

class ExcelWriter:
    def __init__(self, output_file):
        self.output_file = output_file

    def write_to_excel(self, data):
        """
        :param data: Dict of processed data, key — list name, value — list of phone numbers
        """
        wb = Workbook()
        for sheet_name, phone_numbers in data.items():
            ws = wb.create_sheet(sheet_name)
            ws.append(["phone", "full_name", "age", "city", "import_id", "gender", "rfm_segment", "game_id"])

            # Fills in the data
            import_id = 701120240001
            for phone in phone_numbers:
                ws.append([phone, "", 1995, "", import_id, "", "cold_21_11", import_id])
                import_id += 1

            # !!! Need to add a logic of setting rfm_segmenta value basing on the data a file is being processed
            # !!! for example: cold_21_11 <- 21 - is a day, 11 - is a month

        # Deletes the default excel sheet 
        default_sheet = wb["Sheet"]
        if default_sheet:
            wb.remove(default_sheet)

        wb.save(self.output_file)
