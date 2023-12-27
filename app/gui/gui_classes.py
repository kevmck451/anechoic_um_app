import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
from threading import Thread
import time
from tkinter import PhotoImage
import numpy as np
import warnings


import circuit_data
from circuit_manager import TDT_Circuit
from headset_manager import VR_Headset_Hardware
from utils_exp import CSVFile
from utils_exp import time_class



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Computer Icon
        img = Image.open('../docs/harl_logo.png')
        icon = ImageTk.PhotoImage(img)
        self.tk.call('wm', 'iconphoto', self._w, icon)

        # Main Setup ------------------------------------------------------------
        self.title('University of Memphis | Hearing Aid Research Laboratory | Sound Localization Experiment')

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1600
        window_height = 800
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.minsize(1000,600)

        # Padding and Font Styles
        self.x_pad_main = 2
        self.y_pad_main = 2
        self.x_pad_1 = 10
        self.y_pad_1 = 10
        self.x_pad_2 = 10
        self.y_pad_2 = 10
        self.font_size = 26
        self.fg_color = '#578CD5'
        self.hover_color = '#496FA3'

        # Widgets ---------------------------------------------------------------
        self.circuit = TDT_Circuit()
        self.headset = VR_Headset_Hardware()
        self.experiment_loaded = False
        self.experiment_started = False
        self.playing_icon = PhotoImage(file='../docs/playing icon s.png')
        self.start_icon = PhotoImage(file='../docs/start icon s.png')
        self.stop_icon = PhotoImage(file='../docs/stop icon s.png')
        self.pause_icon = PhotoImage(file='../docs/pause icon s.png')
        self.load_icon = PhotoImage(file='../docs/load icon s.png')
        warnings.filterwarnings('ignore', category=UserWarning, module='customtkinter.*')

        self.right_frame = Right_Frame(self)
        self.left_frame = Left_Frame(self, self.right_frame)

        # Grid configuration
        self.columnconfigure(0, weight=2)  # Left column with 2/3 of the space
        self.columnconfigure(1, weight=1)  # Right column with 1/3 of the space

        # Place the frames using grid
        self.left_frame.grid(row=0, column=0, sticky='nsew')  # Left frame in column 0
        self.right_frame.grid(row=0, column=1, sticky='nsew')  # Right frame in column 1


        # Run ---------------------------------------------------------------------
        self.mainloop()


class Right_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Main Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(padx=parent.x_pad_main, pady=parent.y_pad_main, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)  # Configure the column to expand

        self.console_box(main_frame)

    def console_box(self, frame):
        font_style = ("default_font", 12)
        x_pad = 5
        y_pad = 5

        # Experiment Metadata Info Box (Title)
        self.main_info_label = ctk.CTkLabel(frame, text="Sample Audio Order:", font=font_style)
        self.main_info_label.grid(row=0, column=0, padx=x_pad, pady=y_pad, sticky='ew')

        self.stim_labels = [ctk.CTkLabel(frame, text=f"Stim {i}:", font=("default_font", 12)) for i in range(1, 21)]
        for i, label in enumerate(self.stim_labels):
            label.grid(row=i + 1, column=0, padx=5, pady=5, sticky='w')

        # Configure the rows to not expand
        for i in range(21):
            frame.grid_rowconfigure(i, weight=0)

    def update_console_box(self, new_data, experiment, **kwargs):
        text_color = kwargs.get('text_color', 'black')
        number = kwargs.get('number', None)
        bg_color = kwargs.get('bg_color', None)

        self.main_info_label.configure(text=f"Sample Audio Order: Experiment {experiment}")
        for i, data in enumerate(new_data):
            if i+1 == number:
                self.stim_labels[i].configure(text=f"Stim {number}: {str(data).title()}", text_color=text_color, bg_color='#B8B9B8')
            elif bg_color is not None:
                self.stim_labels[i].configure(text=f"Stim {i + 1}: {str(data).title()}", text_color='black', bg_color=bg_color)
            else: self.stim_labels[i].configure(text=f"Stim {i+1}: {str(data).title()}", text_color='black')

    def reset_console_box(self):
        self.main_info_label.configure(text="Sample Audio Order:")
        for i, label in enumerate(self.stim_labels):
            label.configure(text=f"Stim {i+1}:", text_color='black', bg_color='#CFCFCF')


class Left_Frame(ctk.CTkFrame):
    def __init__(self, parent, console_frame):
        super().__init__(parent)
        self.console_frame = console_frame
        self.parent = parent
        # Top Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, padx=parent.x_pad_main, pady=parent.y_pad_main, sticky='nsew')

        # Hardware Status & Load Experiment Widgets
        top_left_frame = ctk.CTkFrame(top_frame)
        top_left_frame.grid(row=0, column=0, padx=parent.x_pad_1, pady=parent.y_pad_1, sticky='nsew')
        top_right_frame = ctk.CTkFrame(top_frame)
        top_right_frame.grid(row=0, column=1, padx=parent.x_pad_1, pady=parent.y_pad_1, sticky='nsew')

        # Configure the grid columns of the top_frame
        top_frame.grid_columnconfigure(0, weight=1, uniform='col')  # First column
        top_frame.grid_columnconfigure(1, weight=1, uniform='col')  # Second column
        top_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Middle Frame
        middle_frame = ctk.CTkFrame(self)
        middle_frame.grid(row=1, column=0, padx=parent.x_pad_main, pady=parent.y_pad_main, sticky='nsew')

        # Creating and placing sub-frames for each column in the middle_frame
        middle_frame_1 = ctk.CTkFrame(middle_frame)
        middle_frame_1.grid(row=0, column=0, padx=parent.x_pad_1, pady=parent.y_pad_1, sticky='nsew')

        middle_frame_2 = ctk.CTkFrame(middle_frame)
        middle_frame_2.grid(row=0, column=1, padx=parent.x_pad_1, pady=parent.y_pad_1, sticky='nsew')

        middle_frame_3 = ctk.CTkFrame(middle_frame)
        middle_frame_3.grid(row=0, column=2, padx=parent.x_pad_1, pady=parent.y_pad_1, sticky='nsew')


        # Configure the grid columns of the middle_frame
        middle_frame.grid_columnconfigure(0, weight=1, uniform='col')  # First column
        middle_frame.grid_columnconfigure(1, weight=1, uniform='col')  # Second column
        middle_frame.grid_columnconfigure(2, weight=1, uniform='col')  # Third column

        # Configure the row of the middle_frame to expand
        middle_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Bottom Frame
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=2, column=0, padx=parent.x_pad_main, pady=parent.y_pad_main, sticky='nsew')

        # Configure the grid rows and column for self
        self.grid_rowconfigure(0, weight=1)  # Top row
        self.grid_rowconfigure(1, weight=1)  # Middle row
        self.grid_rowconfigure(2, weight=1)  # Bottom row
        self.grid_columnconfigure(0, weight=1, uniform='col')  # Single column

        # Bottom Frame Left and Right Cells
        bottom_left_frame = ctk.CTkFrame(bottom_frame)
        bottom_left_frame.grid(row=0, column=0, padx=parent.x_pad_1, pady=parent.y_pad_1, sticky='nsew')

        bottom_right_frame = ctk.CTkFrame(bottom_frame)
        bottom_right_frame.grid(row=0, column=1, padx=parent.x_pad_1, pady=parent.y_pad_1, sticky='nsew')

        # Configure the grid columns of the bottom_frame
        bottom_frame.grid_columnconfigure(0, weight=1, uniform='col')  # Left column
        bottom_frame.grid_columnconfigure(1, weight=1, uniform='col')  # Right column

        # Optionally, configure the row of the bottom_frame to expand
        bottom_frame.grid_rowconfigure(0, weight=1, uniform='row')


        self.hardware_connection_frames(parent, top_left_frame)
        self.select_experiment(parent, top_right_frame)
        self.warmup_frames(parent, middle_frame_1)
        self.start_stop_frames(parent, middle_frame_2)
        self.pause_frames(parent, middle_frame_3)
        self.experiment_metadata_frames_1(parent, bottom_left_frame)
        self.experiment_metadata_frames_2(parent, bottom_right_frame)
        self.check_hardware_status()


    # FRAMES ---------------------------------------------
    def hardware_connection_frames(self, parent, frame):
        # Configure the grid for the frame
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        # TDT Connection Status
        if self.parent.circuit.circuit_state:
            connection_status_TDT = 'TDT Hardware: Connected'
            text_color_TDT = '#2B881A'
        else:
            connection_status_TDT = 'TDT Hardware: Not Connected'
            text_color_TDT = '#BD2E2E'

        self.tdt_status = ctk.CTkLabel(frame, text=connection_status_TDT, text_color=text_color_TDT, font=("default_font", parent.font_size))
        self.tdt_status.grid(row=0, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

        # TDT Reset Button
        self.reset_button_TDT = ctk.CTkButton(frame, text='TDT Reset', font=("default_font", parent.font_size), fg_color=parent.fg_color, command=self.reset_tdt_hardware)
        self.reset_button_TDT.grid(row=0, column=1, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

        # VR Connection Status
        if self.parent.headset.headset_state:
            connection_status_VR = 'VR Headset: Connected'
            text_color_VR = '#2B881A'
        else:
            connection_status_VR = 'VR Headset: Not Connected'
            text_color_VR = '#BD2E2E'

        self.vr_status = ctk.CTkLabel(frame, text=connection_status_VR, text_color=text_color_VR, font=("default_font", parent.font_size))
        self.vr_status.grid(row=1, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

        # VR Reset Button
        self.reset_button_VR = ctk.CTkButton(frame, text='VR Reset', font=("default_font", parent.font_size), fg_color=parent.fg_color, command=self.reset_headset_hardware)
        self.reset_button_VR.grid(row=1, column=1, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

    def select_experiment(self, parent, frame):
        # Configure the grid for the frame
        frame.grid_rowconfigure(0, weight=1)  # Row for the dropdown box
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        # Dropdown Box
        dropdown_values_exp = ['Select an Experiment'] + [f'Experiment {x}' for x in range(1, 21)]
        self.option_var_exp = tk.StringVar(value=dropdown_values_exp[0])  # Set initial value to the prompt text
        self.dropdown_exp = ctk.CTkOptionMenu(frame, variable=self.option_var_exp, values=dropdown_values_exp,
                                              font=("default_font", parent.font_size), fg_color="#0952AA", dropdown_hover_color='#0F5BB6')
        self.dropdown_exp.grid(row=0, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')


        # Load Experiment Button
        self.experiment_button = ctk.CTkButton(frame, text='Load Experiment', font=("default_font", parent.font_size),
                                               fg_color=parent.fg_color, command=self.on_experiment_load, image=self.parent.load_icon)
        self.experiment_button.grid(row=1, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

    def warmup_frames(self, parent, frame):
        frame.grid_rowconfigure(0, weight=1)  # Row for the dropdown box
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_rowconfigure(3, weight=1)  # Row for the load button
        frame.grid_rowconfigure(4, weight=1)  # Row for the load button
        frame.grid_rowconfigure(5, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        # Sub Sub Frame of Warm Up ----------------------------------------
        self.warmup_button = ctk.CTkButton(frame, text="Play Warmup",
                                           font=("default_font", parent.font_size), fg_color=parent.fg_color,
                                           hover_color=parent.hover_color, command=self.on_warmup_button_press,
                                           image=self.parent.start_icon)
        self.warmup_button.grid(row=0, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

        self.warmup_test_1 = ctk.CTkLabel(frame, text='Test 1', text_color='gray', font=("default_font", parent.font_size))
        self.warmup_test_1.grid(row=1, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')
        self.warmup_test_2 = ctk.CTkLabel(frame, text='Test 2', text_color='gray', font=("default_font", parent.font_size))
        self.warmup_test_2.grid(row=2, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')
        self.warmup_test_3 = ctk.CTkLabel(frame, text='Test 3', text_color='gray', font=("default_font", parent.font_size))
        self.warmup_test_3.grid(row=3, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')
        self.warmup_test_4 = ctk.CTkLabel(frame, text='Test 4', text_color='gray', font=("default_font", parent.font_size))
        self.warmup_test_4.grid(row=4, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')
        self.warmup_test_5 = ctk.CTkLabel(frame, text='Test 5', text_color='gray', font=("default_font", parent.font_size))
        self.warmup_test_5.grid(row=5, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

    def start_stop_frames(self, parent, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.start_button = ctk.CTkButton(frame, text='Start Experiment', font=("default_font", parent.font_size),
                                          fg_color="#2B881A", hover_color='#389327', command=self.on_start_button_press,
                                          image=self.parent.start_icon)
        self.start_button.grid(row=0, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')
        self.end_button = ctk.CTkButton(frame, text='End Experiment', font=("default_font", parent.font_size),
                                        fg_color="#BD2E2E", hover_color='#C74343', command=self.on_end_button_press,
                                        image=self.parent.stop_icon)
        self.end_button.grid(row=1, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

    def pause_frames(self, parent, frame):
        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_rowconfigure(3, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.pause_button = ctk.CTkButton(frame, text='Pause', font=("default_font", parent.font_size),
                                          fg_color="#8F8F8F", hover_color='#9E9E9E', image=self.parent.pause_icon)
        self.pause_button.grid(row=0, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

        # Stimulus Dropdown Box
        dropdown_values_stim = [f'Stimulus Start Number: {x}' for x in range(1, 101)]
        self.option_var_stim = tk.StringVar(value=dropdown_values_stim[0])  # Set initial value to the prompt text
        self.dropdown_stim = ctk.CTkOptionMenu(frame, variable=self.option_var_stim, values=dropdown_values_stim,
                                               font=("default_font", parent.font_size), fg_color="#0952AA", dropdown_hover_color='#0F5BB6')
        self.dropdown_stim.grid(row=1, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

        self.load_stim_button = ctk.CTkButton(frame, text='Load', font=("default_font", parent.font_size), fg_color=parent.fg_color, image=self.parent.load_icon)
        self.load_stim_button.grid(row=2, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

        # Stimulus Dropdown Box
        dropdown_values_time_bw_samp = [f'Time bw Samples: {x} sec' for x in np.arange(0.5, 4.5, 0.5)]
        self.option_var_time_bw_samp = tk.StringVar(value=dropdown_values_time_bw_samp[3])  # Set initial value to the prompt text
        self.dropdown_time_bw_samp = ctk.CTkOptionMenu(frame, variable=self.option_var_time_bw_samp, values=dropdown_values_time_bw_samp,
                                               font=("default_font", parent.font_size), fg_color="#0952AA",
                                               dropdown_hover_color='#0F5BB6')
        self.dropdown_time_bw_samp.grid(row=3, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

    def experiment_metadata_frames_1(self, parent, frame):

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        self.current_stimulus_label = ctk.CTkLabel(frame, text='Current Simulus #:',font=("default_font", parent.font_size))
        self.current_stimulus_label.grid(row=0, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')
        self.current_stimulus_display = ctk.CTkLabel(frame, text='None',font=("default_font", parent.font_size))
        self.current_stimulus_display.grid(row=0, column=1, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

        self.total_time_label = ctk.CTkLabel(frame, text='Total Time:', font=("default_font", parent.font_size))
        self.total_time_label.grid(row=1, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')
        self.total_time_display = ctk.CTkLabel(frame, text='00:00',font=("default_font", parent.font_size))
        self.total_time_display.grid(row=1, column=1, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

    def experiment_metadata_frames_2(self, parent, frame):

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        self.speaker_projected_label = ctk.CTkLabel(frame, text='Speaker Projecting:', font=("default_font", parent.font_size))
        self.speaker_projected_label.grid(row=0, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')
        self.speaker_projected_display = ctk.CTkLabel(frame, text='None', font=("default_font", parent.font_size))
        self.speaker_projected_display.grid(row=0, column=1, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

        self.selection_made_label = ctk.CTkLabel(frame, text='Speaker Selected:', font=("default_font", parent.font_size))
        self.selection_made_label.grid(row=1, column=0, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')
        self.selection_made_display = ctk.CTkLabel(frame, text='None',font=("default_font", parent.font_size))
        self.selection_made_display.grid(row=1, column=1, padx=parent.x_pad_2, pady=parent.y_pad_2, sticky='nsew')

    # ACTION FUNCTIONS ---------------------------------------------
    def reset_tdt_hardware(self):
        self.parent.circuit = TDT_Circuit()

        if self.parent.circuit.circuit_state:
            connection_status_TDT = 'TDT Hardware: Connected'
            text_color_TDT = '#2B881A'
            self.tdt_status.configure(text=connection_status_TDT, text_color=text_color_TDT)
        else:
            connection_status_TDT = 'TDT Hardware: Not Connected'
            text_color_TDT = '#BD2E2E'
            self.tdt_status.configure(text=connection_status_TDT, text_color=text_color_TDT)

    def reset_headset_hardware(self):
        self.parent.headset = VR_Headset_Hardware()

        if self.parent.headset.headset_state:
            connection_status_VR = 'VR Headset: Connected'
            text_color_VR = '#2B881A'
            self.vr_status.configure(text=connection_status_VR, text_color=text_color_VR)
        else:
            connection_status_VR = 'VR Headset: Not Connected'
            text_color_VR = '#BD2E2E'
            self.vr_status.configure(text=connection_status_VR, text_color=text_color_VR)

    def check_hardware_status(self):
        if self.parent.headset.first_connect:
            Thread(target=self.parent.headset.check_connection).start()

        if self.parent.circuit.circuit_state:
            connection_status_TDT = 'TDT Hardware: Connected'
            text_color_TDT = '#2B881A'
            self.tdt_status.configure(text=connection_status_TDT, text_color=text_color_TDT)
        else:
            connection_status_TDT = 'TDT Hardware: Not Connected'
            text_color_TDT = '#BD2E2E'
            self.tdt_status.configure(text=connection_status_TDT, text_color=text_color_TDT)

        if self.parent.headset.headset_state:
            connection_status_VR = 'VR Headset: Connected'
            text_color_VR = '#2B881A'
            self.vr_status.configure(text=connection_status_VR, text_color=text_color_VR)
        else:
            connection_status_VR = 'VR Headset: Not Connected'
            text_color_VR = '#BD2E2E'
            self.vr_status.configure(text=connection_status_VR, text_color=text_color_VR)

        self.parent.after(3000, self.check_hardware_status)

    def on_experiment_load(self):
        selected_value = self.option_var_exp.get()

        if selected_value != 'Select an Experiment':
            selected_value = selected_value.split(' ')[1]
            self.sample_names_list = circuit_data.load_audio_names(selected_value)
            self.console_frame.update_console_box(self.sample_names_list, experiment=selected_value)

            # Show loading popup and start loading in a separate thread
            self.manage_loading_audio_popup(show=True)
            load_thread = threading.Thread(target=self.load_audio_samples, args=(selected_value,))
            load_thread.start()
            self.parent.experiment_loaded = True
            self.loaded_experiment_name = self.option_var_exp.get()

    def manage_loading_audio_popup(self, show=False):
        if show:
            self.loading_popup = tk.Toplevel(self)
            self.loading_popup.title("Loading")
            window_width = 400
            window_height = 100
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            center_x = int((screen_width / 2) - (window_width / 2))
            center_y = int((screen_height / 2) - (window_height / 2))
            self.loading_popup.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
            tk.Label(self.loading_popup, text="Loading audio samples, please wait...", font=("default_font", 20)).pack(pady=10)
            # Configure style for a larger progress bar
            style = ttk.Style(self.loading_popup)
            style.theme_use('clam')  # or 'default', 'classic', 'alt', etc.
            style.configure("Larger.Horizontal.TProgressbar",
                            troughcolor='#D3D3D3',
                            bordercolor='#D3D3D3',
                            background='#00008B',  # Dark Blue color
                            lightcolor='#00008B',  # Adjust if needed
                            darkcolor='#00008B',  # Adjust if needed
                            thickness=30)  # Customize thickness

            self.progress = ttk.Progressbar(self.loading_popup, orient="horizontal", length=250, mode="indeterminate",
                                            style="Larger.Horizontal.TProgressbar")
            self.progress.pack(pady=10)
            self.progress.start()
        else:
            if self.loading_popup:
                self.progress.stop()
                self.loading_popup.destroy()

    def load_audio_samples(self, experiment_id):
        self.audio_samples_list = circuit_data.load_audio_samples(experiment_id)
        self.channel_list = circuit_data.load_channel_numbers(experiment_id)

        # Call the function to close the loading pop-up in the main thread
        self.after(0, self.manage_loading_audio_popup)

    def on_warmup_button_press(self):

        if self.parent.experiment_started:
            return
        if self.parent.circuit.circuit_state == False:
            self.warning_popup_general(message='TDT Hardware Not Connected')
            return
        # if self.parent.headset.headset_state == False:
        #     self.warning_popup_general(message='VR Headset Not Connected')
        #     return

        task_thread = threading.Thread(target=self.trigger_warmup_audio_samples)
        task_thread.start()

    def trigger_warmup_audio_samples(self):

        for i in range(5):
            # Dynamically access the test display widget
            test_widget_name = f'warmup_test_{i + 1}'  # Construct the name string
            test_widget = getattr(self, test_widget_name)
            test_widget.configure(text_color='gray', bg_color='#DBDBDB')

        test_audio_buffer, test_channel_buffer = circuit_data.load_warmup_data()

        for i, (sample, channel) in enumerate(zip(test_audio_buffer, test_channel_buffer)):
            self.warmup_button.configure(fg_color="#2B881A", hover_color="#2B881A", image=self.parent.playing_icon)  # Example gray color
            # Dynamically access the test display widget
            test_widget_name = f'warmup_test_{i + 1}'  # Construct the name string
            test_widget = getattr(self, test_widget_name)
            test_widget.configure(bg_color='#B8B9B8')

            # Logic to Trigger Audio Sample out of TDT # todo logic to Trigger Audio Sample out of TDT
            self.parent.circuit.trigger_audio_sample(sample, channel)

            # Wait for VR Response
            vr_thread = Thread(target=self.parent.headset.get_vr_input)
            vr_thread.start()
            vr_input = self.parent.headset.speaker_selected

            if vr_input:  # todo change logic when a number equals channel
                test_widget.configure(text_color='#2B881A')  # update test display color to green
            elif not vr_input:
                test_widget.configure(text_color='#BD2E2E')
            else: test_widget.configure(text_color='gray')

            # Time between Samples
            time_to_sleep = self.option_var_time_bw_samp.get().split(':')[1].strip().split(' ')[0]
            time.sleep(float(time_to_sleep))


        self.after(0, lambda: self.warmup_button.configure(fg_color='#578CD5', hover_color=self.parent.hover_color, image=self.parent.start_icon))  # Replace with original color

    def warning_popup_general(self, message):
        message_popup = tk.Toplevel(self)
        message_popup.title("Message")
        window_width = 400
        window_height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))
        message_popup.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Display the message
        tk.Label(message_popup, text=message, font=("default_font", 20)).pack(pady=20)

        # OK button to close the pop-up
        ok_button = tk.Button(message_popup, text="OK", background="#D3D3D3", padx=10, pady=10,
                              command=message_popup.destroy)
        ok_button.pack(pady=10)

    # EXPERIMENT FUNCTIONS ---------------------------------------------
    def on_start_button_press(self):

        # Error Handling
        if self.option_var_exp.get() == 'Select an Experiment':
            self.warning_popup_general(message='Need to select an Experiment')
            return
        if self.parent.experiment_loaded == False:
            self.warning_popup_general(message='No Experiment Loaded')
            return
        if self.option_var_exp.get() != self.loaded_experiment_name:
            self.warning_popup_general(message='Loaded Experiment doesnt\nmatch Selected Experiment')
            return
        if self.parent.experiment_started:
            return
        if self.parent.circuit.circuit_state == False:
            self.warning_popup_general(message='TDT Hardware Not Connected')
            return
        # if self.parent.headset.headset_state == False:
        #     self.warning_popup_general(message='VR Headset Not Connected')
        #     return

        timer_thread = threading.Thread(target=self.experiment_timer)
        timer_thread.start()
        task_thread = threading.Thread(target=self.start_experiment_procedure)
        task_thread.start()

    def experiment_timer(self):
        self.experiment_total_time_object = time_class('Experiment Total Time')

    def update_experiment_stim_number_display(self, value):
        self.current_stimulus_display.configure(text=value)

    def update_experiment_speaker_proj_display(self, value):
        self.speaker_projected_display.configure(text=value)

    def update_experiment_speaker_selected_display(self, value):
        self.selection_made_display.configure(text=value)

    def update_experiment_total_time_display(self):
        if self.parent.experiment_started:
            time = self.experiment_total_time_object.stats()
            self.total_time_display.configure(text=time)
            self.parent.after(500, self.update_experiment_total_time_display)

    def start_experiment_procedure(self):
        # print('Starting Experiment')
        self.parent.experiment_started = True
        self.start_button.configure(image=self.parent.playing_icon)
        self.update_experiment_total_time_display()
        selected_value = self.option_var_exp.get().split(' ')[1]
        self.output_file = CSVFile(selected_value)

        self.parent.experiment_started = True
        self.start_button.configure(text='Experiment In Progress', fg_color="#2B881A", hover_color="#2B881A")

        self.sample_names_list = circuit_data.load_audio_names(selected_value)

        for iteration, (audio_sample, channel) in enumerate(zip(self.audio_samples_list, self.channel_list)):
            if self.parent.experiment_started == False:
                break
            self.update_experiment_stim_number_display(iteration+1)
            self.update_experiment_speaker_proj_display(channel)
            if iteration%5 == 0:
                # print(f'{int((iteration/5)+1)}: {audio_sample.name.split("_")[0].title()}')
                self.console_frame.update_console_box(self.sample_names_list, experiment=selected_value, text_color='#2B881A', number=int((iteration/5)+1))

            reaction_time = time_class('Reaction Time')

            # Trigger Audio Playing:
            # time.sleep(audio_sample.sample_length)
            self.parent.circuit.trigger_audio_sample(audio_sample, channel)

            # Get VR Response todo: get vr response
            speaker_selected = 0
            # self.update_experiment_speaker_selected_display(speaker_selected)
            reaction_time = reaction_time.reaction_time()
            num_selections = 0

            self.output_file.write_row_at(iteration, [iteration+1, audio_sample.name, channel, speaker_selected, reaction_time, num_selections])

            # Time between Samples
            time_to_sleep = self.option_var_time_bw_samp.get().split(':')[1].strip().split(' ')[0]
            time.sleep(float(time_to_sleep))

        self.console_frame.update_console_box(self.sample_names_list, experiment=selected_value)
        self.end_experiment_procedure()

    def on_end_button_press(self):
        print('Experiment Ended')

        self.total_time_display.configure(text='00:00')
        self.update_experiment_stim_number_display('None')
        self.update_experiment_speaker_proj_display('None')
        self.option_var_exp.set('Select an Experiment')
        self.parent.experiment_loaded = False
        self.console_frame.reset_console_box()
        self.end_experiment_procedure()

    def end_experiment_procedure(self):
        self.start_button.configure(text='Start Experiment', fg_color="#2B881A", hover_color='#389327', image=self.parent.start_icon)
        self.parent.experiment_started = False




if __name__ == "__main__":
    App()