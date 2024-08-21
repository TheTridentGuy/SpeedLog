# SpeedLog
SpeedLog is a self-hosted, web-based amateur radio logging system. 
It's backend is built using Python 3 and the Flask Framework, and 
the frontend is pure HTML/JS/CSS. It is licensed under GNU GPL-V3
# Basics:
**Menu:**
- Press the pen icon to go to the logging page
- Press the eye icon to go to the log viewer
- While in the viewer press the download icon to export the selected logs
# Requirements:
- Python 3.8+
- Flask
> Flask can be installed using `pip install flask`
# Running it:
Simply run `python3 server.py`, or `sudo python3 server.py` if using a port that requires sudo permissions.
# Configuration:
> The default value of the `pass_hash` config option is the SHA-512 of `password`. **It is highly recommended to change this from it's default value.**
The `config.json` file allows you to configure server options. Here are the the currently available options:
**required:**
- `save_file`: the filepath to save all the logs to
- `address`: address for the server, should be `localhost` for testing/local use, or `0.0.0.0` for production hosting
- `port`: port to run the server on, i.e `80`
- `pass_hash`: SHA-512 hexdigest of the password, defaults to SHA-512 of `password`
- More options coming soon
# Credits:
- Made with <3 by @TheTridentGuy
- Made possible by the Flask framework