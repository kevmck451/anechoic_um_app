import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from threading import Thread
import time

import circuit_data
import headset_manager
import circuit_manager
from circuit_data import Warmup



def run_app_1():
    def start_action():
        # Implement what happens when Start is clicked
        pass

    def pause_action():
        # Implement what happens when Pause is clicked
        pass

    def stop_action():
        # Implement what happens when Stop is clicked
        pass

    def update_display():
        # Update the display with the user input
        user_input_display.config(text=user_input.get())

    # Create the main window
    root = tk.Tk()
    root.title("UM Anechoic Chamber Experiment")

    # Set window size (width x height)
    root.geometry("800x800")  # Width = 400px, Height = 300px

    # Number display
    number_display = tk.Label(root, text="Number: 0")
    number_display.pack()

    # User input box
    user_input = tk.Entry(root)
    user_input.pack()

    # User input display
    user_input_display = tk.Label(root, text="")
    user_input_display.pack()

    # Start button
    start_button = tk.Button(root, text="Start", command=start_action)
    start_button.pack()

    # Pause button
    pause_button = tk.Button(root, text="Pause", command=pause_action)
    pause_button.pack()

    # Stop button
    stop_button = tk.Button(root, text="Stop", command=stop_action)
    stop_button.pack()

    # Update display button
    update_button = tk.Button(root, text="Update Display", command=update_display)
    update_button.pack()

    # Start the main loop
    root.mainloop()



class App(ctk.CTk):

    def __init__(self, warmup_class):
        super().__init__()

        self.title("University of Memphis | Hearing Aid Research Laboratory | Sound Localization Experiment")
        self.geometry("1400x800")

        self.x_pad_main = 10
        self.y_pad_main = 10
        self.x_pad_1 = 10
        self.y_pad_1 = 10
        self.x_pad_2 = 10
        self.y_pad_2 = 10
        self.font_size = 20

        self.Warmup_Class = warmup_class

        # Top Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(padx=self.x_pad_main, pady=self.y_pad_main, side='top', fill='both', expand=True)

        # Sub Frames for Top Frame
        hardware_status_frame = ctk.CTkFrame(top_frame)
        hardware_status_frame.pack(padx=self.x_pad_1, pady=self.y_pad_1, side='left', fill='both', expand=True)
        warmup_frame = ctk.CTkFrame(top_frame)
        warmup_frame.pack(padx=self.x_pad_1, pady=self.y_pad_1, side='right', fill='both', expand=True)



        # Hardware Connection Indicators
        if circuit_manager.TDT_connection(0):
            connection_status = 'TDT Hardware: Connected'
            text_color = 'green'
        else:
            connection_status = 'TDT Hardware: Not Connected'
            text_color = 'red'

        self.tdt_status = ctk.CTkLabel(hardware_status_frame, text=connection_status, text_color=text_color, font=("default_font", self.font_size))  # TODO: connection function
        self.tdt_status.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='top', fill='both', expand=True)


        if headset_manager.headset_connection():
            connection_status = 'VR Headset: Connected'
            text_color = 'green'
        else:
            connection_status = 'VR Headset: Not Connected'
            text_color = 'red'

        self.vr_status = ctk.CTkLabel(hardware_status_frame, text=connection_status, text_color=text_color, font=("default_font", self.font_size))  # TODO: connection function
        self.vr_status.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='top', fill='both', expand=True)

        # Reset Button
        self.reset_button = ctk.CTkButton(hardware_status_frame, text='Reset', font=("default_font", self.font_size), command=lambda:print('Resetting'))
        self.reset_button.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='bottom', fill='both', expand=True)

        warmup_thread = Thread(target=self.Warmup_Class.start_warmup)

        # Warmup Widgets
        self.warmup_frame = ctk.CTkButton(warmup_frame, text="Play Warmup", font=("default_font", self.font_size), command=warmup_thread.start)
        self.warmup_frame.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='top', fill='both', expand=True)

        # Visual of Five Selections

        # Sub Sub Frame of Warm Up
        warmup_frame_sub = ctk.CTkFrame(warmup_frame)
        warmup_frame_sub.pack(padx=self.x_pad_1, pady=self.y_pad_1, side='right', fill='both', expand=True)

        print(self.Warmup_Class.test1_answered)

        if self.Warmup_Class.test1_answered:
            if self.Warmup_Class.test1:
                test1_text_color = 'green'
            else: test1_text_color = 'red'
        else:
            test1_text_color = 'gray'
        self.warmup_frame_sub = ctk.CTkLabel(warmup_frame_sub, text='Test 1', text_color=test1_text_color, font=("default_font", self.font_size))
        self.warmup_frame_sub.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='left', fill='both', expand=True)

        if self.Warmup_Class.test2_answered:
            if self.Warmup_Class.test2:
                test2_text_color = 'green'
            else: test2_text_color = 'red'
        else:
            test2_text_color = 'gray'
        self.warmup_frame_sub = ctk.CTkLabel(warmup_frame_sub, text='Test 2', text_color=test2_text_color, font=("default_font", self.font_size))
        self.warmup_frame_sub.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='left', fill='both', expand=True)

        if self.Warmup_Class.test3_answered:
            if self.Warmup_Class.test3:
                test3_text_color = 'green'
            else: test3_text_color = 'red'
        else:
            test3_text_color = 'gray'
        self.warmup_frame_sub = ctk.CTkLabel(warmup_frame_sub, text='Test 3', text_color=test3_text_color, font=("default_font", self.font_size))
        self.warmup_frame_sub.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='left', fill='both', expand=True)

        if self.Warmup_Class.test4_answered:
            if self.Warmup_Class.test4:
                test4_text_color = 'green'
            else: test4_text_color = 'red'
        else:
            test4_text_color = 'gray'
        self.warmup_frame_sub = ctk.CTkLabel(warmup_frame_sub, text='Test 4', text_color=test4_text_color, font=("default_font", self.font_size))
        self.warmup_frame_sub.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='left', fill='both', expand=True)

        if self.Warmup_Class.test5_answered:
            if self.Warmup_Class.test5:
                test5_text_color = 'green'
            else: test5_text_color = 'red'
        else:
            test5_text_color = 'gray'
        self.warmup_frame_sub = ctk.CTkLabel(warmup_frame_sub, text='Test 5', text_color=test5_text_color, font=("default_font", self.font_size))
        self.warmup_frame_sub.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='right', fill='both', expand=True)



        # Middle Frame
        middle_frame = ctk.CTkFrame(self)
        middle_frame.pack(padx=self.x_pad_main, pady=self.y_pad_main, side='top', fill='both', expand=True)

        # Sub Frames for Middle Frame
        stimulus_frame = ctk.CTkFrame(middle_frame)
        stimulus_frame.pack(padx=self.x_pad_1, pady=self.y_pad_1, side='left', expand=True, fill='both')
        exp_metadata_frame = ctk.CTkFrame(middle_frame)
        exp_metadata_frame.pack(padx=self.x_pad_1, pady=self.y_pad_1, side='right', expand=True, fill='both')

        # Description
        description_text = 'Select Experiment to Load'
        description_label = ctk.CTkLabel(stimulus_frame, text=description_text, font=("default_font", self.font_size))
        description_label.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='top', fill='both', expand=True)

        # Dropdown Box
        dropdown_values=[f'Experiment {x}' for x in range(1, 21)]
        self.option_var = tk.StringVar()
        self.dropdown = ctk.CTkOptionMenu(stimulus_frame, variable=self.option_var, values=dropdown_values, font=("default_font", self.font_size))
        self.dropdown.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='top', fill='both', expand=True)
        self.dropdown.bind('<Configure>', self.update_info)

        # Load Experiment Button
        self.experiment_frame = ctk.CTkButton(stimulus_frame, text='Load Experiment', font=("default_font", self.font_size),command=circuit_data.test_warmup_data)
        self.experiment_frame.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='bottom', fill='both', expand=True)

        # Experiment Metadata Info Box
        self.info_label = ctk.CTkLabel(exp_metadata_frame, text="Experiment Info:", font=("default_font", self.font_size))
        self.info_label.pack(expand=True)


        # Bottom Frame
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(padx=self.x_pad_main, pady=self.y_pad_main, side='bottom', fill='both', expand=True)

        # Sub Frames for Bottom Frame
        stimulus_number_frame = ctk.CTkFrame(bottom_frame)
        stimulus_number_frame.pack(padx=self.x_pad_1, pady=self.y_pad_1, side='left', expand=True, fill='both')
        exp_widgets_frame = ctk.CTkFrame(bottom_frame)
        exp_widgets_frame.pack(padx=self.x_pad_1, pady=self.y_pad_1, side='left', expand=True, fill='both')
        actions_frame = ctk.CTkFrame(bottom_frame)
        actions_frame.pack(padx=self.x_pad_1, pady=self.y_pad_1, side='right', expand=True, fill='both')

        # Stimulus Number
        self.stimulus_number_frame = ctk.CTkButton(stimulus_number_frame, text='Stimulus Number', font=("default_font", self.font_size), command=circuit_data.test_warmup_data)
        self.stimulus_number_frame.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='top', fill='both', expand=True)
        # Manual Entry Button
        self.stimulus_number_frame = ctk.CTkButton(stimulus_number_frame, text='Manual Entry', font=("default_font", self.font_size), command=circuit_data.test_warmup_data)
        self.stimulus_number_frame.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='top', fill='both', expand=True)
        # Stimulus Dropdown Box
        dropdown_values = [f'Stimulus Number: {x}' for x in range(1, 101)]
        self.option_var = tk.StringVar()
        self.dropdown = ctk.CTkOptionMenu(stimulus_number_frame, variable=self.option_var, values=dropdown_values, font=("default_font", self.font_size))
        self.dropdown.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='bottom', fill='both', expand=True)
        self.dropdown.bind('<Configure>', self.update_info)

        # Experiment Widgets
        self.exp_widgets_frame = ctk.CTkButton(exp_widgets_frame, text='Total Time', font=("default_font", self.font_size), command=circuit_data.test_warmup_data)
        self.exp_widgets_frame.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='top', fill='both', expand=True)
        self.exp_widgets_frame = ctk.CTkButton(exp_widgets_frame, text='Selection Made', font=("default_font", self.font_size), command=circuit_data.test_warmup_data)
        self.exp_widgets_frame.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='bottom', fill='both', expand=True)

        # Action Buttons
        self.actions_frame = ctk.CTkButton(actions_frame, text='Start', font=("default_font", self.font_size), command=circuit_data.test_num_audio_channels)
        self.actions_frame.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='top', fill='both', expand=True)
        self.actions_frame = ctk.CTkButton(actions_frame, text='Pause', font=("default_font", self.font_size), command=circuit_data.test_warmup_data)
        self.actions_frame.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='top', fill='both', expand=True)
        self.actions_frame = ctk.CTkButton(actions_frame, text='End', font=("default_font", self.font_size), command=circuit_data.test_warmup_data)
        self.actions_frame.pack(padx=self.x_pad_2, pady=self.y_pad_2, side='bottom', fill='both', expand=True)



    def update_info(self, event=None):
        selected_option = self.option_var.get()
        self.info_label.configure(text=f"Information about {selected_option}")







if __name__ == "__main__":
    Warmup_Class = Warmup()
    app = App(Warmup_Class)

    # For cross-platform compatibility, especially if using formats other than .ico
    img = Image.open('../docs/harl_logo.png')
    icon = ImageTk.PhotoImage(img)
    app.tk.call('wm', 'iconphoto', app._w, icon)






    app.mainloop()


    # run_app_1()