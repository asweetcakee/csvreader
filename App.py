from ui.UserInterface import UserInterface
from ui.UItest import UItest
from ui.UserInterfaceConsole import UserInterfaceConsole
from customtkinter import *

def main():
    # root = tk.Tk()
    # app = UserInterface(root)
    # root.mainloop()
    # root = CTk(fg_color="#ffffff")
    # app = UItest(root)
    # root.mainloop()
    root = CTk(fg_color="#ffffff")
    app = UserInterface(root)
    root.mainloop()
    #consoleUI = UserInterfaceConsole()
    #consoleUI.start()
    

if __name__ == "__main__":
    main()
