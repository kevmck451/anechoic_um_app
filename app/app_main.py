from circuit_control import circuit_manager
from vr_input import headset_manager
from gui import main_window



# Start App
main_window.run_app()
circuit_filename = 'audio_buffer'
audio_buffer_circuit = circuit_manager.TDT_connection(circuit_filename)
headset_manager.headset_connection()








