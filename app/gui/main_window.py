import tkinter as tk
import customtkinter as ctk
from threading import Thread
import time

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

        self.title("CustomTkinter App")
        self.geometry("1000x600")

        # Top Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(pady=10, expand=True, fill='x')

        # Sub Frames for Top Frame
        title_frame = ctk.CTkFrame(top_frame)
        title_frame.pack(side='left', expand=True, padx=20)
        status_frame = ctk.CTkFrame(top_frame)
        status_frame.pack(side='right', expand=True, padx=20)

        # Title Label
        self.title_label = ctk.CTkLabel(title_frame, text="UM Anechoic Chamber Experiment",
                                        font=("default_font", 36),padx=30, pady=20)
        self.title_label.pack()

        # Connection Status Indicators
        self.tdt_status = ctk.CTkLabel(status_frame, text="TDT Hardware: Connected",
                                       text_color="green", font=("default_font", 16), padx=10, pady=10) # TODO: connection function
        self.tdt_status.pack()
        self.vr_status = ctk.CTkLabel(status_frame, text="VR Headset: Connected",
                                       text_color="green", font=("default_font", 16), padx=10, pady=10) # TODO: connection function
        self.vr_status.pack()

        # Middle Frame
        middle_frame = ctk.CTkFrame(self)
        middle_frame.pack(pady=10, expand=True, fill='x')

        # Sub Frames for Middle Frame
        dropdown_frame = ctk.CTkFrame(middle_frame)
        dropdown_frame.pack(side='left', expand=True, padx=10)
        info_frame = ctk.CTkFrame(middle_frame)
        info_frame.pack(side='right', padx=10, expand=True, fill='both')

        # Dropdown Box
        # TODO: dropdown selection gets info from file about it's contents
        dropdown_values=[f'Experiment {x}' for x in range(1, 21)]
        self.option_var = tk.StringVar()
        self.dropdown = ctk.CTkOptionMenu(dropdown_frame, variable=self.option_var, values=dropdown_values)
        self.dropdown.pack()
        self.dropdown.bind('<Configure>', self.update_info)

        # Info Display
        # TODO: info displayed is based on experiment selected
        self.info_label = ctk.CTkLabel(info_frame, text="Experiment Info:", font=("default_font", 12), padx=00, pady=50)
        self.info_label.pack(expand=True)

        # Bottom Frame
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(pady=10, expand=True, fill='x')

        # Sub Frames for Bottom Frame
        start_frame = ctk.CTkFrame(bottom_frame)
        start_frame.pack(side='left', expand=True, padx=10)
        pause_frame = ctk.CTkFrame(bottom_frame)
        pause_frame.pack(side='left', expand=True, padx=10)
        timer_frame = ctk.CTkFrame(bottom_frame)
        timer_frame.pack(side='right', expand=True, padx=10)

        # Play Button
        self.start_button = ctk.CTkButton(start_frame, text="Start", font=("default_font", 16), command=self.start_timer)
        self.start_button.pack()

        # Pause Button
        self.pause_button = ctk.CTkButton(pause_frame, text="Pause", font=("default_font", 16), command=self.pause_timer)
        self.pause_button.pack()

        # Timer Label
        self.timer_label = ctk.CTkLabel(timer_frame, text="00:00:00", font=("default_font", 16), padx=50, pady=50)
        self.timer_label.pack()

        # Timer Variables
        self.timer_running = False
        self.timer_counter = 0

    def update_info(self, event=None):
        selected_option = self.option_var.get()
        self.info_label.configure(text=f"Information about {selected_option}")

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            Thread(target=self.update_timer).start()

    def pause_timer(self):
        self.timer_running = False

    def update_timer(self):
        start_time = time.time()  # Record the start time
        while self.timer_running:
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            minutes, seconds = divmod(elapsed_time, 60)
            tenths = int((seconds - int(seconds)) * 10)
            seconds = int(seconds)
            time_string = f"{int(minutes):02d}:{seconds:02d}.{tenths:1d}"
            self.timer_label.configure(text=time_string)
            time.sleep(0.01)  # Update every 10 milliseconds


if __name__ == "__main__":
    app = App()
    app.mainloop()