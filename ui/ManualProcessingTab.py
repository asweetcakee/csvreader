import os
import customtkinter
import logging
from tkinter import filedialog, messagebox
from PIL import Image
from processor.DataProcessorManager import DataProcessorManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ManualProcessingTab:
    def __init__(self, parent):
        self.parent = parent
        self.data_manager = DataProcessorManager()
        self.file_path = ""
        self.file_title = ""

        # UI Elements
        self.region_dropdown = None
        self.phone_dropdown = None
        self.code_dropdown = None

        # CONSTANTS
        self.FTD_COLUMN: str = "firstdeposit_time"
        
        # Checkbox state variables
        self.checkbox_var = customtkinter.StringVar(value="off")
        self.checkbox_var2 = customtkinter.StringVar(value="off")

        # Configure UI
        self.configure_tab()

    def configure_tab(self):
        self.parent.grid_columnconfigure(0, weight=1)
        self._create_top_frame()
        self._create_text_box()
        self._create_bottom_frame()
        self._create_process_button()

    def _create_top_frame(self):
        # Top frame with logo and file selection
        top_frame = customtkinter.CTkFrame(self.parent, fg_color="#f2f2f2")
        top_frame.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # Logo
        image = Image.open("img/top_title_logo.png")
        ctk_image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(90, 45))
        label = customtkinter.CTkLabel(
            top_frame, text="", width=120, height=100, image=ctk_image, fg_color="#d9d9d9", corner_radius=5
        )
        label.grid(row=0, column=0, padx=10, pady=0)

        # File selection button
        select_file_button = customtkinter.CTkButton(
            top_frame, text="Выбрать файл", height=100, corner_radius=5,
            fg_color="#9FACF6", text_color="#0F1B60", font=("Rubik", 26),
            command=self._select_file
        )
        select_file_button.grid(row=0, column=1, padx=10, pady=0, sticky="ew")

    def _create_text_box(self):
        # Textbox to preview file data
        self.text_box = customtkinter.CTkTextbox(self.parent, width=540, height=150, wrap="none")
        self.text_box.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.text_box.configure(state="disabled")

    def _create_bottom_frame(self):
        # Frame for dropdowns and checkboxes
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

        self.phone_dropdown = customtkinter.CTkComboBox(bottom_frame, values=[""])
        self.phone_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.code_dropdown = customtkinter.CTkComboBox(bottom_frame, values=[""])
        self.code_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Checkboxes
        self.__create_checkboxes(bottom_frame)

    def __create_checkboxes(self, frame):
        checkbox = customtkinter.CTkCheckBox(
            frame, text="Смотреть по FTD", text_color="#0F1B60", border_color="#9FACF6",
            variable=self.checkbox_var, onvalue="on", offvalue="off", command=self.__checkbox_event
        )
        checkbox.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        checkbox2 = customtkinter.CTkCheckBox(
            frame, text="Смотреть без FTD", text_color="#0F1B60", border_color="#9FACF6",
            variable=self.checkbox_var2, onvalue="on", offvalue="off", command=self.__checkbox_event
        )
        checkbox2.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

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
            logging.warning("Файл не был выбран.")
            return
        self._load_csv()

    def _load_csv(self):
        try:
            # Load CSV manually and get eligible columns
            eligible_columns = self.data_manager.load_csv_manual(self.file_path)

            # Populate dropdowns with eligible columns
            self.region_dropdown.configure(values=eligible_columns["eligible_countries"])
            self.phone_dropdown.configure(values=eligible_columns["eligible_phones"])
            logging.info(f"Eligible countries: {eligible_columns['eligible_countries']}")
            logging.info(f"Eligible phones: {eligible_columns['eligible_phones']}")


            # Display CSV preview
            preview_text = self.data_manager.csv_parser.get_columns()
            self._update_text_box(preview_text)

            # Notify if no eligible columns are found
            if not eligible_columns["eligible_countries"]:
                messagebox.showwarning("Предупреждение", "Не обнаружено подходящих колонок для страны.")
            if not eligible_columns["eligible_phones"]:
                messagebox.showwarning("Предупреждение", "Не обнаружено подходящих колонок для телефона.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def _update_text_box(self, text: str):
        self.text_box.configure(state="normal", font=("Courier", 12))
        self.text_box.delete("1.0", "end")
        self.text_box.insert("end", text)
        self.text_box.configure(state="disabled")

    def _update_dropdowns(self):
        # Populate dropdowns with column names
        try:
            columns = self.data_manager.get_available_columns()
            self.region_dropdown.configure(values=columns)
            self.phone_dropdown.configure(values=columns)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def _update_code_dropdown(self, event=None):
        # Populate code dropdown with unique region values
        selected_region_col = self.region_dropdown.get().strip()
        
        if selected_region_col:  # Checks if a valid column is selected
            try:
                regions = self.data_manager.get_unique_values(selected_region_col)
                if regions:  # Ensure regions are not empty
                    self.code_dropdown.configure(values=regions)
                else:
                    messagebox.showwarning("Предупреждение", "Нет уникальных значений в выбранной колонке.")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def __checkbox_event(self):
        logging.info(f"FTD setting: {self.checkbox_var.get()}")
        logging.info(f"No FTD setting: {self.checkbox_var2.get()}")

    def __reset_values(self):
        logging.info("Значения UI сброшены.")
        # Resets all variable values
        self.checkbox_var.set("off")
        self.checkbox_var2.set("off")
        
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
    
    def _apply_settings(self):
        # Validate user selections
        region_col = self.region_dropdown.get().strip()
        phone_col = self.phone_dropdown.get().strip()
        filter_region = self.code_dropdown.get().strip()

        if not region_col or not phone_col or not filter_region:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            # Applies filtering and processing
            ftd_filter = "FTD" if self.checkbox_var.get() == "on" else "No FTD" if self.checkbox_var2.get() == "on" else ""
            self.data_manager.process_data(region_col, phone_col, self.FTD_COLUMN, ftd_filter)

            # Writes to Excel
            valid_file, invalid_file = self.data_manager.write_to_excel()
            
            messagebox.showinfo("Готово", f"Файлы сохранены:\n{valid_file}\n{invalid_file}")
            
            # Resets all values
            self.__reset_values()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))