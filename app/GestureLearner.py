from tkinter import Tk

from app.system.ServiceLocator_Checked import ServiceLocator_Checked


def main():
    root = Tk()
    service_locator = ServiceLocator_Checked(root)
    root.geometry("300x250+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()
