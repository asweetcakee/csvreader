import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from CSVParser import CSVParser
from DataProcessor import DataProcessor
from ExcelWriter import ExcelWriter


class UserInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Filter Tool")
        self.root.geometry("800x600")

        # Variables
        self.csv_parser = None
        self.processor = None
        self.file_path = ""
        self.params = {}

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
        # Calls helper window
        messagebox.showinfo("Readme", "Здесь будет инструкция по использованию программы.")

    def create_file_selection(self):
        # Main frame
        frame = tk.Frame(self.root, pady=10, padx=10)
        frame.pack(fill=tk.X)

        # Label and select file button
        tk.Label(frame, text="Выберите CSV файл:").grid(row=0, column=0, sticky=tk.W)
        select_btn = tk.Button(frame, text="Выбрать файл", command=self.select_file)
        select_btn.grid(row=0, column=1)

        # Text Area
        self.file_preview = tk.Text(frame, wrap=tk.NONE, state=tk.DISABLED)
        self.file_preview.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Min and max size of the TextArea
        self.file_preview.config(width=80)
        self.file_preview.config(height=10) 

        # Vertical scroll
        self.scroll_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.file_preview.yview)
        self.scroll_y.grid(row=1, column=2, sticky="ns")
        self.file_preview['yscrollcommand'] = self.scroll_y.set

        # Horizontal scroll
        self.scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.file_preview.xview)
        self.scroll_x.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.file_preview['xscrollcommand'] = self.scroll_x.set

        # Hides scroll
        self.scroll_y.grid_forget()
        self.scroll_x.grid_forget()

        # Links changes in TextArea to display scrolls
        self.file_preview.bind("<Configure>", self.on_text_change)

        # Sets up frame
        frame.grid_columnconfigure(0, weight=1, minsize=200)
        frame.grid_rowconfigure(1, weight=1)  # Allows TextArea to stick and wrap by Vertical orientation


    def on_text_change(self, event):
        # Gets TextArea content (without last newline)
        content = self.file_preview.get("1.0", "end-1c") 

        # Splits content in rows
        lines = content.splitlines()

        # Checks whether Vertical scroll should be displayed
        if len(lines) > 10:  # If lines are more than TextArea height 
            self.scroll_y.grid()  # Displays Vertical scroll
        else:
            self.scroll_y.grid_forget()  # Hides Vertical scroll

        # Checks whether Horizontal scroll should be displayed
        max_line_length = max(len(line) for line in lines) if lines else 0

        # Gets text width
        text_width = self.file_preview.winfo_width()

        if max_line_length > text_width:  # If lines length is greater than TextArea width
            self.scroll_x.grid()  # Displays Horizontal scroll
        else:
            self.scroll_x.grid_forget()  # Hides Horizontal scroll

        # Updated Horizontal scroll binding
        self.file_preview.config(xscrollcommand=self.scroll_x.set)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.file_path:
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
                    self.regions_listbox.delete(0, tk.END)  # Clears Listbox before updating

                    # Adds unique regions to the Listbox
                    for region in regions:
                        self.regions_listbox.insert(tk.END, region)
                except ValueError as e:
                    messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
            else:
                messagebox.showerror("Ошибка", "Не выбран столбец для региона.")


    
    def show_file_preview(self):
        self.file_preview.config(state=tk.NORMAL)
        self.file_preview.delete(1.0, tk.END)

        preview_text = f"Столбцы: {', '.join(self.csv_parser.data.columns)}\n"
        preview_text += self.csv_parser.data.head(3).to_string(index=False)
        self.file_preview.insert(tk.END, preview_text)

        self.file_preview.config(state=tk.DISABLED)

    def create_settings(self):
        frame = tk.Frame(self.root, pady=10, padx=10)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="1. Выберите колонку с регионами:").grid(row=0, column=0, sticky=tk.W)
        self.region_col_var = tk.StringVar()
        self.region_dropdown = ttk.Combobox(frame, textvariable=self.region_col_var)
        self.region_dropdown.grid(row=0, column=1)

        tk.Label(frame, text="2. Выберите колонку с номерами телефона:").grid(row=1, column=0, sticky=tk.W)
        self.phone_col_var = tk.StringVar()
        self.phone_dropdown = ttk.Combobox(frame, textvariable=self.phone_col_var)
        self.phone_dropdown.grid(row=1, column=1)

        tk.Label(frame, text="3. Укажите регионы для фильтрации:").grid(row=2, column=0, sticky=tk.W)
        self.regions_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=5)
        self.regions_listbox.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)

        apply_btn = tk.Button(frame, text="Применить настройки", command=self.apply_settings)
        apply_btn.grid(row=4, column=0, columnspan=2)

        # Binds handler that changes Listbox content once any value was selected in the region dropdown
        self.region_dropdown.bind("<<ComboboxSelected>>", self.update_filter_listbox)


    def apply_settings(self):
        if not self.csv_parser:
            messagebox.showerror("Ошибка", "Сначала выберите CSV файл.")
            return

        region_col = self.region_col_var.get()
        phone_col = self.phone_col_var.get()

        if not region_col or not phone_col:
            messagebox.showerror("Ошибка", "Выберите столбцы для регионов и телефонов.")
            return

        unique_regions = self.csv_parser.get_unique_regions(region_col)

        selected_regions = [self.regions_listbox.get(i) for i in self.regions_listbox.curselection()]
        if not selected_regions:
            messagebox.showerror("Ошибка", "Выберите хотя бы один регион.")
            return

        for region in selected_regions:
            code = input(f"Введите код для {region}: ")
            length = int(input(f"Введите длину номера для {region}: "))
            self.params[region] = {"code": code, "length": length}

        self.processor = DataProcessor(self.params)
        for _, row in self.csv_parser.data.iterrows():
            self.processor.process_row(str(row[region_col]), str(row[phone_col]))

        self.write_to_excel()

    def write_to_excel(self):
        writer = ExcelWriter("phone_numbers_output.xlsx")
        all_data = {**self.processor.processed_data, **self.processor.partial_data}
        writer.write_to_excel(all_data)
        messagebox.showinfo("Готово", "Файл успешно обработан и сохранён.")
