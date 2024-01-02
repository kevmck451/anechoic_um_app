from Main_Window import Main_Window
from controller import Controller

if __name__ == "__main__":

    controller = Controller()
    gui = Main_Window(controller.handle_event)

    controller.set_gui(gui)


    gui.mainloop()

