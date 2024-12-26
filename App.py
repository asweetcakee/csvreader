from UserInterface import UserInterface
from UItest import UItest
from UserInterfaceConsole import UserInterfaceConsole
import tkinter as tk
from customtkinter import *

def main():
    # root = tk.Tk()
    # app = UserInterface(root)
    # root.mainloop()
    root = CTk(fg_color="#ffffff")
    app = UItest(root)
    root.mainloop()
    #consoleUI = UserInterfaceConsole()
    #consoleUI.start()
    

if __name__ == "__main__":
    main()
