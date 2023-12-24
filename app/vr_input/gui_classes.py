import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from threading import Thread
import time

import circuit_data
import headset_manager
import circuit_manager
from circuit_data import Warmup




class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Computer Icon
        img = Image.open('../../docs/harl_logo.png')
        icon = ImageTk.PhotoImage(img)
        self.tk.call('wm', 'iconphoto', self._w, icon)

        # Main Setup ------------------------------------------------------------
        self.title('University of Memphis | Hearing Aid Research Laboratory | Sound Localization Experiment')

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1000
        window_height = 800
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.minsize(1000,600)

        # Padding and Font Styles
        self.x_pad_main = 10
        self.y_pad_main = 10
        self.x_pad_1 = 10
        self.y_pad_1 = 10
        self.x_pad_2 = 10
        self.y_pad_2 = 10
        self.font_size = 26

        # Widgets ---------------------------------------------------------------
        self.top_frame = Top_Frame(self)
        self.top_frame.pack(side='top', fill='both', expand=True)

        self.middle_frame = Middle_Frame(self)
        self.middle_frame.pack(side='top', fill='both', expand=True)

        self.bottom_frame = Bottom_Frame(self)
        self.bottom_frame.pack(side='top', fill='both', expand=True)


        # Run ---------------------------------------------------------------------
        self.mainloop()


class Top_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Top Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(padx=parent.x_pad_main, pady=parent.y_pad_main, side='top', fill='both', expand=True)

        # Sub Frames for Top Frame
        hardware_status_frame = ctk.CTkFrame(top_frame)
        hardware_status_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='left', fill='both', expand=True)
        warmup_frame = ctk.CTkFrame(top_frame)
        warmup_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='right', fill='both', expand=True)



        # TDT Connection
        connection_status_TDT = 'TDT Hardware: Not Connected'
        text_color_TDT = 'red'
        self.tdt_status = ctk.CTkLabel(hardware_status_frame, text=connection_status_TDT, text_color=text_color_TDT, font=("default_font", parent.font_size))  # TODO: connection function
        self.tdt_status.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)
        self.reset_button_TDT = ctk.CTkButton(hardware_status_frame, text='TDT Reset', font=("default_font", parent.font_size))
        self.reset_button_TDT.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)

        # VR Connection
        connection_status_VR = 'VR Headset: Not Connected'
        text_color_VR = 'red'
        self.vr_status = ctk.CTkLabel(hardware_status_frame, text=connection_status_VR, text_color=text_color_VR, font=("default_font", parent.font_size))  # TODO: connection function
        self.vr_status.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)
        self.reset_button_VR = ctk.CTkButton(hardware_status_frame, text='VR Reset', font=("default_font", parent.font_size))
        self.reset_button_VR.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)



        # Sub Sub Frame of Warm Up
        self.warmup_frame = ctk.CTkButton(warmup_frame, text="Play Warmup", font=("default_font", parent.font_size))
        self.warmup_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)

        warmup_frame_sub = ctk.CTkFrame(warmup_frame)
        warmup_frame_sub.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='right', fill='both', expand=True)
        test1_text_color = 'gray'
        self.warmup_frame_sub = ctk.CTkLabel(warmup_frame_sub, text='Test 1', text_color=test1_text_color, font=("default_font", parent.font_size))
        self.warmup_frame_sub.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='left', fill='both', expand=True)

        test2_text_color = 'gray'
        self.warmup_frame_sub = ctk.CTkLabel(warmup_frame_sub, text='Test 2', text_color=test2_text_color, font=("default_font", parent.font_size))
        self.warmup_frame_sub.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='left', fill='both', expand=True)


        test3_text_color = 'gray'
        self.warmup_frame_sub = ctk.CTkLabel(warmup_frame_sub, text='Test 3', text_color=test3_text_color, font=("default_font", parent.font_size))
        self.warmup_frame_sub.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='left', fill='both', expand=True)

        test4_text_color = 'gray'
        self.warmup_frame_sub = ctk.CTkLabel(warmup_frame_sub, text='Test 4', text_color=test4_text_color, font=("default_font", parent.font_size))
        self.warmup_frame_sub.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='left', fill='both', expand=True)

        test5_text_color = 'gray'
        self.warmup_frame_sub = ctk.CTkLabel(warmup_frame_sub, text='Test 5', text_color=test5_text_color, font=("default_font", parent.font_size))
        self.warmup_frame_sub.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='right', fill='both', expand=True)


class Middle_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Middle Frame
        middle_frame = ctk.CTkFrame(self)
        middle_frame.pack(padx=parent.x_pad_main, pady=parent.y_pad_main, side='top', fill='both', expand=True)

        # Sub Frames for Middle Frame
        experiment_select_frame = ctk.CTkFrame(middle_frame)
        experiment_select_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='left', expand=True, fill='both')
        # stimulus_select_frame = ctk.CTkFrame(middle_frame)
        # stimulus_select_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='left', expand=True, fill='both')
        exp_metadata_frame = ctk.CTkFrame(middle_frame)
        exp_metadata_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='right', expand=True, fill='both')

        # Dropdown Box
        dropdown_values_exp = ['Select an Experiment'] + [f'Experiment {x}' for x in range(1, 21)]
        self.option_var_exp = tk.StringVar(value=dropdown_values_exp[0])  # Set initial value to the prompt text
        self.dropdown_exp = ctk.CTkOptionMenu(experiment_select_frame, variable=self.option_var_exp, values=dropdown_values_exp, font=("default_font", parent.font_size))
        self.dropdown_exp.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)

        # Manual Entry Button
        checkbox_var = ctk.IntVar()
        self.stimulus_number_frame = ctk.CTkCheckBox(experiment_select_frame, text='Manual Entry', variable=checkbox_var, font=("default_font", parent.font_size))
        self.stimulus_number_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)

        # Stimulus Dropdown Box
        dropdown_values_stim = [f'Stimulus Start Number: {x}' for x in range(1, 101)]
        self.option_var_stim = tk.StringVar(value=dropdown_values_stim[0])  # Set initial value to the prompt text
        self.dropdown_stim = ctk.CTkOptionMenu(experiment_select_frame, variable=self.option_var_stim, values=dropdown_values_stim, font=("default_font", parent.font_size))
        self.dropdown_stim.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)


        # Load Experiment Button
        self.experiment_frame = ctk.CTkButton(experiment_select_frame, text='Load Experiment', font=("default_font", parent.font_size))
        self.experiment_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='bottom', fill='both', expand=True)


        # Experiment Metadata Info Box
        self.info_label = ctk.CTkLabel(exp_metadata_frame, text="Experiment Info                                                        ", font=("default_font", parent.font_size))
        self.info_label.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=False)


class Bottom_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Bottom Frame
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(padx=parent.x_pad_main, pady=parent.y_pad_main, side='bottom', fill='both', expand=True)

        # Sub Frames for Bottom Frame
        left_frame = ctk.CTkFrame(bottom_frame)
        left_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='left', expand=True, fill='both')
        middle_frame = ctk.CTkFrame(bottom_frame)
        middle_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='left', expand=True, fill='both')
        right_frame = ctk.CTkFrame(bottom_frame)
        right_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='right', expand=True, fill='both')

        # Experiment Widgets
        left_top_frame = ctk.CTkFrame(left_frame)
        left_top_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='top', expand=True, fill='both')
        left_middle_frame = ctk.CTkFrame(left_frame)
        left_middle_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='top', expand=True, fill='both')
        left_bottom_frame = ctk.CTkFrame(left_frame)
        left_bottom_frame.pack(padx=parent.x_pad_1, pady=parent.y_pad_1, side='top', expand=True, fill='both')

        self.current_stimulus_frame = ctk.CTkLabel(left_top_frame, text='Current Simulus #:',font=("default_font", parent.font_size))
        self.current_stimulus_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='left', fill='both', expand=True)
        self.current_stimulus_frame = ctk.CTkLabel(left_top_frame, text='0',font=("default_font", parent.font_size))
        self.current_stimulus_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='right', fill='both', expand=True)

        self.total_time_frame = ctk.CTkLabel(left_middle_frame, text='Total Time:', font=("default_font", parent.font_size))
        self.total_time_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='left', fill='both', expand=True)
        self.total_time_frame = ctk.CTkLabel(left_middle_frame, text='00:00',font=("default_font", parent.font_size))
        self.total_time_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='right', fill='both', expand=True)

        self.selection_made_frame = ctk.CTkLabel(left_bottom_frame, text='Selection Made:', font=("default_font", parent.font_size))
        self.selection_made_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='left', fill='both', expand=True)
        self.selection_made_frame = ctk.CTkLabel(left_bottom_frame, text='None',font=("default_font", parent.font_size))
        self.selection_made_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='right', fill='both', expand=True)


        # Action Buttons
        self.actions_frame = ctk.CTkButton(right_frame, text='Start', font=("default_font", parent.font_size))
        self.actions_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)
        self.actions_frame = ctk.CTkButton(right_frame, text='Pause', font=("default_font", parent.font_size))
        self.actions_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)
        self.actions_frame = ctk.CTkButton(right_frame, text='End', font=("default_font", parent.font_size))
        self.actions_frame.pack(padx=parent.x_pad_2, pady=parent.y_pad_2, side='top', fill='both', expand=True)






if __name__ == "__main__":
    App()