> **NOTICE:** we are aware of a few bugs that break SpeedLog on 
> chromium-based browsers. If you are experiencing any issues we recommend Firefox.
# SpeedLog
SpeedLog is a web-based amateur radio logging system. 
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
- `user_file`:  the file to store user data in
- `allow_acct_creation`: whether or not to allow the creation of new accounts,
should be a boolean `true`/`false` value.
# Limitations:
- Tested on Firefox and the Mozilla engine.
- There used to be a bug on Chromium, but it should be fixed, however,
this software hasn't been fully tested on Chromium.
- Currently no mobile support
# Mobile Spport:
- SpeedLog does not currently support mobile, **however, it is expected to support it in the near future**
# Official Deployments:
- SpeedLog is currently deployed at https://speedlog.pythonanywhere.com
- **DISCLAIMER:** we are not responsible for any data that you give us lost, made public, deleted or otherwise compromised, please back up your own logs, and **NEVER** put sensitive information in logs.
# Credits:
- Made with <3 by @TheTridentGuy
- Made possible by the Flask framework