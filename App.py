from ui.UserInterface import UserInterface
from customtkinter import *

def main():
    root = CTk(fg_color="#ffffff")
    app = UserInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
