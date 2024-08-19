# SpeedLog
SpeedLog is a self-hosted, web-based amateur radio logging system. 
It's backend is built using Python 3 and the Flask Framework, and 
the frontend is pure HTML/JS/CSS. It is licensed under GNU GPL-V3
# Requirements:
- Python 3.8+
- Flask
# Running it:
Simply run `python3 server.py`, or `sudo python3 server.py` permissions if using a port that requires them.
# Configuration:
The `config.json` file allows you to change minor aspects of how the
program runs. Here are the the currently available options:
**required:**
- `save_file`: the filepath to save all the logs too
- More options coming soon
# Credits:
- Made with <3 by @TheTridentGuy
- Made possible by the Flask framework