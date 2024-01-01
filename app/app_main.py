from GUI_class import GUI_class

from controller import Controller

if __name__ == "__main__":

    controller = Controller()
    gui = GUI_class(controller.handle_event)
    controller.set_gui(gui)

    gui.mainloop()

