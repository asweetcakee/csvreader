import os
import customtkinter
import logging

from tkinter import filedialog, messagebox
from PIL import Image

from parser.CSVParser import CSVParser
from processor.DataProcessor import DataProcessor
from writer.ExcelWriter import ExcelWriter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AutoProcessingTab:
    def __init__(self, parent: customtkinter.CTkFrame):
        self.parent: customtkinter.CTkFrame = parent
        self.csv_parser = None
        self.file_path: str = ""
        self.file_title: str = ""
        
        # CONSTANTS
        self.REGION_COLUMN: str = "country"
        self.PHONE_COLUMN: str = "phone"
        
        self.checkbox_var: customtkinter.StringVar = customtkinter.StringVar(value="off")
        self.__configure_tab()
        
    def __configure_tab(self):
        self.parent.grid_columnconfigure(0, weight=1)
        self.__create_top_frame()
        self.__create_text_box()
        self.__create_checkbox()
        self.__create_process_button()
    
    def __create_top_frame(self):
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
            command=self.__select_file
        )
        select_file_button.grid(row=0, column=1, padx=10, pady=0, sticky="ew")
        
    def __create_text_box(self):
        self.text_box = customtkinter.CTkTextbox(self.parent, width=540, height=150, wrap="none")
        self.text_box.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.text_box.configure(state="disabled")

    def __create_checkbox(self):
        checkbox = customtkinter.CTkCheckBox(
            self.parent, text="Смотреть по FTD", variable=self.checkbox_var,
            onvalue="on", offvalue="off", command=self.__checkbox_event
        )
        checkbox.grid(row=2, column=0, padx=10, pady=0, sticky="ew")

    def __create_process_button(self):
        process_button = customtkinter.CTkButton(
            self.parent, text="Обработать данные", corner_radius=5,
            fg_color="#9FACF6", height=50, text_color="#0F1B60", font=("Rubik", 20),
            command=self.__apply_settings
        )
        process_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def __select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.file_path:
            logging.warning("Файл не был выбран.")
            return
        self.__load_csv()

    def __load_csv(self):
        try:
            # Load and display CSV preview
            self.csv_parser = CSVParser(self.file_path)
            self.csv_parser.read_csv()
            
            # Gets first 3 entries preview
            preview_text = self.csv_parser.get_columns()
            self.__update_text_box(preview_text)
            
            # Gets selected file name
            self.file_title = self.csv_parser.get_file_name()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def __update_text_box(self, text: str):
        self.text_box.configure(state="normal", font=("Courier", 12))
        self.text_box.delete("1.0", "end")
        self.text_box.insert("end", text)
        self.text_box.configure(state="disabled")

    def __checkbox_event(self):
        logging.info(f"FTD setting: {self.checkbox_var.get()}")

    def __apply_settings(self):
        if not self.csv_parser:
            messagebox.showerror("Ошибка", "Сначала выберите CSV файл.")
            return

        if self.checkbox_var.get() == "on":
            self.__process_ftd_case()
        
        region = self.__get_unique_region()[0]
        self.__process_with_settings(region)
    
    def __process_ftd_case(self):     
        try:
            self.csv_parser.data = self.csv_parser.data[self.csv_parser.data['firstdeposit_time'].notnull() & (self.csv_parser.data['firstdeposit_time'] != '')]                           
        except Exception as e:
            messagebox.showerror("Ошибка", f"Обработка FTD провалилась: {e}")
    
    def __process_with_settings(self, region: str):
        """Validates inputs and processes the file."""
        
        try:
            #!!!!!!!!!!!! VALIDATE CSV HEADERS !!!!!!!!!!!!!!!!
            #self.validate_csv_headers(region_col, phone_col)
            
            # Ensures the filter region is set
            if not region:
                raise ValueError("Регион для фильтрации не обнаружен.")
            
            self.__process_file(region)
        except ValueError as e:
            logging.error(f"Ошибка, не удалось обработать с настройками. Ошибка: {e}")
            messagebox.showerror("Ошибка", f"Не удалось обработать с настройками. Ошибка: {e}")
                
    def __get_unique_region(self) -> list[str]:
        regions = self.csv_parser.get_unique_regions(self.REGION_COLUMN)
        
        if not regions:
            raise ValueError("Столбец не содержит допустимых кодов регионов.")
        
        return regions

    def __process_file(self, region: str):
        """Helper method to process the file with given settings."""
        try:
            self.__start_processing(region)
        except Exception as e:
            logging.error("Ошибка", f"Обработка провалилась: {e}")
            messagebox.showerror("Ошибка", f"Обработка провалилась: {e}")
    
    def __start_processing(self, region: str):
        self.processed_data = DataProcessor(region)
        logging.info(f"Начинается обработка для региона: {region}")
        
        # Makes sure self.csv_parser is safe to use and not None
        if self.csv_parser and self.csv_parser.data is not None:
            try:
                for row in self.csv_parser.data.itertuples(index=False):
                    self.processed_data.process_row(getattr(row, self.PHONE_COLUMN))
                self.__write_to_excel()
            except Exception as e:
                logging.error(f"Ошибка во время обработки спарсенных данных: {e}")
        else:
            logging.error("Ошибка: Данные CSV не загружены.")
        
        self.__reset_values()
        logging.info("Обработка завершена.")
    
    def __reset_values(self):
        logging.info("Значения сброшены.")
        # Resets all variable values
        self.file_path = ""
        self.csv_parser = None
        self.checkbox_var.set("off")
        
        if hasattr(self, 'text_box'):
            self.text_box.configure(state="normal")
            self.text_box.delete("1.0", "end")
            self.text_box.configure(state="disabled")
    
    def __write_to_excel(self):
        try:
            logging.info("Создаем первичные xlsx файлы.")
            valid_writer = ExcelWriter("result/valid_phones.xlsx")
            invalid_writer = ExcelWriter("result/invalid_phones.xlsx")
            
            # Writes data
            valid_writer.write_to_excel(self.processed_data.valid_numbers)
            invalid_writer.write_to_excel(self.processed_data.invalid_numbers)
            
            # Renames files
            valid_new_name = self.__rename_and_log(valid_writer, "val")
            invalid_new_name = self.__rename_and_log(invalid_writer, "inval")
            
            # Notifies user
            self.__log_and_notify(
                f"Файлы успешно сохранены: {valid_new_name}, {invalid_new_name}",
                f"Файлы сохранены:\n{valid_new_name}\n{invalid_new_name}"
            )
        except Exception as e:
            logging.error(f"Ошибка при записи в Excel файл: {e}")
            messagebox.showerror("Ошибка", f"Не удалось записать данные в файл: {e}")
    
    def __rename_and_log(self, writer: ExcelWriter, prefix: str) -> str:
        date = writer.get_date()
        total_rows = writer.get_total_rows()
        new_name = f"result/{prefix}_{self.file_title}_{date}_{total_rows}.xlsx"
        os.rename(writer.output_file, new_name)
        logging.info(f"Файл переименован: {writer.output_file} -> {new_name}")
        return new_name

    def __log_and_notify(self, log_message: str, notify_message: str, level: str = "info"):
        if level == "info":
            logging.info(log_message)
            messagebox.showinfo("Информация", notify_message)
        elif level == "error":
            logging.error(log_message)
            messagebox.showerror("Ошибка", notify_message)