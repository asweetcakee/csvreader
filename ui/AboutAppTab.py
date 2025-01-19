from tkinter import messagebox
import customtkinter
from PIL import Image

from ui.ImageProcessor import ImageProcessor
from logger.LogManager import LogManager

class AboutAppTab:
    def __init__(self, parent):
        self.parent = parent
        
        self.image = Image.open("img/top_title_logo.png")
        self.ctk_image = customtkinter.CTkImage(light_image=self.image, dark_image=self.image, size=(90, 45))
        self.image2 = Image.open("img/asweetcake_logo.png")
        self.avatar1 = ImageProcessor.make_rounded_corners("img/asweetcake_logo.png", 5)
        self.avatar1.save("img/processed_image.png")
        self.avatar1 = customtkinter.CTkImage(light_image=self.avatar1, dark_image=self.avatar1, size=(130, 130))
        
        # Label status text
        self.sent_status_lbl_text = ""
        
        # Initializes the log manager
        self.log_manager = LogManager(app_name="CSVReader")
        
        # CONSTANTS
        self.AUTHOR_NICKNAME = "asweetcake"
        self.AUTHOR_GIT = "https://github.com/asweetcakee"
        
        self.__configure_tab()
        
    def __configure_tab(self):
        # Top frame
        topFrame = customtkinter.CTkFrame(self.parent, fg_color="#f2f2f2")
        topFrame.grid(row=0, column=0, padx=0, pady=10, sticky="ew")
        topFrame.grid_columnconfigure(0, weight=0)
        topFrame.grid_columnconfigure(1, weight=1)
        
        # Avatar frame
        avatar_frame1 = self.__configure_avatar_frame(topFrame, 0)
        self.__avatar_card(avatar_frame1, self.AUTHOR_NICKNAME, self.AUTHOR_GIT, 0)
        
        # Buttons frame
        self.__configure_buttons_frame(topFrame, 0, 1)
        
        # Bottom frame
        self.__configure_bottom_frame(self.parent, 1, 0)
        
    def __configure_avatar_frame(self, root_frame, column):
        # Outer frame with rounded corners
        frame = customtkinter.CTkFrame(root_frame, fg_color="#d9d9d9", corner_radius=10, width=150)
        frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        frame.grid_columnconfigure(0, weight=0)  # Ensures elements inside the frame are centered
        return frame
    
    def __avatar_card(self, frame, title, link, label_column):
        label = customtkinter.CTkLabel(frame, text="", width=120, height=120, image=self.avatar1, fg_color="#d9d9d9", corner_radius=5)
        label.grid(row=0, column=label_column, padx=5, pady=(10, 0))
        
        button = customtkinter.CTkButton(frame, text=title, corner_radius=5, fg_color="#9FACF6", height=50, width=130, text_color="#0F1B60", font=("Rubik", 16))
        button.grid(row=1, column=0, padx=5, pady=(5, 5))

    def __configure_buttons_frame(self, root_frame, row, column):
        # Buttons frame
        buttonsFrame = customtkinter.CTkFrame(root_frame, fg_color="#f2f2f2")
        buttonsFrame.grid(row=row, column=column, padx=0, pady=0, sticky="ew")
        
        # Buttons
        readme_txt = self.__configure_button(buttonsFrame, "Руководство.txt", 100, 410, "#9FACF6", "#0F1B60", ("Rubik", 26), 0, 0, self.__readme_txt)
        readme_docx = self.__configure_button(buttonsFrame, "Руководство.docx", 100, 410, "#9FACF6", "#0F1B60", ("Rubik", 26), 1, 0, self.__readme_docx)

    def __configure_button(self, root_frame, title, height, width, background_color, text_color, font, row, column, command) -> customtkinter.CTkButton:
        new_button = customtkinter.CTkButton(
            root_frame, text=title, height=height, width= width, corner_radius=5,
            fg_color=background_color, text_color=text_color, font=font,
            command=command
        )
        new_button.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
        return new_button
    
    def __configure_bottom_frame(self, root_frame, row, column):
        frame = customtkinter.CTkFrame(root_frame, fg_color="#f2f2f2")
        frame.grid(row=row, column=column, padx=0, pady=0, sticky="ew")
        
        license_button = self.__configure_button(frame, "Лицензия", 100, 250, "#9FACF6", "#0F1B60", ("Rubik", 20), 0, 0, self.__license)
        send_logs_button = self.__configure_button(frame, "Выгрузить логи", 100, 310, "#9FACF6", "#0F1B60", ("Rubik", 20), 0, 1, self.__retrieve_logs)
        
        sent_status_label = customtkinter.CTkLabel(frame, text=self.sent_status_lbl_text, font=("Rubik", 20))
        sent_status_label.grid(row=1, column=1, sticky="ew")
    
    def __readme_txt(self):
        pass
    
    def __readme_docx(self):
        pass
    
    def __license(self):
        pass
    
    def __retrieve_logs(self):
        """
        Archives and retrieves log files using LogManager.
        """
        try:
            self.log_manager.archive_logs()
            self.sent_status_lbl_text = "Логи успешно заархивированы!"
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось извлечь логи: {e}")