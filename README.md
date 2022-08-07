# axelar-vote-notify
Axelar voter notify bot. 

## Setup

```bash
cd $HOME
mkdir $HOME/voter && cd $HOME/voter
wget https://raw.githubusercontent.com/Errorist79/axelar-vote-notify/main/app.py
```

deps

```bash
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.8
sudo apt-get install python3-pip -y
python3 -m pip install os-sys
python3 -m pip install requests
python3 -m pip install -U discord.py
```

Start 

```bash
python3 app.py
```

## environments
```bash
TOKEN = "#PUT_YOUR_BOT_TOKEN_HERE"
query_time = #API_QUERY_TIME_SEC
```

If you vote against the majority, the bot can also send alerts for it. The following parameter specifies the majority percentage.
For example, if you set it to 70, it will send you an alert if more than 70% of validators voted NO and you voted YES.
```bash
min_status = #Majority percentage
```
