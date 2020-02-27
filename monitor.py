"""
Main file.
Gets the number of humans and zombies in the game, 
then posts changes to a specified GroupMe chat.
Also logs stats at stats.txt.
"""

from __future__ import print_function
from urllib2 import urlopen
from sys import argv
from time import sleep
#from bs4 import BeautifulSoup
from parser import parser
from HTMLParser import HTMLParser
from library import *
from os import system
from datetime import datetime
import urllib

from config import *

def main():
    #Skips sending update to GroupMe on first pass
    first_run = True


    #with open("config.xml") as config_file:
    #settings = config_file.read()
    #config = BeautifulSoup(settings, "xml")
    #bot id taken from GroupMe
    #bot_id = str(config.GroupMe.bot_id.get_text().strip())
    bot_id = BOT_ID
    if bot_id == "FILL THIS IN":
        print("You need to fill in the bot id in the config file")
        exit()
    #if true, delays the GroupMe post by delay_in_mins
    #delay_msg = config.settings.delay_msg.get_text().strip() == "True"
    delay_msg = DELAY_MSG
    #delay_in_mins = int(config.settings.delay_in_mins.get_text().strip())
    delay_in_mins = DELAY_IN_MINS
    #seconds_between_checks= int(config.settings.seconds_between_checks.get_text().strip())
    seconds_between_checks = SECONDS_BETWEEN_CHECKS
    command = "curl -d '{"
    command+= '"text" : "starting", '
    command+= '"bot_id":"'+bot_id+'"}'
    command+= "' https://api.groupme.com/v3/bots/post"

    #system(command)



    #file for logging human and zombie counts
    f = open('stats.txt','a')
    old_players = {}


    while True:
        new_players = {}
        #Parse site, retrieve stats    
        #site = BeautifulSoup(urlopen('https://umbchvz.com/playerList.php').read())
        #f = urllib.urlopen('https://umbchvz.com/playerList.php')
        #site = f.read()
        #my_parser = parser()
        #my_parser.feed(str(site))
        #new_players = my_parser.getPlayers()

        link = 'https://umbchvz.com/playerList.php'
        response = urlopen(link)
        content = response.read()
        content = content.split("\n")[63]
        for player in content.split("<tr>"):
            if(len(player) >= 342):
                player = player[31:31+80]
                name = player.split("""</td><td style="position: relative">""")[0]
                this_player_status = ""
                try:
                    this_player_status = player.split("""</td><td style="position: relative">""")[1]
                    if this_player_status[0:2] == "OZ":
                        new_players[name] = "OZ"
                    elif this_player_status[0:5] == "human":
                        new_players[name] = "human"
                    elif this_player_status[0:6] == "zombie":
                        new_players[name] = "zombie"
                except:
                    pass
                    

        if not(new_players): #if dict is empty
            print("Didn't find any players")
            
            
        #if it's not the first time, then read in old_players from file on last run
        if first_run:
            f_input = open("players.txt", "r")
            players = f_input.read().split("\n")
            for player in players:
                player = player.split(";")
                try:
                    old_players[player[0]] = player[1]
                except:
                    pass
            f_input.close()
        
        #check for deaths
        
        change,humans,zombies = compareDict(old_players,new_players)
        
        if change:
            print(change)
            stats = 'at '+getDate()+': '+str(humans)+' Humans, and '+str(zombies)+' Zombies\n'
            f.write(stats) 
            print(stats + "\a")
            #send message in groupme
            message=change+' -- Humans: '+str(humans)+' Zombies: '+str(zombies)
            command = "curl -d '{"
            command+= '"text" : "'+message+'", '
            command+= '"bot_id":"'+bot_id+'"}'
            command+= "' https://api.groupme.com/v3/bots/post"
            if delay_msg:
                command += " | at now + " + str(delay_in_mins) + " minutes"
            system(command)
        
        cmd = ""
        
        if getDate()[-7:] == "06:30PM":
            #This is hard-coded for each weeklong
            if getDate()[0:2] == START_DATE[3:]:
                cmd = "curl -d '{\"text\" : \"" 
                cmd += "Safe time begins in 20 minutes. The mission tonight will be held at Sondheim 105." 
                cmd += "\", \"bot_id\" : \"" +bot_id+ "\"}' "
                cmd += "https://api.groupme.com/v3/bots/post"
                system(cmd)
            elif getDate()[0:2] == str(int(START_DATE[3:]) +1):
                cmd = "curl -d '{\"text\" : \""
                cmd += "Safe time begins in 20 minutes. The mission tonight will be held at Meyerhoff Room 030 (Lecture Hall 2)"
                cmd += "\", \"bot_id\" : \"" +bot_id+ "\"}' "
                cmd += "https://api.groupme.com/v3/bots/post"
                system(cmd)
            elif getDate()[0:2] == str(int(START_DATE[3:]) +2):
                cmd = "curl -d '{\"text\" : \""
                cmd += "Safe time begins in 20 minutes. The mission tonight will be held at Lecture Hall 1"
                cmd += "\", \"bot_id\" : \"" +bot_id+ "\"}' "
                cmd += "https://api.groupme.com/v3/bots/post"
                system(cmd)
            elif getDate()[0:2] == str(int(START_DATE[3:]) +3):
                cmd = "curl -d '{\"text\" : \""
                cmd += "Safe time begins in 20 minutes. The mission tonight will be held at Meyerhoff 030 (Lecture Hall 2)"
                cmd += "\", \"bot_id\" : \"" +bot_id+ "\"}' "
                cmd += "https://api.groupme.com/v3/bots/post"
                system(cmd)

        times = ["07:00AM", "11:00AM", "03:00PM", "07:00PM", "11:00PM", "03:00AM"]
        
        if getDate()[-7:] in times:
            cmd = "curl -d '{\"text\" : \""
            cmd += "WCKD is good."
            cmd += "\", \"bot_id\" : \"" +bot_id+ "\"}' "
            cmd += "https://api.groupme.com/v3/bots/post"
            system(cmd)
        
                
        times = ["07:00AM", "07:30AM", "08:00AM", "08:30AM", "09:00AM", "09:30AM", "10:00AM", "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "01:00PM", "01:30PM", "02:00PM", "02:30PM", "03:00PM", "03:30PM", "04:00PM", "04:30PM", "05:00PM", "05:30PM", "06:00PM"]
        """ 
        if getDate()[-7:] in times:
            cmd = "curl -d '{\"text\" : \""
            cmd += "This is a reminder that the mission will be in Sondheim 014 tonight and that everyone should stay in their current building until safe time if they can."
            cmd += "\", \"bot_id\" : \"" +bot_id+ "\"}' "
            cmd += "https://api.groupme.com/v3/bots/post"
            system(cmd)
        """
        if getDate()[-7:] == "06:50PM":
            cmd = "curl -d '{\"text\" : \""
            cmd += "Safe time has begun. Safe time will end at 7:00PM. Get to the lecture hall!"
            cmd += "\", \"bot_id\" : \"" +bot_id+ "\"}' "
            cmd += "https://api.groupme.com/v3/bots/post"
            system(cmd)
        if getDate()[-7:] == "09:50PM":
            cmd = "curl -d '{\"text\" : \""
            cmd += "Post-mission safe time will end in 10 minutes. Get to safety!"
            cmd += "\", \"bot_id\" : \"" +bot_id+ "\"}' "
            cmd += "https://api.groupme.com/v3/bots/post"
            system(cmd)
        if getDate()[-7:] == "ENTER TIME HERE":
            cmd = "curl -d '{\"text\" : \""
            cmd += "ENTER MESSAGE HERE"
            cmd += "\", \"bot_id\" : \"" +bot_id+ "\"}' "
            cmd += "https://api.groupme.com/v3/bots/post"
            system(cmd)

        first_run = False
        old_players = new_players

        #write current player list into file in case the program stops
        #unexpectedly and things happen while it's not running
        f_output = open("players.txt", "w")
        for name in new_players:
            f_output.write(name + ";" + new_players[name] + "\n")
        f_output.close()
   
        #wait for next cycle
        print(getDate()[-7:] + " Cycle complete")
        sleep(seconds_between_checks) 
    f.close()
main()
