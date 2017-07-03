# Curtain opener

## Info
Application to open or close your curtain using a webserver-based control for the stepper motor that's connected to a RPI 3.

## Installation

### Software
1. Clone repository to folder. Open it by running `cd curtainopener`
2. Create virtual environment within the curtainopener folder, by running the command `virtualenv -p python3 venv`
3. Activate virtual environment `source venv/bin/activate`
4. Install requirements and setup: `pip install -e .`
5. Set-up database: `python initdb.py`
6. Run server: `python run.py`

If you want to start the server again after installing, first activate the virtual environment by running `source venv/bin/activate`, then run server `python3 run.py`

### Hardware
Nick's part.