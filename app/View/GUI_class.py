from tkinter import PhotoImage
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
import numpy as np
import warnings
from tkinter import ttk

import configuration
from controller import Event


class GUI_class(ctk.CTk):
    def __init__(self, event_handler):
        super().__init__()

        # Computer Icon
        img = Image.open('../docs/harl_logo.png')
        icon = ImageTk.PhotoImage(img)
        self.tk.call('wm', 'iconphoto', self._w, icon)

        # Main Setup ------------------------------------------------------------
        self.title(configuration.window_title)

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (configuration.window_width / 2))
        center_y = int((screen_height / 2) - (configuration.window_height / 2))
        self.geometry(f'{configuration.window_width}x{configuration.window_height}+{center_x}+{center_y}')
        self.minsize(configuration.min_window_width, configuration.min_window_height)

        self.Console_Frame = Console_Frame(self)
        self.Main_Frame = Main_Frame(self, self.Console_Frame, event_handler)

        # Grid configuration
        self.columnconfigure(0, weight=2)  # Left column with 2/3 of the space
        self.columnconfigure(1, weight=1)  # Right column with 1/3 of the space

        # Place the frames using grid
        self.Main_Frame.grid(row=0, column=0, sticky='nsew')  # Left frame in column 0
        self.Console_Frame.grid(row=0, column=1, sticky='nsew')  # Right frame in column 1

class Console_Frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Main Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)  # Configure the column to expand

        self.console_box(main_frame)

    def console_box(self, frame):

        # Experiment Metadata Info Box (Title)
        self.main_info_label = ctk.CTkLabel(frame, text="Sample Audio Order:", font=configuration.console_font_style)
        self.main_info_label.grid(row=0, column=0, padx=configuration.console_x_pad, pady=configuration.console_y_pad, sticky='ew')

        self.stim_labels = [ctk.CTkLabel(frame, text=f"Stim {i}:", font=configuration.console_font_style) for i in range(1, 21)]
        for i, label in enumerate(self.stim_labels):
            label.grid(row=i + 1, column=0, padx=configuration.console_x_pad, pady=configuration.console_y_pad, sticky='w')

        # Configure the rows to not expand
        for i in range(21):
            frame.grid_rowconfigure(i, weight=0)

    def update_console_box(self, new_data, experiment, **kwargs):
        text_color = kwargs.get('text_color', 'black')
        number = kwargs.get('number', None)
        bg_color = kwargs.get('bg_color', None)

        self.main_info_label.configure(text=f"Sample Audio Order: Experiment {experiment}")
        for i, data in enumerate(new_data):
            if i + 1 == number:
                self.stim_labels[i].configure(text=f"Stim {number}: {str(data).title()}", text_color=text_color,
                                               bg_color='#B8B9B8')
            elif bg_color is not None:
                self.stim_labels[i].configure(text=f"Stim {i + 1}: {str(data).title()}", text_color='black',
                                               bg_color=bg_color)
            else:
                self.stim_labels[i].configure(text=f"Stim {i + 1}: {str(data).title()}", text_color='black')

    def reset_console_box(frame):
        frame.main_info_label.configure(text="Sample Audio Order:")
        for i, label in enumerate(frame.stim_labels):
            label.configure(text=f"Stim {i + 1}:", text_color='black', bg_color='#CFCFCF')

class Main_Frame(ctk.CTkFrame):
    def __init__(self, parent, console_frame, event_handler):
        super().__init__(parent)
        self.console_frame = console_frame
        self.event_handler = event_handler

        self.playing_icon = PhotoImage(file=configuration.playing_icon_filepath)
        self.start_icon = PhotoImage(file=configuration.start_icon_filepath)
        self.stop_icon = PhotoImage(file=configuration.stop_icon_filepath)
        self.pause_icon = PhotoImage(file=configuration.pause_icon_filepath)
        self.load_icon = PhotoImage(file=configuration.load_icon_filepath)
        warnings.filterwarnings('ignore', category=UserWarning, module='customtkinter.*')

        # Top Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')

        # Hardware Status & Load Experiment Widgets
        top_left_frame = ctk.CTkFrame(top_frame)
        top_left_frame.grid(row=0, column=0, padx=configuration.x_pad_1, pady=configuration.y_pad_1, sticky='nsew')
        top_right_frame = ctk.CTkFrame(top_frame)
        top_right_frame.grid(row=0, column=1, padx=configuration.x_pad_1, pady=configuration.y_pad_1, sticky='nsew')

        # Configure the grid of the top_frame
        top_frame.grid_columnconfigure(0, weight=1, uniform='col')  # First column
        top_frame.grid_columnconfigure(1, weight=1, uniform='col')  # Second column
        top_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Middle Frame
        middle_frame = ctk.CTkFrame(self)
        middle_frame.grid(row=1, column=0, padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')

        # Creating and placing sub-frames for each column in the middle_frame
        middle_frame_1 = ctk.CTkFrame(middle_frame)
        middle_frame_1.grid(row=0, column=0, padx=configuration.x_pad_1, pady=configuration.y_pad_1, sticky='nsew')
        middle_frame_2 = ctk.CTkFrame(middle_frame)
        middle_frame_2.grid(row=0, column=1, padx=configuration.x_pad_1, pady=configuration.y_pad_1, sticky='nsew')
        middle_frame_3 = ctk.CTkFrame(middle_frame)
        middle_frame_3.grid(row=0, column=2, padx=configuration.x_pad_1, pady=configuration.y_pad_1, sticky='nsew')

        # Configure the grid of the middle_frame
        middle_frame.grid_columnconfigure(0, weight=1, uniform='col')  # First column
        middle_frame.grid_columnconfigure(1, weight=1, uniform='col')  # Second column
        middle_frame.grid_columnconfigure(2, weight=1, uniform='col')  # Third column
        middle_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Bottom Frame
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=2, column=0, padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')

        # Bottom Frame Left and Right Cells
        bottom_left_frame = ctk.CTkFrame(bottom_frame)
        bottom_left_frame.grid(row=0, column=0, padx=configuration.x_pad_1, pady=configuration.y_pad_1, sticky='nsew')
        bottom_right_frame = ctk.CTkFrame(bottom_frame)
        bottom_right_frame.grid(row=0, column=1, padx=configuration.x_pad_1, pady=configuration.y_pad_1, sticky='nsew')

        # Configure the grid of the bottom_frame
        bottom_frame.grid_columnconfigure(0, weight=1, uniform='col')  # Left column
        bottom_frame.grid_columnconfigure(1, weight=1, uniform='col')  # Right column
        bottom_frame.grid_rowconfigure(0, weight=1, uniform='row')

        # Configure the grid rows and column for self
        self.grid_rowconfigure(0, weight=1)  # Top row
        self.grid_rowconfigure(1, weight=1)  # Middle row
        self.grid_rowconfigure(2, weight=1)  # Bottom row
        self.grid_columnconfigure(0, weight=1, uniform='col')  # Single column

        self.hardware_connection_frames(top_left_frame)
        self.select_experiment_frame(top_right_frame)
        self.warmup_frames(middle_frame_1)
        self.start_stop_frames(middle_frame_2)
        self.pause_frames(middle_frame_3)
        self.experiment_metadata_frames_1(bottom_left_frame)
        self.experiment_metadata_frames_2(bottom_right_frame)

    # FRAMES ---------------------------------------------
    def hardware_connection_frames(self, frame):
        # Configure the grid for the frame
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        # TDT Connection Status
        self.tdt_status = ctk.CTkLabel(frame, text=configuration.connection_status_TDT, text_color=configuration.not_connected_color,
                                       font=(configuration.main_font_style, configuration.main_font_size))
        self.tdt_status.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        # TDT Reset Button
        self.reset_button_TDT = ctk.CTkButton(frame, text='TDT Connect',
                                              font=(configuration.main_font_style, configuration.main_font_size),
                                              fg_color=configuration.button_fg_color, command=lambda: self.event_handler(Event.TDT_CONNECT))
        self.reset_button_TDT.grid(row=0, column=1, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        # VR Connection Status
        self.vr_status = ctk.CTkLabel(frame, text=configuration.connection_status_VR, text_color=configuration.not_connected_color,
                                      font=(configuration.main_font_style, configuration.main_font_size))
        self.vr_status.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        # VR Reset Button
        self.reset_button_VR = ctk.CTkButton(frame, text='VR Connect',
                                             font=(configuration.main_font_style, configuration.main_font_size),
                                             fg_color=configuration.button_fg_color, command=lambda: self.event_handler(Event.VR_CONNECT))
        self.reset_button_VR.grid(row=1, column=1, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    def select_experiment_frame(self, frame):
        # Configure the grid for the frame
        frame.grid_rowconfigure(0, weight=1)  # Row for the dropdown box
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        # Dropdown Box
        dropdown_values_exp = ['Select an Experiment'] + [f'Experiment {x}' for x in range(1, 21)]
        self.option_var_exp = tk.StringVar(value=dropdown_values_exp[0])  # Set initial value to the prompt text
        self.dropdown_exp = ctk.CTkOptionMenu(frame, variable=self.option_var_exp, values=dropdown_values_exp,
                                              font=(configuration.main_font_style, configuration.main_font_size),
                                              fg_color=configuration.dropdown_fg_color, dropdown_hover_color=configuration.button_hover_color)
        self.dropdown_exp.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')


        # Load Experiment Button
        self.experiment_button = ctk.CTkButton(frame, text='Load Experiment',
                                               font=(configuration.main_font_style, configuration.main_font_size),
                                               fg_color=configuration.button_fg_color,
                                               image=self.load_icon, command=lambda: self.event_handler(Event.LOAD_EXPERIMENT))
        self.experiment_button.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    def warmup_frames(self, frame):
        frame.grid_rowconfigure(0, weight=1)  # Row for the dropdown box
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_rowconfigure(3, weight=1)  # Row for the load button
        frame.grid_rowconfigure(4, weight=1)  # Row for the load button
        frame.grid_rowconfigure(5, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        # Sub Sub Frame of Warm Up ----------------------------------------
        self.warmup_button = ctk.CTkButton(frame, text="Play Warmup",
                                           font=(configuration.main_font_style, configuration.main_font_size),
                                           fg_color=configuration.button_fg_color, hover_color=configuration.button_hover_color,
                                           image=self.start_icon, command=lambda: self.event_handler(Event.START_WARMUP))
        self.warmup_button.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.warmup_test_1 = ctk.CTkLabel(frame, text='Test 1', text_color=configuration.warmup_test_color,
                                          font=(configuration.main_font_style, configuration.main_font_size))
        self.warmup_test_1.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')
        self.warmup_test_2 = ctk.CTkLabel(frame, text='Test 2', text_color=configuration.warmup_test_color,
                                          font=(configuration.main_font_style, configuration.main_font_size))
        self.warmup_test_2.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')
        self.warmup_test_3 = ctk.CTkLabel(frame, text='Test 3', text_color=configuration.warmup_test_color,
                                          font=(configuration.main_font_style, configuration.main_font_size))
        self.warmup_test_3.grid(row=3, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')
        self.warmup_test_4 = ctk.CTkLabel(frame, text='Test 4', text_color=configuration.warmup_test_color,
                                          font=(configuration.main_font_style, configuration.main_font_size))
        self.warmup_test_4.grid(row=4, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')
        self.warmup_test_5 = ctk.CTkLabel(frame, text='Test 5', text_color=configuration.warmup_test_color,
                                          font=(configuration.main_font_style, configuration.main_font_size))
        self.warmup_test_5.grid(row=5, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    def start_stop_frames(self, frame):

        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.start_button = ctk.CTkButton(frame, text='Start Experiment', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.start_fg_color, hover_color=configuration.start_hover_color,
                                          image=self.start_icon, command=lambda: self.event_handler(Event.START_EXPERIMENT))
        self.start_button.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')
        self.end_button = ctk.CTkButton(frame, text='End Experiment', font=(configuration.main_font_style, configuration.main_font_size),
                                        fg_color=configuration.stop_fg_color, hover_color=configuration.stop_hover_color,
                                        image=self.stop_icon, command=lambda: self.event_handler(Event.END_EXPERIMENT))
        self.end_button.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    def pause_frames(self, frame):
        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_rowconfigure(3, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        self.pause_button = ctk.CTkButton(frame, text='Pause', font=(configuration.main_font_style, configuration.main_font_size),
                                          fg_color=configuration.pause_fg_color, hover_color=configuration.pause_hover_color,
                                          image=self.pause_icon, command=lambda: self.event_handler(Event.PAUSE))
        self.pause_button.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        # Stimulus Dropdown Box
        dropdown_values_stim = [f'Stimulus Start Number: {x}' for x in range(1, 101)]
        self.option_var_stim = tk.StringVar(value=dropdown_values_stim[0])  # Set initial value to the prompt text
        self.dropdown_stim = ctk.CTkOptionMenu(frame, variable=self.option_var_stim, values=dropdown_values_stim,
                                               font=(configuration.main_font_style, configuration.main_font_size),
                                               fg_color=configuration.dropdown_fg_color, dropdown_hover_color=configuration.button_hover_color)
        self.dropdown_stim.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.load_stim_button = ctk.CTkButton(frame, text='Load', font=(configuration.main_font_style, configuration.main_font_size),
                                              fg_color=configuration.button_fg_color, hover_color=configuration.button_hover_color,
                                              image=self.load_icon, command=lambda: self.event_handler(Event.START_SPECIFIC_STIM))
        self.load_stim_button.grid(row=2, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        # Stimulus Dropdown Box
        dropdown_values_time_bw_samp = [f'Time bw Samples: {x} sec' for x in np.arange(0.5, 4.5, 0.5)]
        self.option_var_time_bw_samp = tk.StringVar(value=dropdown_values_time_bw_samp[3])  # Set initial value to the prompt text
        self.dropdown_time_bw_samp = ctk.CTkOptionMenu(frame, variable=self.option_var_time_bw_samp, values=dropdown_values_time_bw_samp,
                                                       font=(configuration.main_font_style, configuration.main_font_size),
                                                       fg_color=configuration.dropdown_fg_color, dropdown_hover_color=configuration.dropdown_hover_color)
        self.dropdown_time_bw_samp.grid(row=3, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    def experiment_metadata_frames_1(self, frame):

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        self.current_stimulus_label = ctk.CTkLabel(frame, text='Current Simulus #:',font=(configuration.main_font_style, configuration.main_font_size))
        self.current_stimulus_label.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')
        self.current_stimulus_display = ctk.CTkLabel(frame, text='None',font=(configuration.main_font_style, configuration.main_font_size))
        self.current_stimulus_display.grid(row=0, column=1, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.total_time_label = ctk.CTkLabel(frame, text='Total Time:', font=(configuration.main_font_style, configuration.main_font_size))
        self.total_time_label.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')
        self.total_time_display = ctk.CTkLabel(frame, text='00:00',font=(configuration.main_font_style, configuration.main_font_size))
        self.total_time_display.grid(row=1, column=1, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    def experiment_metadata_frames_2(self, frame):

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        self.speaker_projected_label = ctk.CTkLabel(frame, text='Speaker Projecting:', font=(configuration.main_font_style, configuration.main_font_size))
        self.speaker_projected_label.grid(row=0, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')
        self.speaker_projected_display = ctk.CTkLabel(frame, text='None', font=(configuration.main_font_style, configuration.main_font_size))
        self.speaker_projected_display.grid(row=0, column=1, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

        self.selection_made_label = ctk.CTkLabel(frame, text='Speaker Selected:', font=(configuration.main_font_style, configuration.main_font_size))
        self.selection_made_label.grid(row=1, column=0, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')
        self.selection_made_display = ctk.CTkLabel(frame, text='None',font=(configuration.main_font_style, configuration.main_font_size))
        self.selection_made_display.grid(row=1, column=1, padx=configuration.x_pad_2, pady=configuration.y_pad_2, sticky='nsew')

    # ACTIONS -------------------------------------------
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
            tk.Label(self.loading_popup, text="Loading audio samples, please wait...", font=("default_font", 20)).pack(
                pady=10)
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




# if __name__ == "__main__":
    # GUI_class()