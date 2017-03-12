# coding=utf-8

from app.modules.UI import UI
from app.system import Constants
from app.system.ServiceLocator import ServiceLocator
from app.system.ServiceLocator_Checked import ServiceLocator_Checked

if Constants.DEBUG_MODE:
    service_locator = ServiceLocator_Checked()
else:
    service_locator = ServiceLocator


def main():
    """
    The starting point of the program
    """
    ui = UI()
    ui.init(service_locator)


if __name__ == '__main__':
    main()
