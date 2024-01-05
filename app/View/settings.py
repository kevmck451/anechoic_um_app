from tkinter import PhotoImage
import customtkinter as ctk
import tkinter as tk
import numpy as np
import warnings

import app.View.configuration as configuration
from app.Controller.events import Event



# Settings Window
class Settings_Window(ctk.CTk):
    def __init__(self, event_handler, initial_values):
        super().__init__()
        ctk.set_appearance_mode("light")
        # Computer Icon

        # Main Setup ------------------------------------------------------------
        self.title(configuration.settings_window_title)

        # Get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width / 2) - (configuration.settings_window_width / 2))
        center_y = int((screen_height / 2) - (configuration.settings_window_height / 2))
        self.geometry(f'{configuration.settings_window_width}x{configuration.settings_window_height}+{center_x}+{center_y}')
        self.minsize(configuration.settings_min_window_width, configuration.settings_min_window_height)


        self.Main_Frame = Settings_Frame(self, event_handler, initial_values)
        self.columnconfigure(0, weight=1)  # Left column with 2/3 of the spac
        self.rowconfigure(0, weight=1)  # Left column with 2/3 of the spac
        self.Main_Frame.grid(row=0, column=0, sticky='nsew')  # Left frame in column 0

        # Ending Procedures
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Perform any cleanup or process termination steps here
        # For example, safely terminate any running threads, save state, release resources, etc.
        # print("Performing cleanup before exiting...")  # Replace this with actual cleanup code

        # End the application
        self.destroy()


class Settings_Frame(ctk.CTkFrame):
    def __init__(self, parent, event_handler, initial_values):
        super().__init__(parent)

        self.event_handler = event_handler
        self.initial_value = initial_values

        self.playing_icon = PhotoImage(file=configuration.playing_icon_filepath)
        self.start_icon = PhotoImage(file=configuration.start_icon_filepath)
        self.stop_icon = PhotoImage(file=configuration.stop_icon_filepath)
        self.pause_icon = PhotoImage(file=configuration.pause_icon_filepath)
        self.load_icon = PhotoImage(file=configuration.load_icon_filepath)
        self.settings_icon = PhotoImage(file=configuration.settings_icon_filepath)
        self.reset_icon = PhotoImage(file=configuration.reset_icon_filepath)
        warnings.filterwarnings('ignore', category=UserWarning, module='customtkinter.*')

        # Main Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(padx=configuration.x_pad_main, pady=configuration.y_pad_main, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)  # Configure the column to expand
        self.grid_rowconfigure(0, weight=1)  # Configure the column to expand

        self.setting_frames(main_frame)

    def setting_frames(self, frame):
        frame.grid_rowconfigure(0, weight=1)  # Row for the load button
        frame.grid_rowconfigure(1, weight=1)  # Row for the load button
        frame.grid_rowconfigure(2, weight=1)  # Row for the load button
        frame.grid_rowconfigure(3, weight=1)  # Row for the load button
        frame.grid_columnconfigure(0, weight=1)  # Single column

        # Stimulus Dropdown Box
        dropdown_values_time_bw_samp = [f'Time bw Samples: {x} sec' for x in np.arange(0, 4.5, 0.5)]
        value_list = [x for x in np.arange(0, 4.5, 0.5)]
        init_index = 0
        for i, value in enumerate(value_list):
            # print(str(self.initial_value[0]), str(value))
            if str(self.initial_value[0]) == str(value):
                init_index = i

        self.option_var_time_bw_samp = tk.StringVar(value=dropdown_values_time_bw_samp[init_index])  # Set initial value
        self.dropdown_time_bw_samp = ctk.CTkOptionMenu(frame, variable=self.option_var_time_bw_samp,
                                                       values=dropdown_values_time_bw_samp,
                                                       font=(configuration.main_font_style, configuration.main_font_size),
                                                       fg_color=configuration.dropdown_fg_color,
                                                       dropdown_hover_color=configuration.dropdown_hover_color)
        self.dropdown_time_bw_samp.grid(row=0, column=0, padx=configuration.x_pad_setting, pady=configuration.y_pad_setting,
                                        sticky='nsew')

        # Load Stim Button
        self.save_default_bw_time = ctk.CTkButton(frame, text='Change Default',
                                              font=(configuration.main_font_style, configuration.main_font_size),
                                              fg_color=configuration.button_fg_color,
                                              hover_color=configuration.button_hover_color,
                                              command=lambda: self.event_handler(Event.SET_DEFAULT_BW_TIME))
        self.save_default_bw_time.grid(row=1, column=0, padx=configuration.x_pad_setting, pady=configuration.y_pad_setting,
                                   sticky='nsew')

        # Stimulus Dropdown Box
        dropdown_values_stim = [f'Stimulus Start Number: {x}' for x in range(1, 101)]
        self.option_var_stim = tk.StringVar(value=dropdown_values_stim[0])  # Set initial value to the prompt text
        self.dropdown_stim = ctk.CTkOptionMenu(frame, variable=self.option_var_stim, values=dropdown_values_stim,
                                               font=(configuration.main_font_style, configuration.main_font_size),
                                               fg_color=configuration.dropdown_fg_color, dropdown_hover_color=configuration.button_hover_color)
        self.dropdown_stim.grid(row=2, column=0, padx=configuration.x_pad_setting, pady=configuration.y_pad_setting, sticky='nsew')

        # Load Stim Button
        self.load_stim_button = ctk.CTkButton(frame, text='Load', font=(configuration.main_font_style, configuration.main_font_size),
                                              fg_color=configuration.button_fg_color, hover_color=configuration.button_hover_color,
                                              command=lambda: self.event_handler(Event.SET_STIM_NUMBER))
        self.load_stim_button.grid(row=3, column=0, padx=configuration.x_pad_setting, pady=configuration.y_pad_setting, sticky='nsew')




