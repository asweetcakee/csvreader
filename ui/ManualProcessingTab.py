import os
import customtkinter
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

from parser.CSVParser import CSVParser
from processor.DataProcessor import DataProcessor
from writer.ExcelWriter import ExcelWriter


class ManualProcessingTab:
    def __init__(self, parent):
        self.parent = parent
        self.csv_parser = None
        self.selected_region = ""
        self.file_title = ""
        
        self.region_dropdown = None
        self.phone_dropdown = None
        self.code_dropdown = None
        self.manual_text_box = None
        self.configure_tab()
            
    def configure_tab(self):
        self.parent.grid_columnconfigure(0, weight=1)
        self._create_top_frame()
        self._create_text_box()
        self._create_bottom_frame()
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
        
    def _create_bottom_frame(self):
        bottom_frame = customtkinter.CTkFrame(self.parent, fg_color="#f2f2f2", height=50)
        bottom_frame.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)
        
        # Labels
        labels = [
            "1. Выберите колонку с регионом",
            "2. Выберите колонку с номером",
            "3. Укажите регион для фильтрации"
        ]
        for i, text in enumerate(labels):
            label = customtkinter.CTkLabel(bottom_frame, text=text, font=("Rubik", 16))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        
        # Dropdowns
        self.region_dropdown = customtkinter.CTkComboBox(bottom_frame, values=[""], command=self._update_code_dropdown)
        self.region_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        self.phone_dropdown = customtkinter.CTkComboBox(bottom_frame, values=[""], command=self._on_phone_dropdown_change)
        self.phone_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        self.code_dropdown = customtkinter.CTkComboBox(bottom_frame, values=[""])
        self.code_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
            
    def _create_process_button(self):
        process_button = customtkinter.CTkButton(
            self.parent, text="Обработать данные", corner_radius=5,
            fg_color="#9FACF6", height=50, text_color="#0F1B60", font=("Rubik", 20),
            command=self._apply_settings
        )
        process_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
    def _update_code_dropdown(self, event=None):
        """Обновляет ComboBox с уникальными регионами."""
        if self.csv_parser.data is not None:
            # Gets selected column from region_dropdown
            selected_column = self.region_dropdown.get()
            
            print("--T | selected column")
            print(selected_column)

            if selected_column:
                try:
                    # # Validate the selected column
                    # self.validate_region_column(selected_column)
                    
                    # Get unique regions
                    regions = self.csv_parser.get_unique_regions(selected_column)
                    print("--T | unique regions")
                    print(regions)
                    
                    # Filter out NaN or None values
                    regions = [region for region in regions if isinstance(region, str) and region.strip()]
                    
                    # Check if regions is not empty
                    if not regions:
                        raise ValueError("Столбец не содержит допустимых кодов регионов.")
                    
                    # Populate the region dropdown with unique regions
                    self.code_dropdown.configure(values=regions)
                    self.selected_region = regions[0]  # Optionally set the first region as default
                    
                except ValueError as e:
                    messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
            else:
                messagebox.showerror("Ошибка", "Не выбран столбец для региона.")
        else:
            messagebox.showerror("Ошибка", "Данные CSV отсутствуют. Загрузите файл перед выбором.")
    
    def _on_phone_dropdown_change(self, selected_value):
        """Handler for when the phone column dropdown value changes."""
        try:
            if selected_value.strip():  # Ensure a value is selected
                #self.validate_phone_column(selected_value)
                print(f"Столбец '{selected_value}' успешно проверен как столбец с телефонами.")
            else:
                raise ValueError("Выберите столбец для телефонов.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
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
            
            self._update_dropdowns()  # Depends on dropdowns value
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
    
    def _update_text_box(self, text):
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.insert("end", text)
        self.text_box.configure(state="disabled")
    
    def _update_dropdowns(self):
        if self.csv_parser and self.csv_parser.data is not None:
            columns = self.csv_parser.data.columns.tolist()
            self.region_dropdown.configure(values=columns)
            self.phone_dropdown.configure(values=columns)
    
    def _apply_settings(self):
        if not self.csv_parser:
            messagebox.showerror("Ошибка", "Сначала выберите CSV файл.")
            return

        # Get values from dropdowns
        region_col = self.region_dropdown.get().strip()
        phone_col = self.phone_dropdown.get().strip()
        region = self.code_dropdown.get().strip()
        
        # Validate dropdown inputs
        if not region_col or not phone_col:
            messagebox.showerror("Ошибка", "Выберите столбцы для регионов и телефонов.")
            return

        if not region:
            messagebox.showerror("Ошибка", "Выберите хотя бы один регион.")
            return
        
        self._process_with_settings(region_col, phone_col, region)
        
    def _process_with_settings(self, region_col, phone_col, region):
        try:
            #!!!!!!!!!!!! VALIDATE CSV HEADERS !!!!!!!!!!!!!!!!
            #self.validate_csv_headers(region_col, phone_col)
            # # Validate the selected columns
            # self.validate_region_column(region_col)
            # self.validate_phone_column(phone_col, region)

            # Ensure the filter region is set
            if not region:
                raise ValueError("Регион для фильтрации не обнаружен.")
            
            # Process the data
            self._process_file(phone_col, region)
            
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def _process_file(self, phone_col, region):
        """Helper method to process the file with given settings."""
        try:
            self._start_processing(phone_col, region)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Обработка провалилась: {e}")
            
    def _start_processing(self, phone_col, region):
        self.processed_data = DataProcessor(region)
        
        # Makes sure self.csv_parser is safe to use and not None
        if self.csv_parser and self.csv_parser.data is not None:
            for _, row in self.csv_parser.data.iterrows():
                self.processed_data.process_row(row[phone_col])
            self._write_to_excel()
        else:
            print("Ошибка", "Данные CSV не загружены.")
        
        self._reset_values()
        
    def _reset_values(self):
        # Closes filtering window after data proccessing is finished
        for window in self.parent.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy()
        
        # Resets all variable values
        self.file_path = ""
        self.csv_parser = None
        
        # Clears dropdown values
        self.region_dropdown.set('') 
        self.region_dropdown['values'] = []
        self.phone_dropdown.set('')
        self.phone_dropdown['values'] = []
        self.code_dropdown.set('')
        self.code_dropdown['values'] = []
        
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