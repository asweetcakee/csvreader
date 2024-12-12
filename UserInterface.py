import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from CSVParser import CSVParser
from DataProcessor import DataProcessor
from ExcelWriter import ExcelWriter


class UserInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Filter Tool")
        self.root.geometry("600x400")

        # Variables
        self.csv_parser = None
        self.processed_data = None
        self.excel_writer = None
        self.file_path = ""
        self.checkbox_vars = {}

        # Creating an interface
        self.create_interface()

    def create_interface(self):
        # Top panel
        self.create_top_panel()

        # File selection
        self.create_file_selection()

        # Params settings
        self.create_settings()

    def create_top_panel(self):
        frame = tk.Frame(self.root, bg="lightblue", height=50)
        frame.pack(fill=tk.X)

        logo = tk.Label(frame, text="🌟", font=("Arial", 24), bg="lightblue")
        logo.pack(side=tk.LEFT, padx=10)

        title = tk.Label(frame, text="CSV Filter Tool", font=("Arial", 16, "bold"), bg="lightblue")
        title.pack(side=tk.LEFT)

        readme_btn = tk.Button(frame, text="Readme.txt", command=self.open_readme)
        readme_btn.pack(side=tk.RIGHT, padx=10)

    def open_readme(self):
        # !!!!!!!!!!!!! Add a function that opens README.docx !!!!!!!!!!!!
        # Calls helper window
        messagebox.showinfo("Readme", "Здесь будет инструкция по использованию программы.")

    def create_file_selection(self):
        # Main frame
        frame = tk.Frame(self.root, pady=20, padx=20)
        frame.pack(fill=tk.X)

        # Label and select file button
        tk.Label(frame, text="Выберите CSV файл:").grid(row=0, column=0, sticky=tk.W)
        select_btn = tk.Button(frame, text="Выбрать файл", command=self.select_file)
        select_btn.grid(row=0, column=0, sticky=tk.E)

        # Frame for a Text with fixed sizes
        text_frame = tk.Frame(frame, width=560, height=100)
        text_frame.grid(row=1, column=0, sticky="we")
        text_frame.grid_propagate(False)  # Disables auto wrap on parent frame

        # Horizontal frame
        scroll_x = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        scroll_x.grid(row=1, column=0, sticky="we")

        # Text with a fixed size
        self.file_preview = tk.Text(text_frame, wrap=tk.NONE, state=tk.DISABLED, xscrollcommand=scroll_x.set, height=5)
        self.file_preview.grid(row=0, column=0, sticky="nsew")

        # Attaches scroll to the Text widget
        scroll_x.config(command=self.file_preview.xview)

        # Sets up Text sizes according to text_frame
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
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

    def update_dropdowns(self):
        """Обновляет выпадающие списки с названиями столбцов."""
        if self.csv_parser.data is not None:
            columns = self.csv_parser.data.columns.tolist() 
            self.region_dropdown['values'] = columns  # Updates region dropdown 
            self.phone_dropdown['values'] = columns  # Updates phone dropdown
    
    def update_filter_listbox(self, event=None):
        """Обновляет Listbox с уникальными регионами."""
        if self.csv_parser.data is not None:
            # Gets selected column out of dropdown
            selected_column = self.region_dropdown.get()

            if selected_column:
                try:
                    # Gets unique regions
                    regions = self.csv_parser.get_unique_regions(selected_column)
                    # Refreshes before updating
                    for widget in self.checkbox_inner_frame.winfo_children():
                        widget.grid_forget()

                    # Adds unique regions to the Listbox
                    for i, region in enumerate(regions):
                        var = tk.BooleanVar()
                        checkbox = tk.Checkbutton(self.checkbox_inner_frame, text=region, variable=var)
                        checkbox.grid(row=i+2, column=0, sticky=tk.W)
                        self.checkbox_vars[region] = var                        

                    # Обновляем размер Canvas в зависимости от количества чекбоксов
                    # Updates Canvas size basing on checkboxes quantity
                    self.checkbox_inner_frame.update_idletasks()
                    self.canvas.config(scrollregion=self.canvas.bbox("all"))
                    
                except ValueError as e:
                    messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
            else:
                messagebox.showerror("Ошибка", "Не выбран столбец для региона.")
    
    def show_file_preview(self):
        self.file_preview.config(state=tk.NORMAL)
        self.file_preview.delete(1.0, tk.END)

        preview_text = self.csv_parser.data.head(3).to_string(index=False)
        self.file_preview.insert(tk.END, preview_text)

        self.file_preview.config(state=tk.DISABLED)

    def create_settings(self):
        frame = tk.Frame(self.root, pady=10, padx=10)
        frame.pack(fill=tk.X)

        # Dropdown
        dropdown_frame = tk.Frame(frame, width=200, height=100, pady=10, padx=10)
        dropdown_frame.grid(row=0, column=0, sticky="n")
        
        tk.Label(dropdown_frame, text="1. Выберите колонку с регионами:").grid(row=0, column=0, sticky=tk.W)
        self.region_col_var = tk.StringVar()
        self.region_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.region_col_var)
        self.region_dropdown.grid(row=0, column=1, sticky=tk.W)

        tk.Label(dropdown_frame, text="2. Выберите колонку с номерами телефона:").grid(row=1, column=0, sticky=tk.W)
        self.phone_col_var = tk.StringVar()
        self.phone_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.phone_col_var)
        self.phone_dropdown.grid(row=1, column=1, sticky=tk.W)

        # Checkbox
        checkbox_frame_main = tk.Frame(frame, width=100, height=100, pady=10, padx=10,)
        checkbox_frame_main.grid(row=0, column=1, sticky="n")
        
        tk.Label(checkbox_frame_main, text="3. Укажите регионы для фильтрации:", wraplength=150, anchor=tk.W).grid(row=0, column=0, sticky=tk.W)
        
        self.checkbox_frame = tk.Frame(checkbox_frame_main, width=150, height=100, pady=10, padx=10)
        self.checkbox_frame.grid(row=1, column=0, sticky="nw")
        
        # Creates Canvas for scroll
        self.canvas = tk.Canvas(self.checkbox_frame, width=100, height=100)
        self.canvas.grid(row=0, column=0, sticky="n")

        # Vertical scrollbar
        scroll_y = tk.Scrollbar(self.checkbox_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")

        self.canvas.config(yscrollcommand=scroll_y.set)

        # Frame inside canvas that holds checkboxes
        self.checkbox_inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.checkbox_inner_frame, anchor="nw")
        
        apply_btn = tk.Button(frame, text="4. Обработать данные", command=self.apply_settings)
        apply_btn.grid(row=0, column=0, sticky="ew")

        # Binds handler that changes Listbox content once any value was selected in the region dropdown
        self.region_dropdown.bind("<<ComboboxSelected>>", self.update_filter_listbox)

    def apply_settings(self):       
        if not self.csv_parser:
            messagebox.showerror("Ошибка", "Сначала выберите CSV файл.")
            return

        self.region_col = self.region_col_var.get().strip()
        self.phone_col = self.phone_col_var.get().strip()
        
        if not self.region_col or not self.phone_col:
            messagebox.showerror("Ошибка", "Выберите столбцы для регионов и телефонов.")
            return

        selected_regions = [region for region, var in self.checkbox_vars.items() if var.get()]
                
        if not selected_regions:
            messagebox.showerror("Ошибка", "Выберите хотя бы один регион.")
            return

        self.start_processing(selected_regions)
               
    def start_processing(self, selected_regions):
        self.processed_data = DataProcessor(selected_regions)
        
        # Makes sure self.csv_parser is safe to use and not None
        if self.csv_parser and self.csv_parser.data is not None:
            for _, row in self.csv_parser.data.iterrows():
                self.processed_data.process_row(row[self.phone_col])
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
        self.checkbox_vars = {}
        
        # Clears dropdown values
        self.region_col_var.set('')  
        self.phone_col_var.set('')   
        
        self.region_dropdown.set('') 
        self.region_dropdown['values'] = []
        self.phone_dropdown.set('')
        self.phone_dropdown['values'] = []
        
        # Clears text widget values
        if hasattr(self, 'file_preview'):
            self.file_preview.config(state=tk.NORMAL)
            self.file_preview.delete(1.0, tk.END)
            self.file_preview.config(state=tk.DISABLED)
            
        # Clears checkbox values
        for widget in self.checkbox_inner_frame.winfo_children():
            widget.destroy()


    def write_to_excel(self):
        writer_valid = ExcelWriter("valid_phones.xlsx")
        writer_invalid = ExcelWriter("invalid_phones.xlsx") 
        writer_valid.write_to_excel({**self.processed_data.valid_numbers})
        writer_invalid.write_to_excel({**self.processed_data.invalid_numbers})
        print("Готово", "Файл успешно обработан и сохранён.")   
