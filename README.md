# Pterodactyl Server Monitor

This Python script allows you to monitor the performance of servers on a Pterodactyl panel and shut down those that are inactive for a specified period of time.
Features

    Monitor server resources (CPU usage).
    Shut down inactive servers using less than 50% CPU for a certain duration.
    Use Pterodactyl's API to retrieve server information and perform actions (start, stop, restart).

Prerequisites
  - Python 3.x
  - Python libraries:
      - requests
      - python-dotenv
        
Installation
1. Clone the project

Clone this repository to your local machine:
```
git clone https://github.com/OmeSky-Studio/Stop-Free-server-pterodactyl.git
```
2. Install dependencies

Install the required libraries:
```
pip install -r requirements.txt
```
3. Create a .env file

In the project directory, create a .env file and add the following information:
```
PANEL_URL=http://url_panel/api/client  # Replace with your panel URL
API_KEY=api_key_client  # Replace with your API key
NODE_NAME=NODE_NAME  # Name of the node you want to monitor
TIME_INACTIF=5  # Inactivity time in minutes before shutting down the server
```
4. Run the script

Once you’ve configured your .env file, you can run the script by executing:
```
python monitor_servers.py
```
