# Pilot Telegram Bot
Telegram bot chat manager with administrative functions written on Python

## Functions
- Ban, kick, mute users
- Control users' permissions
- Spam accounts filter
- Warns system
- Notes
- Greeting and message about user leave
- Translator
- Weather forecast showing

## Deploying
### Normal deploy
1. Clone this repo and cd in this folder

2. If you want, you can create venv with following command:  
   `python -m venv venv`  
   And enter it (this example is for bash):  
   `source venv/bin/activate`

3. Install all required python packages:  
   `pip install -r requirements.txt`

4. Fill all needed lines in `config.py`, and then start bot with  
   `python main.py`

5. If all done well, it will ask you for a code which was sent to a helper account. If you see an error, check if `config.py` is filled properly.

6. To do autostart, you can add a systemd service (or daemon). Here is an example:

   ```
   [Unit]
   Description=Any description of daemon here
   After=network.target
   
   [Service]
   WorkingDirectory=/path/to/bot/sources
   Type=simple
   # If you aren't using venv, uncomment this and set your user
   #User=pi
   # If you aren't using venv, remove /path/to/bot/sources/venv/bin/ from command below
   ExecStart=/path/to/bot/sources/venv/bin/python3 -u /path/to/bot/sources/main.py
   # Restart bot after fail
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```

### Docker container deploy

1. Pull container from hub  
   `docker pull sanyapilot/pilotbot:bleeding`

2. Then do first start  
   `docker container run --name pilotbot -it -v /full/path/to/config/dir:/config sanyapilot/pilotbot:bleeding`  
   Remember to set -v argument properly, because without this bind-mount bot will fail to init, and you'll see such error:

   ```
   2021-05-07 12:04:14.260 | INFO     | init:<module>:22 - Welcome to PilotTelegramBot!
   2021-05-07 12:04:14.261 | INFO     | init:<module>:23 - Starting init...
   2021-05-07 12:04:14.261 | ERROR    | init:<module>:40 - Can't init! If starting in normal way, check config.py. If starting as Docker container, apply RW bind-mount to /config container's directory
   ```

   If all done well, you will be requested to edit a new `config.py` file created in config directory:

   ```
   2021-05-07 12:00:17.823 | INFO     | init:<module>:22 - Welcome to PilotTelegramBot!
   2021-05-07 12:00:17.823 | INFO     | init:<module>:23 - Starting init...
   2021-05-07 12:00:17.823 | INFO     | init:<module>:30 - Docker first start init
   2021-05-07 12:00:17.823 | INFO     | init:<module>:32 - Now fill lines in config.py and restart container again
   ```

3. Fill needed lines in `config.py` and start container again with the following command:  
   `docker container run --rm -it -v /full/path/to/config/dir:/config sanyapilot/pilotbot:bleeding`  
   If all ok, you'll be requested to enter a code which was sent to helper account. If you see an error, check if `config.py` is filled properly.

4. Enter the code. If the bot successfully started, press `Ctrl+C` to stop it, and run it in detached mode:  
   `docker container start pilotbot`

5. Check it's status by running  
   `docker container ls -a`

