from os import system
from config import BOT_ID

bot_id = BOT_ID
#bot_id = ""


while True:
    cmd = "curl -d '{\"text\" : \""
    cmd += "WCKD is good" #Include the message in the quotes 
    cmd += "\", \"bot_id\" : \"" +bot_id+ "\"}' "
    cmd += "https://api.groupme.com/v3/bots/post"
    system(cmd)
    import time
    time.sleep(1)
    exit()

if(bot_id == "FILL THIS IN"):
    print "You need to fill in the bot id in the config file"
    exit()

system(cmd)
