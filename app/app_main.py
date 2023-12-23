import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from threading import Thread
import time

from circuit_control import circuit_data



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

    def __init__(self):
        super().__init__()

        self.title("University of Memphis | Hearing Aid Research Laboratory | Sound Localization Experiment")
        self.geometry("1400x800")

        x_pad_main = 10
        y_pad_main = 10
        x_pad_1 = 10
        y_pad_1 = 10
        x_pad_2 = 10
        y_pad_2 = 10
        font_size = 20

        # Top Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(padx=x_pad_main, pady=y_pad_main, side='top', fill='both', expand=True)

        # Sub Frames for Top Frame
        hardware_status_frame = ctk.CTkFrame(top_frame)
        hardware_status_frame.pack(padx=x_pad_1, pady=y_pad_1, side='left', fill='both', expand=True)
        warmup_frame = ctk.CTkFrame(top_frame)
        warmup_frame.pack(padx=x_pad_1, pady=y_pad_1, side='right', fill='both', expand=True)


        # Hardware Connection Indicators
        self.tdt_status = ctk.CTkLabel(hardware_status_frame, text="TDT Hardware: Connected", text_color="green", font=("default_font", font_size)) # TODO: connection function
        self.tdt_status.pack(padx=x_pad_2, pady=y_pad_2, side='top', fill='both', expand=True)
        self.vr_status = ctk.CTkLabel(hardware_status_frame, text="VR Headset: Connected", text_color="green", font=("default_font", font_size)) # TODO: connection function
        self.vr_status.pack(padx=x_pad_2, pady=y_pad_2, side='bottom', fill='both', expand=True)

        # Warmup Widgets
        self.warmup_frame = ctk.CTkButton(warmup_frame, text="Play Warmup", font=("default_font", font_size), command=circuit_data.test_warmup_data)
        self.warmup_frame.pack(padx=x_pad_2, pady=y_pad_2, side='top', fill='both', expand=True)
        self.warmup_frame = ctk.CTkButton(warmup_frame, text="Visual of Each Test", font=("default_font", font_size), command=circuit_data.test_warmup_data)
        self.warmup_frame.pack(padx=x_pad_2, pady=y_pad_2, side='bottom', fill='both', expand=True)


        # Middle Frame
        middle_frame = ctk.CTkFrame(self)
        middle_frame.pack(padx=x_pad_main, pady=y_pad_main, side='top', fill='both', expand=True)

        # Sub Frames for Middle Frame
        stimulus_frame = ctk.CTkFrame(middle_frame)
        stimulus_frame.pack(padx=x_pad_1, pady=y_pad_1, side='left', expand=True, fill='both')
        exp_metadata_frame = ctk.CTkFrame(middle_frame)
        exp_metadata_frame.pack(padx=x_pad_1, pady=y_pad_1, side='right', expand=True, fill='both')

        # Description
        description_text = 'Select Experiment to Load'
        description_label = ctk.CTkLabel(stimulus_frame, text=description_text)
        description_label.pack(padx=x_pad_2, pady=y_pad_2, side='top', fill='both', expand=True)

        # Dropdown Box
        dropdown_values=[f'Experiment {x}' for x in range(1, 21)]
        self.option_var = tk.StringVar()
        self.dropdown = ctk.CTkOptionMenu(stimulus_frame, variable=self.option_var, values=dropdown_values, font=("default_font", font_size))
        self.dropdown.pack(padx=x_pad_2, pady=y_pad_2, side='top', fill='both', expand=True)
        self.dropdown.bind('<Configure>', self.update_info)

        # Load Experiment Button
        self.experiment_frame = ctk.CTkButton(stimulus_frame, text='Load Experiment', font=("default_font", font_size),command=circuit_data.test_warmup_data)
        self.experiment_frame.pack(padx=x_pad_2, pady=y_pad_2, side='bottom', fill='both', expand=True)

        # Experiment Metadata Info Box
        self.info_label = ctk.CTkLabel(exp_metadata_frame, text="Experiment Info:", font=("default_font", font_size))
        self.info_label.pack(expand=True)


        # Bottom Frame
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(padx=x_pad_main, pady=y_pad_main, side='bottom', fill='both', expand=True)

        # Sub Frames for Bottom Frame
        stimulus_number_frame = ctk.CTkFrame(bottom_frame)
        stimulus_number_frame.pack(padx=x_pad_1, pady=y_pad_1, side='left', expand=True, fill='both')
        exp_widgets_frame = ctk.CTkFrame(bottom_frame)
        exp_widgets_frame.pack(padx=x_pad_1, pady=y_pad_1, side='left', expand=True, fill='both')
        actions_frame = ctk.CTkFrame(bottom_frame)
        actions_frame.pack(padx=x_pad_1, pady=y_pad_1, side='right', expand=True, fill='both')

        # Stimulus Number
        self.stimulus_number_frame = ctk.CTkButton(stimulus_number_frame, text='Stimulus Number', font=("default_font", font_size), command=circuit_data.test_warmup_data)
        self.stimulus_number_frame.pack(padx=x_pad_2, pady=y_pad_2, side='top', fill='both', expand=True)
        # Manual Entry Button
        self.stimulus_number_frame = ctk.CTkButton(stimulus_number_frame, text='Manual Entry', font=("default_font", font_size), command=circuit_data.test_warmup_data)
        self.stimulus_number_frame.pack(padx=x_pad_2, pady=y_pad_2, side='top', fill='both', expand=True)
        # Stimulus Dropdown Box
        dropdown_values = [f'Stimulus Number: {x}' for x in range(1, 101)]
        self.option_var = tk.StringVar()
        self.dropdown = ctk.CTkOptionMenu(stimulus_number_frame, variable=self.option_var, values=dropdown_values, font=("default_font", font_size))
        self.dropdown.pack(padx=x_pad_2, pady=y_pad_2, side='bottom', fill='both', expand=True)
        self.dropdown.bind('<Configure>', self.update_info)

        # Experiment Widgets
        self.exp_widgets_frame = ctk.CTkButton(exp_widgets_frame, text='Time', font=("default_font", font_size), command=circuit_data.test_warmup_data)
        self.exp_widgets_frame.pack(padx=x_pad_2, pady=y_pad_2, side='top', fill='both', expand=True)
        self.exp_widgets_frame = ctk.CTkButton(exp_widgets_frame, text='Selection Made', font=("default_font", font_size), command=circuit_data.test_warmup_data)
        self.exp_widgets_frame.pack(padx=x_pad_2, pady=y_pad_2, side='bottom', fill='both', expand=True)

        # Action Buttons
        self.actions_frame = ctk.CTkButton(actions_frame, text='Start', font=("default_font", font_size), command=circuit_data.test_warmup_data)
        self.actions_frame.pack(padx=x_pad_2, pady=y_pad_2, side='top', fill='both', expand=True)
        self.actions_frame = ctk.CTkButton(actions_frame, text='Pause', font=("default_font", font_size), command=circuit_data.test_warmup_data)
        self.actions_frame.pack(padx=x_pad_2, pady=y_pad_2, side='top', fill='both', expand=True)
        self.actions_frame = ctk.CTkButton(actions_frame, text='End', font=("default_font", font_size), command=circuit_data.test_warmup_data)
        self.actions_frame.pack(padx=x_pad_2, pady=y_pad_2, side='bottom', fill='both', expand=True)



    def update_info(self, event=None):
        selected_option = self.option_var.get()
        self.info_label.configure(text=f"Information about {selected_option}")




if __name__ == "__main__":
    app = App()

    # For cross-platform compatibility, especially if using formats other than .ico
    img = Image.open('../docs/harl_logo.png')
    icon = ImageTk.PhotoImage(img)
    app.tk.call('wm', 'iconphoto', app._w, icon)

    app.mainloop()
