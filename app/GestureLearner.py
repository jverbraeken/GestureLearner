# coding=utf-8

from app.modules.UI import UI
from app.system.ServiceLocator_Checked import ServiceLocator_Checked

service_locator = ServiceLocator_Checked()


def main():
    """
    The starting point of the program
    """
    ui = UI()
    ui.init(service_locator)


if __name__ == '__main__':
    main()
