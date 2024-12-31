from ui.TabViewManager import TabViewManager

class UserInterface:
    def __init__(self, root):
        self.root = root
        self.configure_window()
        self.tab_manager = TabViewManager(self.root)
        
    def configure_window(self):
        self.root.title("CSV Reader")
        self.root.geometry(f"{600}x{530}")
        
    