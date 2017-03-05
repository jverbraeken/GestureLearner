from tkinter import Tk

from app.GestureLearner import GestureLearner


def main():
    root = Tk()
    ex = GestureLearner(root)
    root.geometry("300x250+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()
