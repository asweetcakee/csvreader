import customtkinter
from ui.AutoProcessingTab import AutoProcessingTab
from ui.ManualProcessingTab import ManualProcessingTab
from ui.AboutAppTab import AboutAppTab

class TabViewManager:
    def __init__(self, root):
        self.root = root
        self.tabview = customtkinter.CTkTabview(
            self.root, width=580, fg_color="#f7f5f5", text_color="#0F1B60",
            segmented_button_fg_color="#dedede", segmented_button_selected_color="#9FACF6",
            segmented_button_unselected_color="#dedede" 
        )
        self.tabview.grid(row=0, column=0, padx=(10, 0), sticky="nsew")
        self.create_tabs()
        
    def create_tabs(self):
        tab_titles = {
            "Автоматическая обработка": AutoProcessingTab,
            "Ручная обработка": ManualProcessingTab,
            "О приложении": AboutAppTab
        }
        
        for title, TabClass in tab_titles.items():
            self.tabview.add(title)
            if TabClass:
                TabClass(self.tabview.tab(title))
        