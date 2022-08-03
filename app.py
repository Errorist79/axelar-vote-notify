import os
from discord.ext import commands, tasks
import requests
import json

### env ###
TOKEN = ""
query_time = 250

Bot = commands.Bot("$")
file_json = "data.json"

api_data = []
txhash_data = []
global min_status
min_status = 70

### functions ###

## register ##
def save(user_id, user_name, user_tag, API, channel_id):
    if API == None:
        API = None
    else:
        API = API[1:]

    try:
        file = json.load(open(file_json, "r", encoding="UTF-8"))
    except:
        file = []
    i = 0
    for user in file:
        if int(user["id"]) == int(user_id):
            while True:
                try:
                    jsonFile = open(file_json, "r", encoding="utf-8")
                    break
                except:
                    pass

            data = json.load(jsonFile)
            jsonFile.close()
            data[i]["api"] = API
            data[i]["channel_id"] = channel_id
            with open(file_json, mode='w', encoding="utf-8") as f:
                f.write(json.dumps(data, indent=2,ensure_ascii=False))
            return
        i += 1

    information = {
        'id': user_id,
        'username': user_name,
        'usertag': user_tag,
        'api': API,
        'channel_id': channel_id
    }
    a = []
    if not os.path.isfile(file_json):
        a.append(information)
        with open(file_json, mode='w', encoding="utf-8") as f:
            f.write(json.dumps(a, indent=2,ensure_ascii=False))
    else:
        with open(file_json, encoding="utf-8") as feedsjson:
            feeds = json.load(feedsjson)

        feeds.append(information)
        with open(file_json, mode='w', encoding="utf-8") as f:
            f.write(json.dumps(feeds, indent=2,ensure_ascii=False))
    
    if API in api_data:
        pass
    else:
        api_data.append(API)

## query ##
def query(api):
    for data in response_json:
        if data["voter"] == api:
            if data["vote"] == False:
                return [False, data]
            else:
                return [True, data]

    return [None, None]

## Bot auth ##
@Bot.event
async def on_ready():
    check_control_data.start()

## query loop ##
@tasks.loop(seconds=query_time)
async def check_control_data():
    vote_true = 0
    vote_false = 0
    try:
        file = json.load(open(file_json, "r", encoding="UTF-8"))
        global response_json
        try:
            response_json = json.loads(requests.get("https://testnet.api.axelarscan.io/evm-votes").text)["data"]
            # response_json = json.load(open("test.json", "r", encoding="UTF-8"))["data"]
        except:
            response_json = []

        for data in response_json:
            if data["vote"] == True:
                vote_true += 1
            elif data["vote"] == False:
                vote_false += 1
    except:
        file = []
    

    message_list = []
    message_list_true = []
    for user in file:
        channel_id = user["channel_id"]
        api = user["api"]
        if api == None or len(api) < 3:
            pass
        else:
            answer_query = query(api)
            answer = answer_query[1]
            if answer_query[0] == False:
                if answer["txhash"] in txhash_data:
                    pass
                else:
                    sender_chain = answer["sender_chain"]
                    txhash = answer["txhash"]
                    
                    data2 = []
                    for user2 in file:
                        if user2["api"] == api:
                            data2.append(f'<@{user2["id"]}>')

                    text_id = ""
                    for user_data_id in data2:
                        text_id = text_id + " " + user_data_id

                    message = f"Hey {text_id}, voted ***NO*** for {sender_chain}!\nTx Hash: `{txhash}`"
                    message_list.append([message, channel_id])
                    txhash_data.append(txhash)

            elif answer_query[0] == True:
                message_list_true.append([f'<@{user["id"]}>', channel_id])

    if int(min_status * (vote_true + vote_false) / 100) < vote_false:
        for message_i in message_list:
            await Bot.get_channel(int(message_i[1])).send(message_i[0])
    else:
        if len(message_list_true) > 0:
            text_id = ""
            for user_data_id in message_list_true:
                text_id = text_id + " " + user_data_id[0]
                channel_id = user_data_id[1]

            await Bot.get_channel(int(channel_id)).send(f"Voting result is incompatible with the majority. You may need to check. {text_id}")

## register app ##
@Bot.event
async def on_message(message):
    msg = await Bot.get_channel(int(message.channel.id)).fetch_message(int(message.id))
    msg_list = msg.content.split(" ")
    if msg_list[0].lower() == "$ping":
        await Bot.get_channel(int(message.channel.id)).send(f"Pong!({Bot.latency * 1000}ms)")
    elif msg_list[0].lower() == "$help":
        await Bot.get_channel(int(message.channel.id)).send(f"🧾 Set the voter address```bash\n You can register as $VOTERADDRESS or $VOTERADDRESS @username @username ... ```\n🔕 Delete your voter address```bash\n If you want to delete: $delete or $delete @username @username ... ```\n```bash\n For MS: $ping ```\n```bash\n For help: $help```")
    elif msg_list[0].lower() == "$min":
        try:
            new_min_status = int(msg_list[1])
            global min_status
            min_status = new_min_status
            await Bot.get_channel(int(message.channel.id)).send(f"Successful & Min: {str(min_status)}")
        except:
            await Bot.get_channel(int(message.channel.id)).send(f"Please enter number.")

    elif msg_list[0][0] == "$":
        if msg_list[0][:7] == "$delete":
            API = None
        else:
            API = msg_list[0]

        save(msg.author.id, msg.author.name, msg.author.discriminator, API, int(message.channel.id))

        if len(msg_list) != 1:
            a = 0
            users = []
            for msg_text in msg_list:
                if a == 0:
                    a += 1
                else:
                    if len(msg_text) < 5:
                        pass
                    else:
                        if msg_text[:2] == "<@":
                            users.append(msg_text.replace("<@","").replace(">","").replace(" ", ""))
                        else:
                            await Bot.get_channel(int(message.channel.id)).send(f"Failed {msg_text}")

            data3 = []
            data3.append(f'<@{msg.author.id}>')
            for user in users:
                user_data = await Bot.fetch_user(user)
                user_id = user
                user_name, user_tag = str(user_data).split("#")
                save(user_id, user_name, user_tag, API, int(message.channel.id))
                data3.append(f'<@{user_id}>')

            text_id = ""
            for user_data_id in data3:
                text_id = text_id + " " + user_data_id

            if len(users) > 0:
                if API == None:
                    await Bot.get_channel(int(message.channel.id)).send(f"Hey {text_id}, successfully deleted.")
                else:
                    await Bot.get_channel(int(message.channel.id)).send(f"Hey {text_id}, successfully saved.")
        else:
            if API == None:
                await Bot.get_channel(int(message.channel.id)).send(f"Dear <@{msg.author.id}>, successfully deleted.")
            else:
                await Bot.get_channel(int(message.channel.id)).send(f"Dear <@{msg.author.id}>, successfully saved.")

Bot.run(TOKEN)
