import customtkinter
from PIL import Image

from ui.ImageProcessor import ImageProcessor

class AboutAppTab:
    def __init__(self, parent):
        self.parent = parent
        
        self.image = Image.open("img/top_title_logo.png")
        self.ctk_image = customtkinter.CTkImage(light_image=self.image, dark_image=self.image, size=(90, 45))
        self.image2 = Image.open("img/asweetcake_logo.png")
        self.avatar1 = ImageProcessor.make_rounded_corners("img/asweetcake_logo.png", 5)
        self.avatar1.save("img/processed_image.png")
        self.avatar1 = customtkinter.CTkImage(light_image=self.avatar1, dark_image=self.avatar1, size=(130, 130))
        
        self.configure_tab()
        
    def configure_tab(self):
        # Top frame
        topFrame = customtkinter.CTkFrame(self.parent, fg_color="#f2f2f2")
        topFrame.grid(row=0, column=0, padx=0, pady=10, sticky="ew")
        topFrame.grid_columnconfigure(0, weight=1)
        topFrame.grid_columnconfigure(1, weight=1)
        topFrame.grid_columnconfigure(2, weight=1)
        
        avatar_frame1 = self.configure_avatar_frame(topFrame, 0)
        avatar_frame2 = self.configure_avatar_frame(topFrame, 1)
        avatar_frame3 = self.configure_avatar_frame(topFrame, 2)
        
        self.avatar_card(avatar_frame1, "asweetcake", "https://github.com/asweetcakee", 0)
        self.avatar_card(avatar_frame2, "yaneik", "https://github.com/Yaneik", 0)
        self.avatar_card(avatar_frame3, "Инструкция", "https://github.com/Yaneik", 0)
    
    def configure_avatar_frame(self, root_frame, column):
        # Outer frame with rounded corners
        frame = customtkinter.CTkFrame(root_frame, fg_color="#d9d9d9", corner_radius=10, width=150)
        frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")  # Adjust padding here for spacing around the frame
        frame.grid_columnconfigure(0, weight=0)  # Ensure elements inside the frame are centered
        return frame
    
    def avatar_card(self, frame, title, link, label_column):
        # Label with an image (avatar) and rounded corners
        label = customtkinter.CTkLabel(frame, text="", width=120, height=120, image=self.avatar1, fg_color="#d9d9d9", corner_radius=5)
        label.grid(row=0, column=label_column, padx=5, pady=(10, 0))  # Add padding to separate it from the frame edges
        # Button beneath the image with proper padding
        button = customtkinter.CTkButton(frame, text=title, corner_radius=5, fg_color="#9FACF6", height=50, width=130, text_color="#0F1B60", font=("Rubik", 16))
        button.grid(row=1, column=0, padx=5, pady=(5, 5))  # Add top padding to separate from the label
