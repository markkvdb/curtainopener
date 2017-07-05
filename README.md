# Curtain opener

## Info
Application to open or close your curtain using a webserver-based control for the stepper motor that's connected to a RPI 3.

## Installation

### Software
1. Clone repository to folder. Open it by running `cd curtainopener`.
2. Create virtual environment within the curtainopener folder, by running the command `virtualenv -p python3 venv`.
3. Activate virtual environment `source venv/bin/activate`.
4. Install requirements and setup: `pip install -e .`
5. Set-up database: `python initdb.py`
6. Run server: `python run.py`

If you want to start the server again after installing, first activate the virtual environment by running `source venv/bin/activate`.

### Hardware
1. Get the following parts: 
    - Stepper motor suitable of opening and closing your curtain(s)
    - Stepper motor driver with the following inputs:
        - Step
        - Direction
        - Enable
2. Connect GPIO pin 4 to the Direction (CW/CCW) pin of your stepper driver
3. Connect GPIO pin 17 to the Step pin of your stepper driver
4. Connect GPIO pin 22 to the Enable pin of your stepper driver
5. Be creative in making the mechanical part work, for example the stepper driving a small rope which is connected to the curtain, if possible using pulleys
