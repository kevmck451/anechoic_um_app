# UM Sound Localization Experiment

## Overview
This application was developed for the University of Memphis Hearing Aid Research Laboratory (HARL). It's designed for an experiment to test participants' ability to localize sounds. The experiment takes place in a state-of-the-art anechoic chamber using a multi-speaker array. Participants, wearing VR headsets, will listen to speech from various speakers and identify the source of the sound from nine gender-neutral static avatars in the VR scene.

![App Home](docs/App%20Pic%20V7a.JPG)

## Features
- Multi-speaker array integration in an anechoic chamber.
- VR environment with 9 avatars representing different sound sources.
- Real-time tracking of participants' choices and reaction times.
- Background noise variation to study the impact of ambient noise on sound localization.

## Installation and Setup

### Prerequisites
- Python: Download and install Python from [Python Downloads](https://www.python.org/downloads/). Ensure you add Python to your system's PATH during the setup.

### Setting Up the Environment
1. **Check Python Installation**:
   - Open Terminal.
   - Check Python installation:
     ```
     python
     exit()
     ```
3. **Download Repo**:
   ```
   git clone https://github.com/kevmck451/anechoic_um_app
   ```
4. **Navigate to Your Project Directory**:
   ```
   cd Desktop/anechoic_um_app
   ```
5. **Create and Activate a Virtual Environment**:
   - Create:
     ```
     python -m venv myenv
     ```
   - Activate:
     ```
     myenv\Scripts\activate
     ```
   - If you encounter a permission issue in PowerShell:
     ```
     Set-ExecutionPolicy Unrestricted -Scope Process
     .\myenv\Scripts\Activate.ps1
     ```
   - To deactivate:
     ```
     deactivate
     ```
6. **Install Required Packages**:
   ```
   pip install -r requirements.txt
   ```
7. **Export Requirements** (if needed):
   ```
   pip freeze > requirements.txt
   ```

### Running the Application
- **On a Mac Computer**:
  - Run the app from the `anechoic_um_app` directory:
    ```
    python3.7 -m app.app_main
    ```
- **On a Windows Computer**:
  - Run the app from the `anechoic_um_app` directory:
    ```
    python .\app\app_main.py
    ```
- **On the Anechoic Chamber Computer**:
  - Navigate to the `anechoic_um_app` directory:
    ```
    python -m app.app_main
    ```


![App Home](docs/App%20Pic%20V7c.JPG)