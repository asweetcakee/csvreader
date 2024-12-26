import tkinter as tk
import customtkinter
from PIL import Image
from tkinter import filedialog, messagebox
from CSVParser import CSVParser
from DataProcessor import DataProcessor
from ExcelWriter import ExcelWriter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class UItest:
    def __init__(self, root):
        self.root = root

        # Variables
        self.csv_parser = None
        self.processed_data = None
        self.excel_writer = None
        self.file_path = ""
        self.checkbox_vars = {}
        self.selected_region = ""
        
        self.image = Image.open("img/top_title_logo.png")
        self.ctk_image = customtkinter.CTkImage(light_image=self.image, dark_image=self.image, size=(90, 45))
        
        self.configure_window() 
        self.configure_tabview()       
        
    def configure_window(self):
        self.root.title("CSV Reader")
        self.root.geometry(f"{600}x{530}")
    
    def configure_tabview(self):
        self.tabview = customtkinter.CTkTabview(self.root, width=580, fg_color="#f7f5f5", text_color="#0F1B60", segmented_button_fg_color="#dedede", segmented_button_selected_color="#9FACF6", segmented_button_unselected_color="#dedede")
        self.tabview.grid(row=0, column=0, padx=(10, 0), pady=(10, 10), sticky="nsew")
        
        tabTitle_Auto = "Автоматическая обработка"
        tabTitle_Manual = "Ручная обработка"
        tabTitle_AboutApp = "О приложении"
        
        self.tabview.add(tabTitle_Auto)
        self.tabview.add(tabTitle_Manual)
        self.tabview.add(tabTitle_AboutApp)
        
        self.configure_auto_tab(self.tabview, tabTitle_Auto)
        self.configure_manual_tab(self.tabview, tabTitle_Manual)
            
    def configure_auto_tab(self, tabview, title):
        # Sets tab on row 0, expand = TRUE
        auto_tab = tabview.tab(title)
        auto_tab.grid_columnconfigure(0, weight=1)
        
        # Top frame
        topFrame = customtkinter.CTkFrame(auto_tab, fg_color="#f2f2f2")
        topFrame.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")
        topFrame.grid_columnconfigure(0, weight=0)  # Left column for label
        topFrame.grid_columnconfigure(1, weight=1)  # Right column for button
        # Logo    
        label = customtkinter.CTkLabel(topFrame, text="", width=120, height=100, image=self.ctk_image, fg_color="#d9d9d9", corner_radius=5)
        label.grid(row=0, column=0, padx=10, pady=0)
        # Selection Button
        select_file_button = customtkinter.CTkButton(topFrame, text="Выбрать файл", height=100, corner_radius=5, fg_color="#9FACF6", text_color="#0F1B60", font=("Rubik", 26), command=self.select_file)
        select_file_button.grid(row=0, column=1, padx=10, pady=0, sticky="ew")
        # Text Box
        self.auto_text_box = customtkinter.CTkTextbox(auto_tab, width=540, height=150, wrap="none")
        self.auto_text_box.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.auto_text_box.configure(state="disabled")
        # Processing button                
        process_button = customtkinter.CTkButton(auto_tab, text="Обработать данные", corner_radius=5, fg_color="#9FACF6", height=50, text_color="#0F1B60", font=("Rubik", 20), command=self.apply_auto_settings)
        process_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
    
    def configure_manual_tab(self, tabview, title):
        # Sets tab on row 0, expand = TRUE
        manual_tab = tabview.tab(title)
        manual_tab.grid_columnconfigure(0, weight=1)
        # Top frame
        topFrame = customtkinter.CTkFrame(manual_tab, fg_color="#f2f2f2")
        topFrame.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")
        topFrame.grid_columnconfigure(0, weight=0)  # Left column for label
        topFrame.grid_columnconfigure(1, weight=1)  # Right column for button
        # Logo
        label = customtkinter.CTkLabel(topFrame, text="", width=120, height=100, image=self.ctk_image, fg_color="#d9d9d9", corner_radius=5)
        label.grid(row=0, column=0, padx=10, pady=0)
        # Selection Button
        select_file_button = customtkinter.CTkButton(topFrame, text="Выбрать файл", height=100, corner_radius=5, fg_color="#9FACF6", command=self.select_file, text_color="#0F1B60", font=("Rubik", 26))
        select_file_button.grid(row=0, column=1, padx=10, pady=0, sticky="ew")
        # Text box
        self.manual_text_box = customtkinter.CTkTextbox(manual_tab, width=540, height=150, wrap="none")
        self.manual_text_box.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.manual_text_box.configure(state="disabled")
        
        # Bottom Frame
        bottomFrame = customtkinter.CTkFrame(manual_tab, fg_color="#f2f2f2", height=50)
        bottomFrame.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
        bottomFrame.grid_columnconfigure(0, weight=1)  # Left column for label
        bottomFrame.grid_columnconfigure(1, weight=1)  # Right column for button
        # Labels on the left
        label_1 = customtkinter.CTkLabel(bottomFrame, text="1. Выберите колонку с регионом", font=("Rubik", 16))
        label_1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        label_2 = customtkinter.CTkLabel(bottomFrame, text="2. Выберите колонку с номером", font=("Rubik", 16))
        label_2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        label_3 = customtkinter.CTkLabel(bottomFrame, text="3. Укажите регион для фильтрации", font=("Rubik", 16))
        label_3.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        # Input fields on the right
        self.region_dropdown = customtkinter.CTkComboBox(bottomFrame, values=[""], border_color="#9FACF6", dropdown_fg_color="#ffffff", dropdown_hover_color="#9FACF6", button_color="#6376e0", command=self.update_code_dropdown)
        self.region_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.phone_dropdown = customtkinter.CTkComboBox(bottomFrame, values=[""], border_color="#9FACF6", dropdown_fg_color="#ffffff", dropdown_hover_color="#9FACF6", button_color="#6376e0")
        self.phone_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.code_dropdown = customtkinter.CTkComboBox(bottomFrame, values=[""], border_color="#9FACF6", dropdown_fg_color="#ffffff", dropdown_hover_color="#9FACF6", button_color="#6376e0")
        self.code_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        process_button = customtkinter.CTkButton(manual_tab, text="Обработать данные", corner_radius=5, fg_color="#9FACF6", height=50, command=self.apply_settings, text_color="#0F1B60", font=("Rubik", 20))
        process_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.file_path:
            print("Files was not selected.")
            return

        try:
            self.csv_parser = CSVParser(self.file_path)
            self.csv_parser.read_csv()
            self.show_file_preview()
            
            self.update_dropdowns()  # Depends on dropdowns value
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
            
    def show_file_preview(self):
        if hasattr(self, 'auto_text_box'):
            self.auto_text_box.configure(state="normal")
            self.auto_text_box.delete("1.0", "end")
            preview_text = self.csv_parser.data.head(3).to_string(index=False)
            self.auto_text_box.insert("end", preview_text)
            self.auto_text_box.configure(state="disabled")
        if hasattr(self, 'manual_text_box'):
            self.manual_text_box.configure(state="normal")
            self.manual_text_box.delete("1.0", "end")
            self.manual_text_box.insert("end", preview_text)
            self.manual_text_box.configure(state="disabled")
        
    def update_dropdowns(self):
        if self.csv_parser and self.csv_parser.data is not None:
            columns = self.csv_parser.data.columns.tolist()
            self.region_dropdown.configure(values=columns)
            self.phone_dropdown.configure(values=columns)
    
    def update_code_dropdown(self, event=None):
        """Обновляет ComboBox с уникальными регионами."""
        if self.csv_parser.data is not None:
            # Gets selected column from region_dropdown
            selected_column = self.region_dropdown.get()

            print("--T selected col: ")
            print(selected_column)
            
            if selected_column:
                try:
                    # Get unique regions
                    regions = self.csv_parser.get_unique_regions(selected_column)
                    print("--T regions: ")
                    print(regions)
                    # Populate the region dropdown with unique regions
                    self.code_dropdown.configure(values=regions)
                    self.selected_region = regions
                    
                except ValueError as e:
                    messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
            else:
                messagebox.showerror("Ошибка", "Не выбран столбец для региона.")
    
    def update_auto_code_dropdown(self):
        """Обновляет ComboBox с уникальными регионами."""
        if self.csv_parser.data is not None:            
            try:
                # Get unique regions
                regions = self.csv_parser.get_unique_regions("country")
                print("--T regions: ")
                print(regions)
                # Populate the region dropdown with unique regions
                self.code_dropdown.configure(values=regions)
                self.selected_region = regions
                
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
    
    def apply_settings(self):
        if not self.csv_parser:
            messagebox.showerror("Ошибка", "Сначала выберите CSV файл.")
            return

        region_col = self.region_dropdown.get().strip()
        phone_col = self.phone_dropdown.get().strip()
        filter_region = self.code_dropdown.get().strip()

        if not region_col or not phone_col:
            messagebox.showerror("Ошибка", "Выберите столбцы для регионов и телефонов.")
            return

        if not filter_region:
            messagebox.showerror("Ошибка", "Выберите хотя бы один регион.")
            return
        
        try:
            # Performs filtering logic
            self.start_processing(filter_region, phone_col)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Обработка провалилась: {e}")

    def apply_auto_settings(self):
        if not self.csv_parser:
            messagebox.showerror("Ошибка", "Сначала выберите CSV файл.")
            return

        self.update_auto_code_dropdown()
        
        region_col = "country"
        phone_col = "phone"
        filter_region = self.selected_region

        print("--T | country: " + region_col)
        print("--T | phone: " + phone_col)
        print("--T | filter: ")
        print(filter_region)
        
        try:
            # Performs filtering logic
            self.start_processing(filter_region, phone_col)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Обработка провалилась: {e}")
    
    def start_processing(self, selected_regions, phone_col):
        self.processed_data = DataProcessor(selected_regions)
               
        # Makes sure self.csv_parser is safe to use and not None
        if self.csv_parser and self.csv_parser.data is not None:
            for _, row in self.csv_parser.data.iterrows():
                self.processed_data.process_row(row[phone_col])
            self.write_to_excel()
        else:
            print("Ошибка", "Данные CSV не загружены.")
        
        # Closes filtering window after data proccessing is finished
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy()
        
        # Clears all variable values
        self.file_path = ""
        self.csv_parser = None
        self.params = {}
        
        # Clears dropdown values
        self.region_dropdown.set('') 
        self.region_dropdown['values'] = []
        self.phone_dropdown.set('')
        self.phone_dropdown['values'] = []
        self.code_dropdown.set('')
        self.code_dropdown['values'] = []
        
        # Clears text widget values
        if hasattr(self, 'auto_text_box'):
            self.auto_text_box.configure(state="normal")
            self.auto_text_box.delete("1.0", "end")
            self.auto_text_box.configure(state="disabled")
        if hasattr(self, 'manual_text_box'):
            self.manual_text_box.configure(state="normal")
            self.manual_text_box.delete("1.0", "end")
            self.manual_text_box.configure(state="disabled")
            
    def write_to_excel(self):
        valid_writer = ExcelWriter("valid_phones.xlsx")
        invalid_writer = ExcelWriter("invalid_phones.xlsx")
        valid_writer.write_to_excel(self.processed_data.valid_numbers)
        invalid_writer.write_to_excel(self.processed_data.invalid_numbers)
        print("Готово", "Файл успешно обработан и сохранён.")