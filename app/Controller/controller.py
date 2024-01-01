
from enum import Enum, auto


class Controller:
    def __init__(self, tdt_hardware, vr_hardware):
        self.tdt_hardware = tdt_hardware
        self.vr_hardware = vr_hardware
        self.state = State.IDLE

    def set_gui(self, gui):
        self.gui = gui

    def handle_event(self, event):
        print(event)

        # These are the gate keepers for whether or not to perform the action
        if event == Event.TDT_CONNECT:
            print(f'State: {self.state}')


        elif event == Event.VR_CONNECT:
            print(f'State: {self.state}')


        elif event == Event.LOAD_EXPERIMENT:
            print(f'State: {self.state}')
            print(f'Options: {self.gui.Main_Frame.option_var_exp.get()}')


        elif event == Event.START_WARMUP:
            print(f'State: {self.state}')
            print(f'Options: {self.gui.Main_Frame.option_var_time_bw_samp.get()}')


        elif event == Event.START_EXPERIMENT:
            print(f'State: {self.state}')
            print(f'Options: {self.gui.Main_Frame.option_var_time_bw_samp.get()}')


        elif event == Event.END_EXPERIMENT:
            print(f'State: {self.state}')


        elif event == Event.PAUSE:
            print(f'State: {self.state}')


        elif event == Event.START_SPECIFIC_STIM:
            print(f'State: {self.state}')
            print(f'Options: {self.gui.Main_Frame.option_var_stim.get()}')


        else: return


        print('-'*40)

# Define the states using an enumeration
class State(Enum):
    IDLE = auto()
    VR_INITIALIZING = auto()
    VR_RUNNING = auto()
    TDT_INITIALIZING = auto()
    TDT_RUNNING = auto()
    LOADING_EXPERIMENT = auto()
    WARMUP_RUNNING = auto()
    EXPERIMENT_RUNNING = auto()
    EXPERIMENT_PAUSED = auto()
    SHUTTING_DOWN = auto()

# Define the events
class Event(Enum):
    TDT_CONNECT = auto()
    VR_CONNECT = auto()
    LOAD_EXPERIMENT = auto()
    START_WARMUP = auto()
    START_EXPERIMENT = auto()
    END_EXPERIMENT = auto()
    PAUSE = auto()
    START_SPECIFIC_STIM = auto()


'''
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


'''