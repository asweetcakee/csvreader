import os
import customtkinter
from tkinter import filedialog, messagebox
from PIL import Image

from parser.CSVParser import CSVParser
from processor.DataProcessor import DataProcessor
from writer.ExcelWriter import ExcelWriter

class AutoProcessingTab:
    def __init__(self, parent):
        self.parent = parent
        self.csv_parser = None
        self.file_path = ""
        self.file_title = ""
        
        # CONSTANTS
        self.REGION_COLUMN = "country"
        self.PHONE_COLUMN = "phone"
        
        self.checkbox_var = customtkinter.StringVar(value="off")
        self.configure_tab()
        
    def configure_tab(self):
        self.parent.grid_columnconfigure(0, weight=1)
        self._create_top_frame()
        self._create_text_box()
        self._create_checkbox()
        self._create_process_button()
    
    def _create_top_frame(self):
        # Top frame
        top_frame = customtkinter.CTkFrame(self.parent, fg_color="#f2f2f2")
        top_frame.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # Logo
        image = Image.open("img/top_title_logo.png")
        ctk_image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(90, 45))
        label = customtkinter.CTkLabel(top_frame, text="", width=120, height=100, image=ctk_image, fg_color="#d9d9d9", corner_radius=5)
        label.grid(row=0, column=0, padx=10, pady=0)

        # Selection button
        select_file_button = customtkinter.CTkButton(
            top_frame, text="Выбрать файл", height=100, corner_radius=5,
            fg_color="#9FACF6", text_color="#0F1B60", font=("Rubik", 26),
            command=self._select_file
        )
        select_file_button.grid(row=0, column=1, padx=10, pady=0, sticky="ew")
        
    def _create_text_box(self):
        self.text_box = customtkinter.CTkTextbox(self.parent, width=540, height=150, wrap="none")
        self.text_box.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.text_box.configure(state="disabled")

    def _create_checkbox(self):
        checkbox = customtkinter.CTkCheckBox(
            self.parent, text="Смотреть по FTD", variable=self.checkbox_var,
            onvalue="on", offvalue="off", command=self._checkbox_event
        )
        checkbox.grid(row=2, column=0, padx=10, pady=0, sticky="ew")

    def _create_process_button(self):
        process_button = customtkinter.CTkButton(
            self.parent, text="Обработать данные", corner_radius=5,
            fg_color="#9FACF6", height=50, text_color="#0F1B60", font=("Rubik", 20),
            command=self._apply_settings
        )
        process_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def _select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.file_path:
            print("File was not selected.")
            return
        self._load_csv()

    def _load_csv(self):
        try:
            # Load and display CSV preview
            self.csv_parser = CSVParser(self.file_path)
            self.csv_parser.read_csv()
            # Gets first 3 entries
            preview_text = self.csv_parser.data.head(3).to_string(index=False)
            self._update_text_box(preview_text)
            self.file_title = self.csv_parser.get_file_name()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def _update_text_box(self, text):
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.insert("end", text)
        self.text_box.configure(state="disabled")

    def _checkbox_event(self):
        print("Checkbox value:", self.checkbox_var.get())

    def _apply_settings(self):
        if not self.csv_parser:
            messagebox.showerror("Ошибка", "Сначала выберите CSV файл.")
            return

        if self.checkbox_var.get() == "on":
            self._process_ftd_case()
        
        region = self._get_unique_region()[0]
        self._process_with_settings(region)
    
    def _process_ftd_case(self):     
        try:
            self.csv_parser.data = self.csv_parser.data[self.csv_parser.data['firstdeposit_time'].notnull() & (self.csv_parser.data['firstdeposit_time'] != '')]                           
        except Exception as e:
            messagebox.showerror("Ошибка", f"Обработка FTD провалилась: {e}")
    
    def _process_with_settings(self, region):
        """Validates inputs and processes the file."""
        
        try:
            #!!!!!!!!!!!! VALIDATE CSV HEADERS !!!!!!!!!!!!!!!!
            #self.validate_csv_headers(region_col, phone_col)
            
            # Ensures the filter region is set
            if not region:
                raise ValueError("Регион для фильтрации не обнаружен.")
            
            self._process_file(region)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
                
    def _get_unique_region(self):
        regions = self.csv_parser.get_unique_regions(self.REGION_COLUMN)
        
        if not regions:
            raise ValueError("Столбец не содержит допустимых кодов регионов.")
        
        return regions

    def _process_file(self, region):
        """Helper method to process the file with given settings."""
        try:
            self._start_processing(region)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Обработка провалилась: {e}")
    
    def _start_processing(self, region):
        self.processed_data = DataProcessor(region)
        
        # Makes sure self.csv_parser is safe to use and not None
        if self.csv_parser and self.csv_parser.data is not None:
            for _, row in self.csv_parser.data.iterrows():
                self.processed_data.process_row(row[self.PHONE_COLUMN])
            self._write_to_excel()
        else:
            print("Ошибка", "Данные CSV не загружены.")
        
        self._reset_values()
    
    def _reset_values(self):
        # Resets all variable values
        self.file_path = ""
        self.csv_parser = None
        self.checkbox_var.set("off")
        
        if hasattr(self, 'text_box'):
            self.text_box.configure(state="normal")
            self.text_box.delete("1.0", "end")
            self.text_box.configure(state="disabled")
    
    def _write_to_excel(self):
        valid_writer = ExcelWriter("result/valid_phones.xlsx")
        invalid_writer = ExcelWriter("result/invalid_phones.xlsx")
        valid_writer.write_to_excel(self.processed_data.valid_numbers)
        invalid_writer.write_to_excel(self.processed_data.invalid_numbers)
        
        creation_date_valid = valid_writer.get_date()
        max_entries_valid = valid_writer.get_total_rows()
        creation_date_invalid = invalid_writer.get_date()
        max_entries_invalid = invalid_writer.get_total_rows()
        
        valid_new_name = f"result/val_{self.file_title}_{creation_date_valid}_{max_entries_valid}.xlsx"
        invalid_new_name = f"result/inval_{self.file_title}_{creation_date_invalid}_{max_entries_invalid}.xlsx"
        
        os.rename(valid_writer.output_file, valid_new_name)
        os.rename(invalid_writer.output_file, invalid_new_name)

        print("Готово", "Файл успешно обработан и сохранён.")
        print(f"Valid file renamed to: {valid_new_name}")
        print(f"Invalid file renamed to: {invalid_new_name}")