import os
import customtkinter
import logging

from tkinter import filedialog, messagebox
from PIL import Image

from processor.DataProcessorManager import DataProcessorManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AutoProcessingTab:
    def __init__(self, parent: customtkinter.CTkFrame):
        self.parent: customtkinter.CTkFrame = parent
        self.data_manager = DataProcessorManager()
        self.file_path: str = ""
                        
        # CONSTANTS
        self.REGION_COLUMN: str = "country"
        self.PHONE_COLUMN: str = "phone"
        self.FTD_COLUMN: str = "firstdeposit_time"
        
        self.checkbox_var: customtkinter.StringVar = customtkinter.StringVar(value="off")
        self.checkbox_var2: customtkinter.StringVar = customtkinter.StringVar(value="off")
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
            self.parent, text="Смотреть по FTD", 
            text_color="#0F1B60", border_color="#9FACF6", 
            variable=self.checkbox_var,
            onvalue="on", offvalue="off", command=self.__checkbox_event
        )
        checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        checkbox2 = customtkinter.CTkCheckBox(
            self.parent, text="Смотреть без FTD", 
            text_color="#0F1B60", border_color="#9FACF6",  
            variable=self.checkbox_var2,
            onvalue="on", offvalue="off", command=self.__checkbox_event
        )
        checkbox2.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    def __create_process_button(self):
        process_button = customtkinter.CTkButton(
            self.parent, text="Обработать данные", corner_radius=5,
            fg_color="#9FACF6", height=50, text_color="#0F1B60", font=("Rubik", 20),
            command=self.__apply_settings
        )
        process_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    def __select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.file_path:
            logging.warning("Файл не был выбран.")
            return
        self.__load_csv()

    def __load_csv(self):
        try:
            # Gets first 3 entries preview
            preview_text = self.data_manager.load_csv(
                self.file_path,
                required_headers=[self.REGION_COLUMN, self.PHONE_COLUMN, self.FTD_COLUMN]
            )
            self.__update_text_box(preview_text)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def __update_text_box(self, text: str):
        self.text_box.configure(state="normal", font=("Courier", 12))
        self.text_box.delete("1.0", "end")
        self.text_box.insert("end", text)
        self.text_box.configure(state="disabled")

    def __checkbox_event(self):
        logging.info(f"FTD setting: {self.checkbox_var.get()}")
        logging.info(f"No FTD setting: {self.checkbox_var2.get()}")

    def __clear_checkbox_values(self):
        self.checkbox_var.set("off")
        self.checkbox_var2.set("off")
    
    def __reset_values(self):
        logging.info("Значения UI сброшены.")
        # Resets all variable values
        self.checkbox_var.set("off")
        self.checkbox_var2.set("off")
        
        if hasattr(self, 'text_box'):
            self.text_box.configure(state="normal")
            self.text_box.delete("1.0", "end")
            self.text_box.configure(state="disabled")
    
    def __apply_settings(self):
        
        if self.checkbox_var.get() == "on" and self.checkbox_var2.get() == "on":
            messagebox.showwarning("Предупреждение", "Нельзя отмечать одновременно 2 настройки.")
            logging.warning("Отмечены одновременно FTD и No FTD.")
            self.__clear_checkbox_values()
            return
        
        try:
            # Applies filtering and processing
            ftd_filter = "FTD" if self.checkbox_var.get() == "on" else "No FTD" if self.checkbox_var2.get() == "on" else ""
            self.data_manager.process_data(self.REGION_COLUMN, self.PHONE_COLUMN, "", self.FTD_COLUMN, ftd_filter)
            
            # Writes to excel
            valid_file, invalid_file = self.data_manager.write_to_excel()
                
            messagebox.showinfo("Готово", f"Файлы сохранены:\n{valid_file}\n{invalid_file}")
            
            # Resets all values
            self.__reset_values()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))