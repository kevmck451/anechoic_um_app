# Main File for GUI_class


from GUI_class import GUI_class
from TDT_manager import TDT_Circuit
from VR_manager import VR_Headset_Hardware
from controller import Controller

if __name__ == "__main__":

    vr_hardware = VR_Headset_Hardware()
    tdt_hardware = TDT_Circuit()
    controller = Controller(tdt_hardware, vr_hardware)

    gui = GUI_class(controller.handle_event)
    controller.set_gui(gui)


    gui.mainloop()

