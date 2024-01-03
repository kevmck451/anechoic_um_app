
from enum import Enum, auto
from threading import Thread
import time

from TDT_manager import TDT_Circuit
from VR_manager import VR_Headset_Hardware
from data_manager import circuit_data
from experiment_state import Experiment
from settings import Settings_Window
from events import Event
import configuration

class Controller:
    def __init__(self):
        self.app_state = State.IDLE
        self.sample_names_list = list
        self.audio_samples_list = list
        self.channel_list = list
        self.loaded_experiment_name = str
        self.experiment_loaded = False
        self.tdt_hardware = TDT_Circuit()
        self.vr_hardware = VR_Headset_Hardware()
        self.experiment = Experiment()
        self.warmup = Experiment()
        self.stop_flag_raised = False

    def set_gui(self, gui):
        self.gui = gui

    # These are the gate keepers for whether or not to perform the action
    def handle_event(self, event):
        # Connect to TDT Hardware:
        if event == Event.TDT_CONNECT:
            if self.app_state == State.IDLE:
                self.app_state = State.TDT_INITIALIZING
                self.tdt_hardware.connect_hardware()
                self.app_state = State.IDLE

        # Connect to VR Hardware:
        elif event == Event.VR_CONNECT:
            if self.app_state == State.IDLE:
                self.app_state = State.VR_INITIALIZING
                self.vr_hardware.connect()
                self.app_state = State.IDLE

        # Load Experiment: FINISHED
        elif event == Event.LOAD_EXPERIMENT:
            if self.app_state == State.IDLE:
                selected_value = self.gui.Main_Frame.option_var_exp.get()

                if selected_value != 'Select an Experiment':
                    if selected_value == self.loaded_experiment_name:
                        self.gui.Main_Frame.warning_popup_general(message='Experiment already Loaded')
                    else:
                        self.loaded_experiment_name = selected_value
                        self.app_state = State.LOADING_EXPERIMENT
                        self.load_experiment(selected_value)
                else:
                    if selected_value == 'Select an Experiment':
                        self.gui.Main_Frame.warning_popup_general(message='Need to select an Experiment')

        # Start Warmup:
        elif event == Event.START_WARMUP:
            if self.app_state == State.IDLE:
                self.start_warmup()

        # END Warmup:
        elif event == Event.END_WARMUP:
            if self.app_state == State.WARMUP_RUNNING:
                self.stop_flag_raised = True
                # self.end_warmup()
                self.app_state = State.IDLE

        # Start Experiment:
        elif event == Event.START_EXPERIMENT:
            if self.app_state == State.IDLE:
                if self.gui.Main_Frame.option_var_exp.get() == 'Select an Experiment':
                    self.gui.Main_Frame.warning_popup_general(message='Need to select an Experiment')
                elif self.experiment_loaded == False:
                    self.gui.Main_Frame.warning_popup_general(message='No Experiment Loaded')
                elif self.gui.Main_Frame.option_var_exp.get() != self.loaded_experiment_name:
                    self.gui.Main_Frame.warning_popup_general(message='Loaded Experiment doesnt\nmatch Selected Experiment')
                else:
                    self.start_experiment()

        # End Experiment:
        elif event == Event.END_EXPERIMENT:
            if self.app_state == State.EXPERIMENT_RUNNING or \
                    self.app_state == State.EXPERIMENT_PAUSED:
                if self.gui.Main_Frame.pause_button_state == False:
                    self.gui.Main_Frame.toggle_pause_button()
                self.app_state = State.EXPERIMENT_ENDED
                self.end_experiment()

        # Pause Experiment:
        elif event == Event.PAUSE:
            if self.app_state == State.EXPERIMENT_RUNNING:
                self.gui.Main_Frame.toggle_pause_button()
                self.app_state = State.EXPERIMENT_PAUSED

        # Resume Experiment:
        elif event == Event.RESUME:
            if self.app_state == State.EXPERIMENT_PAUSED:
                self.gui.Main_Frame.toggle_pause_button()
                self.app_state = State.EXPERIMENT_RUNNING

        # Load from Specific Stimulus Number:
        elif event == Event.SETTINGS:
            if self.app_state == State.EXPERIMENT_PAUSED or \
                    self.app_state == State.IDLE or \
                    self.app_state == State.EXPERIMENT_ENDED:
                self.settings_window = Settings_Window(self.handle_event)
                self.settings_window.mainloop()

        # Get Current Stim Number to Display
        elif event == Event.STIM_NUMBER:
            # set gui variable from experiment variable
            if self.app_state == State.WARMUP_RUNNING:
                self.gui.Main_Frame.current_stim_number = self.warmup.current_stim_number
            elif self.app_state == State.EXPERIMENT_RUNNING:
                self.gui.Main_Frame.current_stim_number = self.experiment.current_stim_number

        # Get Current Channel Number to Display
        elif event == Event.CHANNEL_NUMBER:
            # set gui variable from experiment variable
            if self.app_state == State.WARMUP_RUNNING:
                self.gui.Main_Frame.current_speaker_projecting_number = self.warmup.current_speaker_projecting
            elif self.app_state == State.EXPERIMENT_RUNNING:
                self.gui.Main_Frame.current_speaker_projecting_number = self.experiment.current_speaker_projecting

        # Get Current Channel Selected to Display
        elif event == Event.CHANNEL_SEL_NUMBER:
            # set gui variable from experiment variable
            if self.app_state == State.WARMUP_RUNNING:
                self.gui.Main_Frame.current_speaker_selected_number = self.warmup.current_speaker_selected
            elif self.app_state == State.EXPERIMENT_RUNNING:
                self.gui.Main_Frame.current_speaker_selected_number = self.experiment.current_speaker_selected

        # Reset Experiment Conditions
        elif event == Event.RESET_EXPERIMENT:
            self.reset_experiment()
            self.app_state = State.IDLE

        # Set Stim Number from Settings
        elif event == Event.SET_STIM_NUMBER:
            # Number to set trigger audio to
            print(self.settings_window.Main_Frame.option_var_stim.get())

        # Set default time between samples value
        elif event == Event.SET_DEFAULT_BW_TIME:
            # get value selected and set default
            configuration.set_default_time_bw_samples_value(self.settings_window.Main_Frame.option_var_time_bw_samp.get())

    def load_experiment(self, selected_value):
        exp_num = selected_value.split(' ')[1]
        self.sample_names_list = circuit_data.load_audio_names(exp_num)
        self.gui.Main_Frame.manage_loading_audio_popup(show=True)
        load_thread = Thread(target=self.load_audio_samples, args=exp_num, daemon=True)
        load_thread.start()

    def load_audio_samples(self, experiment_id):
        self.audio_samples_list = circuit_data.load_audio_samples(experiment_id)
        self.channel_list = circuit_data.load_channel_numbers(experiment_id)
        self.experiment.set_audio_channel_list(self.audio_samples_list, self.channel_list)
        self.experiment_loaded = True
        self.gui.Console_Frame.update_console_box(self.sample_names_list, experiment=experiment_id)
        self.gui.Main_Frame.close_loading_popup()
        self.app_state = State.IDLE

    def start_warmup(self):
        self.app_state = State.WARMUP_RUNNING
        self.gui.Main_Frame.toggle_warmup_button()
        warmup_audio, warmup_channels = circuit_data.load_warmup_data()
        self.warmup.set_audio_channel_list(warmup_audio, warmup_channels)
        self.warmup.experiment_in_progress = False

        self.warmup.current_index = 0
        self.warmup.max_index = 4
        self.warmup.update_current_stim_number(self.warmup.current_index)
        self.gui.Main_Frame.update_stim_number()
        self.gui.Main_Frame.update_speaker_projecting_number()
        self.gui.Main_Frame.update_speaker_selected_number()
        task_thread = Thread(target=self.perform_warmup_round, daemon=True)
        task_thread.start()


    def perform_warmup_round(self):
        while self.warmup.current_index <= self.warmup.max_index:
            if self.warmup.experiment_in_progress == False:
                self.warmup.experiment_in_progress = True

                audio_sample = self.warmup.audio_sample_list[self.warmup.current_index]
                channel_num = self.warmup.channel_list[self.warmup.current_index]
                self.warmup.current_speaker_projecting = channel_num

                if self.tdt_hardware.circuit_state == False:
                    self.tdt_hardware.trigger_audio_sample_computer(audio_sample)

                else:
                    # real TDT Hardware code here
                    self.tdt_hardware.trigger_audio_sample(audio_sample, channel_num)

                # time.sleep(audio_sample.sample_length)
                time.sleep(1)
                self.warmup.current_index += 1
                if self.warmup.current_index < 6:
                    self.warmup.update_current_stim_number(self.warmup.current_index)
                self.warmup.experiment_in_progress = False
            if self.stop_flag_raised: break

        self.end_warmup()


    def end_warmup(self):
        self.warmup.current_index = ''
        self.warmup.current_speaker_projecting = ''
        self.warmup.current_speaker_selected = ''
        self.gui.Main_Frame.stop_update_stim_number()
        self.gui.Main_Frame.stop_update_speaker_projecting_number()
        self.gui.Main_Frame.stop_update_speaker_selected_number()
        self.gui.Main_Frame.toggle_warmup_button()
        self.stop_flag_raised = False
        self.gui.Main_Frame.reset_metadata_displays()
        self.app_state = State.IDLE


    def start_experiment(self):
        self.gui.Main_Frame.toggle_start_button()
        self.app_state = State.EXPERIMENT_RUNNING
        self.gui.Main_Frame.start_experiment_timer()



        self.gui.Main_Frame.update_stim_number()


        # Thread to Start Procedure

    def end_experiment(self):
        self.gui.Main_Frame.toggle_start_button()
        self.gui.Main_Frame.stop_experiment_timer()
        self.gui.Main_Frame.stop_update_stim_number()

    def reset_experiment(self):
        self.gui.Main_Frame.toggle_start_button()
        self.gui.Console_Frame.reset_console_box()
        self.gui.Main_Frame.reset_metadata_displays()
        self.gui.Main_Frame.reset_dropdown_box()
        self.experiment_loaded = False
        self.loaded_experiment_name = 'Select an Experiment'




# Define the states using an enumeration
class State(Enum):
    VR_INITIALIZING = auto()
    TDT_INITIALIZING = auto()
    IDLE = auto()
    LOADING_EXPERIMENT = auto()
    WARMUP_RUNNING = auto()
    EXPERIMENT_RUNNING = auto()
    EXPERIMENT_PAUSED = auto()
    EXPERIMENT_ENDED = auto()
    SHUTTING_DOWN = auto()
    SETTINGS_OPEN = auto()




# ACTION FUNCTIONS ---------------------------------------------
def reset_tdt_hardware(self):
    self.circuit = TDT_Circuit()

    if self.circuit.circuit_state:
        connection_status_TDT = 'TDT Hardware: Connected'
        text_color_TDT = '#2B881A'
    else:
        connection_status_TDT = 'TDT Hardware: Not Connected'
        text_color_TDT = '#BD2E2E'

    self.tdt_status.configure(text=connection_status_TDT, text_color=text_color_TDT)

def reset_headset_hardware(self):
    self.parent.headset = VR_Headset_Hardware()

    if self.parent.headset.headset_state:
        connection_status_VR = 'VR Headset: Connected'
        text_color_VR = '#2B881A'
    else:
        connection_status_VR = 'VR Headset: Not Connected'
        text_color_VR = '#BD2E2E'

    self.vr_status.configure(text=connection_status_VR, text_color=text_color_VR)

def check_hardware_status(self):

    if self.parent.circuit.circuit_state:
        connection_status_TDT = 'TDT Hardware: Connected'
        text_color_TDT = '#2B881A'
    else:
        connection_status_TDT = 'TDT Hardware: Not Connected'
        text_color_TDT = '#BD2E2E'

    self.tdt_status.configure(text=connection_status_TDT, text_color=text_color_TDT)

    if self.parent.headset.headset_state:
        connection_status_VR = 'VR Headset: Connected'
        text_color_VR = '#2B881A'
    else:
        connection_status_VR = 'VR Headset: Not Connected'
        text_color_VR = '#BD2E2E'

    self.vr_status.configure(text=connection_status_VR, text_color=text_color_VR)

    self.parent.after(500, self.check_hardware_status)

# ---------------------------------------------

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
        vr_input = self.parent.headset.get_vr_input()


        if vr_input:  # todo change logic when a number equals channel
            test_widget.configure(text_color='#2B881A')  # update test display color to green
        else:
            test_widget.configure(text_color='#BD2E2E')

        # Time between Samples
        time_to_sleep = self.option_var_time_bw_samp.get().split(':')[1].strip().split(' ')[0]
        time.sleep(float(time_to_sleep))


    self.after(0, lambda: self.warmup_button.configure(fg_color='#578CD5', hover_color=self.parent.hover_color, image=self.parent.start_icon))  # Replace with original color


# EXPERIMENT FUNCTIONS ---------------------------------------------
def on_start_button_press(self):
    task_thread = Thread(target=self.start_experiment_procedure)
    task_thread.start()

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




