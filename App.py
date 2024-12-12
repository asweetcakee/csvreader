from UserInterface import UserInterface
from UserInterfaceConsole import UserInterfaceConsole
import tkinter as tk

def main():
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()
    #consoleUI = UserInterfaceConsole()
    #consoleUI.start()
    

if __name__ == "__main__":
    main()
